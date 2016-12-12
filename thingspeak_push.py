#!/usr/bin/python

import sys
import os
from datetime import datetime
from time import sleep
import config
from libs.http import HTTP
os.chdir(os.path.dirname(sys.argv[0]))  # so that workdir = this dir

http = HTTP({'THINGSPEAKAPIKEY': config.API_KEY})

if not hasattr(config, 'limit_uploads'):
    config.LIMIT_UPLOADS = 5

if not hasattr(config, 'delay'):
    config.DELAY = 16

cached = sorted([int(f) for f in os.listdir('./cache') if f.isdigit()])[0:config.LIMIT_UPLOADS]
for timestamp in cached:
    contents = ''
    filename = './cache/{}'.format(timestamp)
    with open(filename, 'r') as cnts:
        contents = cnts.read().strip()
    (temperature, humidity) = contents.split(' ')
    isodate = datetime.utcfromtimestamp(timestamp).isoformat()
    error = None
    try:
        result = http.call(
            'update', 'POST', {'field1': temperature, 'field2': humidity, 'created_at': isodate})
        if result == '0':
            error = 'Thingspeak exception'
        print result
    except:
        error = 'Network error'
    if error is not None:
        print "Error uploading data: {}".format(error)
        sys.exit(1)
    os.remove(filename)
    sleep(config.DELAY)
