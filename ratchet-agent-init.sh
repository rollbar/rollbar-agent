#!/bin/bash
# chkconfig: 345 99 01
# description: ratchet-agent - watches log files and pushes events to ratchet.io

# Example init.d script for ratchet-agent
# Change the configuration variables as needed, then symlink to /etc/init.d/ratchet-agent

# ratchet configuration
CONFIG_FILE=/etc/ratchet-agent.conf

# system configuration
PROGRAM="/var/www/ratchet-agent/ratchet-agent"
ARGS="--config=$CONFIG_FILE"
PROGNAME='ratchet-agent'
PIDFILE="/var/run/$PROGNAME.pid"
ALT_PIDFILE="/var/run/$PROGNAME.sh.pid"
LOGFILE="/var/log/$PROGNAME.log"
RUN_AS_USER='root'
RUN_AS_HOME='/root'
VIRTUALENV="$RUN_AS_HOME/envs/$PROGNAME"

function start() {
  echo "Starting $PROGRAM..."
  if [ -f $PIDFILE ]; then
    echo "$PIDFILE exists, exiting..."
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
