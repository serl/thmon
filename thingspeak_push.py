#!/usr/bin/env python

import os
from datetime import datetime

import requests

import config

os.chdir(os.path.dirname(__file__))  # so that workdir = this dir


def main():
    """Uploads all files in cache to Thingspeak"""

    if not hasattr(config, "TS_BULK_UPDATE_SIZE"):
        config.TS_BULK_UPDATE_SIZE = 50

    whole_cache = [int(f) for f in os.listdir("./cache") if f.isdigit()]
    cached = sorted(whole_cache)[0 : config.TS_BULK_UPDATE_SIZE]
    entries = []
    files = []
    for timestamp in cached:
        contents = ""
        filename = "./cache/{}".format(timestamp)
        with open(filename, "r") as cnts:
            contents = cnts.read().strip()
        try:
            (temperature, humidity) = contents.split(" ")
        except ValueError:
            continue
        isodate = datetime.utcfromtimestamp(timestamp).isoformat()
        entry = {"field1": temperature, "field2": humidity, "created_at": isodate}
        if float(humidity) >= 50:
            # using approximated formula that works only in these conditions
            dew_point = float(temperature) - ((100 - float(humidity)) / 5)
            entry["field3"] = "{:.1f}".format(dew_point)
        entries.append(entry)
        files.append(filename)

    res = requests.post(
        f"https://api.thingspeak.com/channels/{config.TS_CHANNEL_ID}/bulk_update.json",
        json={
            "write_api_key": config.TS_WRITE_API_KEY,
            "updates": entries,
        },
    )
    res.raise_for_status()
    data = res.json()
    if "error" in data:
        raise Exception(data)

    for f in files:
        os.remove(f)

    print("{} entries updated".format(len(entries)))


if __name__ == "__main__":
    main()
