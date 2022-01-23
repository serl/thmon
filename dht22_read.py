#!/usr/bin/env python3

import sys
from time import sleep

import adafruit_dht
import board

dhtDevice = adafruit_dht.DHT22(board.D4)
max_number_of_reads = 50  # max reads attempted before exit(1)
good_reads_required = 2  # take the n-th successful read and stop trying
pause_between_reads = 3  # in seconds

f_val = ""
good_reads = 0
for i in range(max_number_of_reads):
    try:
        f_val = "{0:0.1f} {1:0.1f}".format(dhtDevice.temperature, dhtDevice.humidity)
        print("measure {}: {}".format(i + 1, f_val), file=sys.stderr)
        good_reads += 1
        if good_reads >= good_reads_required:
            print(f_val)
            sys.exit()
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print("measure {}: {}".format(i + 1, error.args[0]), file=sys.stderr)
    sleep(pause_between_reads)

sys.exit(1)
