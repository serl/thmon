#!/usr/bin/python

from libs.parse import Parse
import config, sys, os
from datetime import datetime
os.chdir(os.path.dirname(sys.argv[0])) # so that workdir = this dir

parse = Parse(config.application_id, config.rest_api_key)
parse.set_session_token(config.session_token)

me = parse.call('users/me')
if 'error' in me:
	print "Config not valid: {}".format(me['error'])
	sys.exit(1)

cached = [int(f) for f in os.listdir('./cache') if f.isdigit()]
for timestamp in cached:
	contents = ''
	filename = './cache/{}'.format(timestamp)
	with open(filename, 'r') as cnts:
		contents = cnts.read().strip()
	(temperature, humidity) = contents.split(' ')
	isodate = datetime.utcfromtimestamp(timestamp).isoformat()
	insert_response = parse.call(
		'classes/Measure',
		'POST',
		{
			'value': { 'temp': temperature, 'rh': humidity },
			'timestamp': { '__type': 'Date', 'iso': isodate },
			'sensor': { '__type': 'Pointer', 'className': 'Sensor', 'objectId': config.sensor}
		}
	)
	if 'error' in insert_response:
		print "Error uploading data: {}".format(insert_response['error'])
		sys.exit(1)
	os.remove(filename)
