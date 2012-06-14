#!/usr/bin/env python
"""
ratchetd - agent to monitor log files and send notices to Ratchet.io
"""

import copy
import hashlib
import json
import logging
import optparse  # for python2.6 compat
import os
import re
import shelve
import signal
import socket
import stat
import sys
import threading
import time

import requests

log = logging.getLogger(__name__)

DEFAULT_ENDPOINT = 'http://submit.ratchet.io/api/item/'
DEFAULT_TIMEOUT = 3  # in seconds


## utils

def send_payload(payload):
    # do immediate http post
    # in the future, will do this with batches and single separate thread
    requests.post(options.endpoint, data=payload, timeout=options.timeout)


def parse_timestamp(format, s):
    try:
        ts = time.mktime(time.strptime(s, format))
    except ValueError:
        # fall back to current timestamp
        ts = time.time()
    return int(ts)


## processors

def choose_processor(filename):
    if filename.endswith('.ratchet'):
        return RatchetFileProcessor
    return LogFileProcessor


class Processor(object):
    def __init__(self, scanner):
        self.scanner = scanner

    def process(self, fp):
        raise NotImplementedError()


class RatchetFileProcessor(Processor):
    """
    Processor for .ratchet files
    Each line is a json-encoded payload, so all we have to do is decode it and send it.
    """
    def process(self, fp, filename, state):
        for line in fp:
            log.debug("read line. length: %d hash: %s", len(line), hashlib.md5(line).hexdigest())
            self._process_line(line)
    
    def _process_line(self, line):
        line = line.strip()
        if not line:
            log.debug("Skipping empty line")
            return
        try:
            payload = json.loads(line)
        except ValueError:
            log.warning("Could not process badly formatted line: %s", line)

        send_payload(line)


class LogFileProcessor(Processor):
    """
    Processor for general log files - currently works reasonably well for paste/pylons log files.
    Some events we want will span multiple lines.
    """
    # list of tuples containing (pattern, strptime format)
    # pattern should put the timestamp into group #1
    _message_start_pats = [
        # pylons generic
        (re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(\d+)?\s+(?P<level>[A-Z]+)\s+(?P<title>.*$)'), 
         '%Y-%m-%d %H:%M:%S'),
    ]   

    def process(self, fp, filename, state):
        empty_message = {'data': [], 'timestamp': None, 'level': None, 'title': None}
        current_message = state.get('current_message', copy.deepcopy(empty_message))

        for line in fp:
            # does this look like the beginning of a new log message?
            new_message_match = None

            for pattern, format in self._message_start_pats:
                match = pattern.match(line)
                if match:
                    new_message_match = match
                    break

            if new_message_match:
                if current_message['data']:
                    # done with the previous item - send it off and clear data
                    self._process_message(current_message, filename)
                    current_message = copy.deepcopy(empty_message)
                
                # save interesting data from first line
                current_message['timestamp'] = parse_timestamp(format, 
                    new_message_match.group('timestamp'))
                current_message['level'] = new_message_match.group('level')
                current_message['title'] = new_message_match.group('title')
            
            current_message['data'].append(line)
        
        if self.scanner.scan_start_time - state['mtime'] > 1:
            # it's been at least 1 second since anything was written to the file
            # if there's a pending message, send it
            if current_message['data']:
                self._process_message(current_message, filename)
                current_message = copy.deepcopy(empty_message)

        state['current_message'] = current_message

    def _process_message(self, message, filename):
        data = "".join(message['data'])
        log.debug("Processing message. Timestamp: %s Level: %s Title: %s Data: %s",
            message['timestamp'], message['level'], message['title'], data)
        # eventually, we'll send level and title as separate params
        # for now, send it all together
        payload = {}
        payload['access_token'] = options.access_token
        payload['timestamp'] = message['timestamp']
        payload['body'] = data

        params = {}
        params.update(self.scanner.payload_params)
        params['server.log_file'] = filename

        payload['params'] = json.dumps(params)

        send_payload(payload)


## main thread and loop

class ScannerThread(threading.Thread):
    """
    The main 'scanner' thread - scans files and posts items to the ratchet.io api.
    There should only be a single instance of this thread.
    """
    def __init__(self, stop_event):
        super(ScannerThread, self).__init__()
        self.stop_event = stop_event
        self.filenames = ['/Users/brian/www/mox/log.ratchet', '/Users/brian/www/mox/mox.log']

        self.payload_params = {
            'server.host': socket.gethostname(),
            'server.environment': options.environment,
            'server.branch': options.branch,
            'server.root': options.root,
            'server.github.account': options.github_account,
            'server.github.repo': options.github_repo,
            'notifier.name': 'ratchetd',
        }

    def run(self):
        while not self.stop_event.is_set():
            log.info("scanner thread looping...")
            try:
                self.scan_all()
            except:
                log.exception("Caught exception in ScannerThread.run() loop")
            time.sleep(1)

    def scan_all(self):
        # we keep state in a dictionary like:
        # {'files': {'filename1': {'pos': 12345, 'inode': 4567}, ...}}
        self.scan_start_time = time.time()
        state = shelve.open('ratchetd.state')
        files = state.get('files', {})
        
        for filename in self.filenames:
            stats = os.stat(filename)
            inode = stats[stat.ST_INO]
            mtime = stats[stat.ST_MTIME]
            if filename in files:
                # filename we've seen before.
                if inode != files[filename]['inode']:
                    # file has been rotated. reset to position 0 and store new inode.
                    files[filename] = {'pos': 0, 'inode': inode, 'mtime': mtime}
            else:
                # new file - initialize
                files[filename] = {'pos': 0, 'inode': inode, 'mtime': mtime}

            self.scan_file(filename, files[filename])
        
        state['files'] = files
        state.close()

    def scan_file(self, filename, file_state):
        processor = choose_processor(filename)(self)
        with open(filename, 'r') as fp:
            pos = file_state['pos']
            log.debug("file %s seeking to pos %d", filename, pos)
            fp.seek(pos)
            processor.process(fp, filename, file_state)
            new_pos = fp.tell()
            log.debug("file %s new pos %d", filename, new_pos)
            file_state['pos'] = new_pos
        

def register_signal_handlers(stop_event):
    def signal_handler(signum, frame):
        log.info("Shutting down...")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT, signal.SIGALRM):
        signal.signal(sig, signal_handler)


def main_loop():
    stop_event = threading.Event()
    register_signal_handlers(stop_event)
    scanner = ScannerThread(stop_event)
    scanner.start()

    # sleep until the thread is killed 
    # have to sleep in a loop, instead of worker.join(), otherwise we'll never get the signals
    while scanner.isAlive():
        time.sleep(1)
    
    log.info("Shutdown complete")


def build_option_parser():
    parser = optparse.OptionParser()

    # verbosity
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, 
        help='Verbose output (uses log level DEBUG)')
    parser.add_option('-q', '--quiet', dest='quiet', action='store_true', default=False,
        help='Quiet output (uses log level WARNING)')
    
    # params
    parser.add_option('--access_token', dest='access_token', action='store',
        help='Ratchet.io project access token')
    parser.add_option('--environment', dest='environment', action='store', default='production',
        help='Environment name. Should be "production", "staging", or "development". Default: production')
    parser.add_option('--root', dest='root', action='store', default=os.getcwd(),
        help='Code root. Default: current directory')
    parser.add_option('--branch', dest='branch', action='store', default=None,
        help='Branch name')
    parser.add_option('--github.account', dest='github_account', action='store', default=None,
        help='Github account name')
    parser.add_option('--github.repo', dest='github_repo', action='store', default=None,
        help='Github repo name')
    parser.add_option('--endpoint', dest='endpoint', action='store', default=DEFAULT_ENDPOINT,
        help='Ratchet API endpoint. Default: %s' % DEFAULT_ENDPOINT)
    parser.add_option('--timeout', dest='timeout', action='store', default=DEFAULT_TIMEOUT,
        type='int',
        help='Per-POST timeout, in seconds. Default: %s' % DEFAULT_TIMEOUT)

    return parser


if __name__ == '__main__':
    parser = build_option_parser()

    (options, args) = parser.parse_args()
    mandatory_options = ['access_token']
    if not all(getattr(options, m, None) for m in mandatory_options):
        print "Missing one or more required arguments: %s" % ", ".join(mandatory_options)
        parser.print_help()
        sys.exit(1)

    # set up logging
    level = logging.INFO
    if options.verbose:
        level = logging.DEBUG
    elif options.quiet:
        level = logging.WARNING
    logging.basicConfig(level=level)

    # start main loop
    main_loop()

