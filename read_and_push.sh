#!/bin/bash

cd $(dirname $0)

./read_value.sh && ./parse_push.py
