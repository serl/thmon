#!/bin/bash -e

cd "$(dirname "$0")"

values=$(sudo ./libs/read_value.py)
[[ $values ]] || exit 1
echo "$values" > "cache/$(date +%s)"
