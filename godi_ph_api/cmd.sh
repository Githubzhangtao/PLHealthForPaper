#!/bin/bash
CMD=$1
PROJ_NAME='ph_api'
#LOG_FILE='/data/jeffreytian/DevOpsOa/jeff_live/ipv6_log.log'
function uwsgi_stop() {
    ps -ef|grep ${PROJ_NAME}|grep -v grep|grep uwsgi |awk '{print $2}'|xargs kill -9 >/dev/null 2>&1
}
function uwsgi_start(){
    uwsgi --ini uwsgi.ini --set name=${PROJ_NAME}
}
function uwsgi_reload() {
    uwsgi_stop
    uwsgi_start
}

case ${CMD} in
    start)
      uwsgi_start

    ;;
    stop)
      uwsgi_stop

    ;;
    reload)
      uwsgi_reload
    ;;
    *)
      echo './ cmd.sh start   to start '
      echo './ cmd.sh reload  to reload '
      echo './ cmd.sh stop    to stop '
    ;;
esac
