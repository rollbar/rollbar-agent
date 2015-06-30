#!/bin/bash
# chkconfig: 345 99 01
# description: rollbar-agent - watches log files and pushes events to rollbar
### BEGIN INIT INFO
# Provides:             rollbar-agent
# Required-Start:       $remote_fs $syslog $time $named
# Required-Stop:        $remote_fs $syslog $time $named
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short-Description:    Start rollbar-agent
# Description:          Enables rollbar-agent
### END INIT INFO

# Example init.d script for rollbar-agent
# Change the configuration variables as needed, then symlink to /etc/init.d/rollbar-agent

# rollbar configuration
CONFIG_FILE=/etc/rollbar-agent.conf

# system configuration
PROGRAM="/usr/local/rollbar-agent"
ARGS="--config=$CONFIG_FILE"
PROGNAME='rollbar-agent'
PIDFILE="/var/run/$PROGNAME.pid"
ALT_PIDFILE="/var/run/$PROGNAME.sh.pid"
LOGFILE="/var/log/$PROGNAME.log"
# If not using a virtualenv, change to VIRTUALENV=""
VIRTUALENV="PATH_TO_YOUR_VIRTUALENV"

function start() {
  echo "Starting $PROGRAM..."
  if [ -f $PIDFILE ] && kill -0 $(cat $PIDFILE); then
    echo "Service already running: $PROGNAME"
    exit 1
  fi

  if [ "$VIRTUALENV" != "" ]; then
    source $VIRTUALENV/bin/activate
  fi
  python -u $PROGRAM $ARGS >> $LOGFILE 2>&1 &
  echo $! > $PIDFILE
}

function stop() {
  echo "Stopping $PROGRAM..."
  if [ -f $PIDFILE ]; then
    kill `cat $PIDFILE`
    rm $PIDFILE
  elif [ -f $ALT_PIDFILE ]; then
    kill `cat $ALT_PIDFILE`
    rm $ALT_PIDFILE
  else
    echo "$PIDFILE not found, will attempt to look at ps list"
    # DIE DIE DIE
    for pid in `ps auxwww| grep $PROGRAM | grep -v grep | grep bash | awk '{print $2}'`; do
      kill -9 $pid
    done
  fi
  rm -f $PIDFILE
}

function condrestart() {
  echo "Doing Conditional Restart..."
  if [ -f $PIDFILE ]; then
    stop
    sleep 5
    start
  else
    echo "pidfile not found, not restarting"
  fi
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    sleep 5
    start
    ;;
  condrestart)
    condrestart
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|condrestart}"
esac
