#!/bin/bash
set -e

cd "$(dirname "$0")"

# shellcheck source=/dev/null
source .venv/bin/activate

if values=$(python dht22_read.py); then
    echo "$values" > "cache/$(date +%s)"
    echo "$values" > "cache/latest"
fi

LOCK='.lock'
if mkdir "$LOCK" 2>/dev/null; then
    python thingspeak_push.py
    rmdir "$LOCK"
fi
