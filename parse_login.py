#!/usr/bin/python

from libs.parse import Parse

#compatibility with Python 3, but I really don't know if everything else works :D
try:
	input = raw_input
except NameError:
	pass

print "We'll configure this piece of software to write directly on Parse."
application_id = input("I need the application id: ")
rest_api_key = input("And the rest api key: ")

instance = Parse(application_id, rest_api_key)

print "Now we'll log in and forge a session token for the sensor."
username = input("App username: ")
password = input("App password: ")

instance.login(username, password)
print "Login successful, now creating IoT token..."
restricted_session_token = instance.create_session_token()

print "Writing everything on the configuration file"
with open('config.py', 'w') as configfile:
	configfile.write("application_id='{}'\nrest_api_key='{}'\nsession_token='{}'\n".format(application_id, rest_api_key, restricted_session_token))
print "Done"
