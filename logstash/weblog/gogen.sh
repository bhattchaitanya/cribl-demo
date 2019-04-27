#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
gogen -cd ${DIR}/../../gogen/gogen -v -f ${DIR}/weblog.log -o file -ot raw gen -s shoppingapache -c 1 -i 1 -r
