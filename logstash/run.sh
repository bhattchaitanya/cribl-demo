#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
docker run -p 5044:5044 -p 5045:5045 -v ${DIR}/logstash:/etc/logstash -d cribl/logstash
