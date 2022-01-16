#!/bin/bash

cd "$(dirname "$0")"

source .venv/bin/activate

values=$(python dht22_read.py) &&
    echo "$values" > "cache/$(date +%s)"

LOCK='.lock'
if mkdir "$LOCK" 2>/dev/null; then
    python thingspeak_push.py
    rmdir "$LOCK"
fi
