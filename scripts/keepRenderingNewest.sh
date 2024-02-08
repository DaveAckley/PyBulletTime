#!/usr/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DELAY=${1-1h}

while [ 1 ]; do
    $DIR/newestSceneRender.pl 
    date
    trap 'echo -en "\n[^C CAUGHT]"' SIGINT
    echo -n "sleeping for $DELAY (^C to rerender now) - "
    sleep $DELAY &
    wait $!
    trap - SIGINT
    echo -n " ^C again within 2 sec to exit instead - "
    sleep 2s &
    wait $!
    date
done
