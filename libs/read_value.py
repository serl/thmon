#!/usr/bin/python

import sys, Adafruit_DHT

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)

if humidity is not None and temperature is not None:
	print 'TEMPERATURE={0:0.1f} HUMIDITY={1:0.1f}'.format(temperature, humidity)
else:
	print 'TEMPERATURE= HUMIDITY='
	sys.exit(1)
