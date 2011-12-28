import sys
import requests
from urlparse import urljoin

from tweepy import TweepyError
from tweepy.parsers import default_json_parser

class Client(object):

    def __init__(self,
        auth=None,
        host='api.twitter.com',
        secure=True,
        api_version='1',
        parser=default_json_parser,
        response_format='json'):
        """
        auth: a tuple that takes the format: (auth_mode, param_1, param_2, ..., param_n)
              Supported modes: OAuth, Basic
        host: hostname of the API server. Defaults to api.twitter.com
        secure: if true uses HTTPS for network requests to the API server. Default is true.
        api_version: which version of the API to use. Defaults to 1.
        parser: an instance of the parser which extends the Parser class.
                By default the JSONParser is used with default configurations.
        response_format: the response format to request. Ex: json(default), xml, rss, atom
                         The parser must support the selected response format.
        """
        self.base_url = '%s://%s/%s/' % ('https' if secure else 'http', host, api_version)

        if isinstance(auth, tuple):
            self.session = requests.session(auth=auth)
        else:
            self.session = requests

        # Make sure parser supports response format.
        if response_format not in getattr(parser, 'accepted_formats', ['json']):
            raise TweepyError('Parser does not support the response format %s' % response_format)
        self.parser = parser
        self.response_format = response_format

    def request(self, method, url, parameters=None):
        """Send a request to API server.

        method: type of HTTP method to send (ex: GET, DELETE, POST)
        url: API endpoint URL minus the /<version> part.
        parameters: API parameters to be sent with the request.
        """
        url = '%s.%s' % (urljoin(self.base_url, url), self.response_format)

        try:
            r = self.session.request(method, url, params=dict(parameters))
        except requests.exceptions.RequestException, e:
            raise TweepyError('Request error: %s' % e)

        if r.status_code != 200:
            error_msg = self.parser.parse_error(r.content)
            raise TweepyError('API error: %s' % error_msg)

        if self.parser and len(r.content) > 0:
            return self.parser.parse_content(r.content)
        else:
            return r.content

    def home_timeline(self, **parameters):
        """GET statuses/home_timeline"""
        return self.request('GET', 'statuses/home_timeline', paramters)

    def mentions(self, **parameters):
        """GET statuses/mentions"""
        return self.request('GET', 'statuses/mentions', parameters)

    def public_timeline(self, **parameters):
        """GET statuses/public_timeline"""
        return self.request('GET', 'statuses/public_timeline', parameters)

    def retweeted_by_me(self, **parameters):
        """GET statuses/retweeted_by_me"""
        return self.request('GET', 'statuses/retweeted_by_me', parameters)

    def retweeted_to_me(self, **parameters):
        """GET statuses/retweeted_to_me"""
        return self.request('GET', 'statuses/retweeted_to_me', parameters)

    def retweets_of_me(self, **parameters):
        """GET statuses/retweets_of_me"""
        return self.request('GET', 'statuses/retweets_of_me', parameters)

    def user_timeline(self, screen_name=None, user_id=None, **parameters):
        """GET statuses/user_timeline"""
        parameters.update({'screen_name': screen_name, 'user_id': user_id})
        return self.request('GET', 'statuses/user_timeline', parameters)

    def retweeted_to_user(self, id=None, screen_name=None, **parameters):
        """GET statuses/retweeted_to_user"""
        parameters.update({'id': id, 'screen_name': screen_name})
        return self.request('GET', 'statuses/retweeted_to_user', parameters)

    def update_status(self, status, **parameters):
        """POST statuses/update"""
        parameters.update({'status': status})
        return self.request('POST', 'statuses/update', parameters)

