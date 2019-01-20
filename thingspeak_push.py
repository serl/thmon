#!/usr/bin/python

import sys
import os
from datetime import datetime
from time import sleep
import config
from libs.thingspeak import ThingSpeak
os.chdir(os.path.dirname(sys.argv[0]))  # so that workdir = this dir


def main():
    """Uploads all files in cache to Thingspeak"""

    ts_client = ThingSpeak(config.TS_CHANNEL_ID, config.TS_WRITE_API_KEY)

    if not hasattr(config, 'TS_BULK_UPDATE_SIZE'):
        config.TS_BULK_UPDATE_SIZE = 50

    whole_cache = [int(f) for f in os.listdir('./cache') if f.isdigit()]
    cached = sorted(whole_cache)[0:config.TS_BULK_UPDATE_SIZE]
    entries = []
    files = []
    error = None
    for timestamp in cached:
        contents = ''
        filename = './cache/{}'.format(timestamp)
        with open(filename, 'r') as cnts:
            contents = cnts.read().strip()
        (temperature, humidity) = contents.split(' ')
        isodate = datetime.utcfromtimestamp(timestamp).isoformat()
        entry = {
            'field1': temperature, 'field2': humidity, 'created_at': isodate}
        if float(humidity) >= 50:
            # using approximated formula that works only in these conditions
            dew_point = float(temperature) - ((100 - float(humidity)) / 5)
            entry['field3'] = "{:.1f}".format(dew_point)
        entries.append(entry)
        files.append(filename)

    try:
        result = ts_client.bulk_update(entries)
        if 'error' in result:
            error = '{message} ({details})'.format(**result['error'])
    except Exception as e:
        error = 'Network error ({})'.format(e.message)
    if error:
        print "Error uploading data: {}".format(error)
        sys.exit(1)

    for f in files:
        os.remove(f)

    print "{} entries updated".format(len(entries))

if __name__ == "__main__":
    main()
