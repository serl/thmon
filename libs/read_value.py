#!/usr/bin/python

import sys
from time import sleep
import Adafruit_DHT


def main():
    """read value from sensor"""

    number_of_reads = 2
    pause_between_reads = 3  # seconds
    for i in range(number_of_reads):
        val = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
        if val == (None, None):
            sys.exit(1)
        f_val = '{0:0.1f} {1:0.1f}'.format(val[1], val[0])
        print >> sys.stderr, "measure {}: {}".format(i + 1, f_val)
        sleep(pause_between_reads)
    print f_val


if __name__ == '__main__':
    main()
