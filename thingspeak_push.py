#!/usr/bin/python

import sys
import os
from datetime import datetime
from time import sleep
import config
from libs.http import HTTP
os.chdir(os.path.dirname(sys.argv[0]))  # so that workdir = this dir


def main():
    """Uploads all files in cache to Thingspeak"""

    http = HTTP({'THINGSPEAKAPIKEY': config.API_KEY})

    if not hasattr(config, 'LIMIT_UPLOADS'):
        config.LIMIT_UPLOADS = 5

    if not hasattr(config, 'DELAY'):
        config.DELAY = 16

    whole_cache = [int(f) for f in os.listdir('./cache') if f.isdigit()]
    cached = sorted(whole_cache)[0:config.LIMIT_UPLOADS]
    for timestamp in cached:
        contents = ''
        filename = './cache/{}'.format(timestamp)
        with open(filename, 'r') as cnts:
            contents = cnts.read().strip()
        (temperature, humidity) = contents.split(' ')
        isodate = datetime.utcfromtimestamp(timestamp).isoformat()
        error = None
        data_to_send = {
            'field1': temperature, 'field2': humidity, 'created_at': isodate}
        if float(humidity) >= 50:
            # using approximated formula that works only in these conditions
            dew_point = float(temperature) - ((100 - float(humidity)) / 5)
            data_to_send['field3'] = "{:.1f}".format(dew_point)
        try:
            result = http.call('update', 'POST', data_to_send)
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

if __name__ == "__main__":
    main()
