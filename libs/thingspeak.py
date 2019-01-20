"""
ThingSpeak service connector
"""

import json
import httplib
import urllib


class ThingSpeak:

    def __init__(self, channel_id, api_key):
        self.channel_id = channel_id
        self.api_key = api_key

    def _call(self, endpoint, verb='GET', params={}):
        headers = {}
        connection = httplib.HTTPSConnection('api.thingspeak.com', 443, timeout=120)
        body = ''
        connection.connect()
        url = '/channels/{}/{}'.format(self.channel_id, endpoint)
        if verb == 'GET':
            url += '?{}'.format(urllib.urlencode(params))
        else:
            body = json.dumps(params)
            headers.update({"Content-Type": "application/json"})
        connection.request(verb, url, body, headers)
        return connection.getresponse().read()

    def bulk_update(self, updates):
        response = self._call(
            'bulk_update.json',
            'POST',
            {
                'write_api_key': self.api_key,
                'updates': updates
            }
        )
        try:
            return json.loads(response)
        except ValueError:
            return {
                'error': {
                    'message': 'Error parsing JSON response',
                    'details': response
                }
            }
