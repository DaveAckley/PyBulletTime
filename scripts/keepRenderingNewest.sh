#!/usr/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DELAY=${1-1h}

while [ 1 ]; do
    $DIR/newestSceneRender.pl
    date
    echo -n sleeping for $DELAY -
    sleep $DELAY
    date
done
