#!/bin/bash

cd $(dirname $0)

values=$(sudo ./libs/read_value.py)
[ "$values" ] || exit 1
export $values
([ $TEMPERATURE ] && [ $HUMIDITY ]) || exit 2
echo "$TEMPERATURE $HUMIDITY" > cache/$(date +%s)
