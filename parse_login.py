#!/usr/bin/python

from libs.parse import Parse
os.chdir(os.path.dirname(sys.argv[0])) # so that workdir = this dir

config = object()
try:
	import config
except:
	pass

#compatibility with Python 3, but I really don't know if everything else works :D
try:
	input = raw_input
except NameError:
	pass

if not (hasattr(config, 'application_id') and hasattr(config, 'rest_api_key')):
	print "We'll configure this piece of software to write directly on Parse."
	config.application_id = input("I need the application id: ")
	config.rest_api_key = input("And the rest api key: ")

parse = Parse(config.application_id, config.rest_api_key)

if not (hasattr(config, "session_token")):
	print "Now we'll log in and forge a session token for the sensor."
	username = input("App username: ")
	password = input("App password: ")

	parse.login(username, password)
	print "Login successful, now creating IoT token..."
	config.session_token = parse.create_session_token()
else:
	parse.set_session_token(config.session_token)

me = parse.call('users/me')

sensor_name = input("Sensor name: ")
sensor_create_response = parse.call(
	'classes/Sensor',
	'POST',
	{
		'name': sensor_name,
		'owner': { '__type': 'Pointer', 'className': '_User', 'objectId': me['objectId'] }
	}
)
config.sensor = sensor_create_response['objectId']

print "Writing everything on the configuration file"
with open('config.py', 'w') as configfile:
	configfile.write("application_id='{}'\nrest_api_key='{}'\nsession_token='{}'\nsensor='{}'\n".format(config.application_id, config.rest_api_key, config.session_token, config.sensor))
print "Done"
