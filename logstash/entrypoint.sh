#!/bin/sh

mkdir -p /var/log/logstash

if [ "$1" = "start" ]; then
    /usr/share/logstash/bin/logstash --path.settings /etc/logstash --config.reload.automatic
    exit $?
fi

exec "$@"
