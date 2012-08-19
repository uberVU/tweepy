import sys
import unittest

import tweepy
from requests.auth import OAuth1

# OAuth credentials.
CONSUMER = (u'KHKOhs4270N0jTmjRMBVUg', u'RZzjrdI81HLmQxyT4ZfEEEgZwaxFZK9rLuaOOmNM')
ACCESS_TOKEN = (u'82301637-uJyyc4U0cq2qcY5N7l9Iy1n93RHkEzWaZnx2uHZr7',
                u'0zqP7tq8eiH9bVCEUMFbrSRWwTAXLDKVRUEfTIcV68')

class TweepyTestCase(unittest.TestCase):
    def setUp(self):
        auth = OAuth1(CONSUMER[0], CONSUMER[1],
                      ACCESS_TOKEN[0], ACCESS_TOKEN[1])
        self.client = tweepy.Client(auth)

        # Print out each HTTP request to stdout.
        self.client.http.config['verbose'] = sys.stdout

    def assertIsStatus(self, obj):
        self.assertIsInstance(obj['id'], int)
        self.assertIsInstance(obj['id_str'], unicode)
        self.assertIsInstance(obj['text'], unicode)

    def assertIsTimeline(self, obj):
        self.assertIsInstance(obj, list)
        if len(obj) > 0:
            self.assertIsStatus(obj[0])
        else:
            print 'Warning: No timeline object to verify as status.'

class TweepyOAuthTests(TweepyTestCase):
    # Verify request_token() returns a tuple
    # containing the request token and secret.
    def test_request_token(self):
        request_token = self.client.request_token()
        self.assertIs(request_token, tuple)
        self.assertIs(request_token[0], str)
        self.assertIs(request_token[1], str)

    def test_authorize(self):
        url = self.client.authorize(request_token)
        self.assertIs(url, str)

class TweepyAPITests(TweepyTestCase):
    def test_home_timeline(self):
        t = self.client.home_timeline()
        self.assertIsTimeline(t)

    def test_mentions(self):
        t = self.client.mentions()
        self.assertIsTimeline(t)

    def test_retweeted_by_me(self):
        t = self.client.retweeted_by_me()
        self.assertIsTimeline(t)

    def test_retweeted_to_me(self):
        t = self.client.retweeted_to_me()
        self.assertIsTimeline(t)

    def test_retweets_of_me(self):
        t = self.client.retweets_of_me()
        self.assertIsTimeline(t)

    def test_user_timeline(self):
        t = self.client.user_timeline()
        self.assertIsTimeline(t)

        t = self.client.user_timeline('twitter')
        self.assertIsTimeline(t)

    def test_retweeted_to_user(self):
        t = self.client.retweeted_to_user('twitter')
        self.assertIsTimeline(t)

    def test_retweeted_by_user(self):
        t = self.client.retweeted_by_user('twitter')
        self.assertIsTimeline(t)

if __name__ == '__main__':
    unittest.main()

