#!/bin/bash

cd $(dirname $0)

./read_value.sh

LOCK='.lock'
if mkdir "$LOCK" 2>/dev/null; then
	echo ex
	./thingspeak_push.py
	rmdir "$LOCK"
fi
