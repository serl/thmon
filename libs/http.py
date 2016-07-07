import json, httplib, urllib

class HTTP:
	def __init__(self, default_headers):
		self.default_headers = default_headers.copy()

	def call(self, endpoint, verb='GET', params={}, input_headers={}):
		headers = self.default_headers.copy()
		headers.update(input_headers)
		connection = httplib.HTTPSConnection('api.thingspeak.com', 443)
		body = ''
		connection.connect()
		url = '/{}'.format(endpoint)
		if verb == 'GET':
			url += '?{}'.format(urllib.urlencode(params))
		else:
			body = json.dumps(params)
			headers.update({"Content-Type": "application/json"})
		connection.request(verb, url, body, headers)
		return connection.getresponse().read()
