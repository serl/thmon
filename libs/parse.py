import json, httplib, urllib

class Parse:
	def __init__(self, application_id, rest_api_key):
		self.application_id = application_id
		self.rest_api_key = rest_api_key

	def call(self, endpoint, verb='GET', params={}, input_headers={}):
		default_headers = {
			"X-Parse-Application-Id": self.application_id,
			"X-Parse-REST-API-Key": self.rest_api_key
		}
		headers = default_headers.copy()
		headers.update(input_headers)
		if hasattr(self, 'session_token'):
			headers.update({"X-Parse-Session-Token": self.session_token})
		connection = httplib.HTTPSConnection('api.parse.com', 443)
		body = ''
		connection.connect()
		url = '/1/{}'.format(endpoint)
		if verb == 'GET':
			url += '?{}'.format(urllib.urlencode(params))
		else:
			body = json.dumps(params)
			headers.update({"Content-Type": "application/json"})
		connection.request(verb, url, body, headers)
		return json.loads(connection.getresponse().read())

	def login(self, username, password):
		result = self.call(
			'login',
			'GET',
			{"username": username,"password": password},
			{ "X-Parse-Revocable-Session": "1" }
		)
		self.session_token = result['sessionToken']

	def create_session_token(self):
		result = self.call('sessions', 'POST')
		return result['sessionToken']

	def set_session_token(self, session_token):
		self.session_token = session_token
