from tweepy import TweepyError

try:
    import simplejson as json
except ImportError, e:
    import json

class Parser(object):

    def parse_content(self, content):
        """Parse the response content and return the a result."""
        raise NotImplementedError

    def parse_error(self, content):
        """Parse the error response and return a message describing it."""
        raise NotImplementedError

    def supports_format(self, response_format):
        """Determine if this parse supports the given response format.

        response_format -- The format this parser may support.

        Returns: True if the format is supported.
        """
        return False

class JSONParser(Parser):
    """Deserializes JSON responses into Python objects."""

    def parse_content(self, content):
        try:
            result = json.loads(content)
        except ValueError, e:
            raise TweepyError('JSON parse error: %s\nJSON content:\n%s' % (e, content))

        return result

    def parse_error(self, content):
        try:
            error = json.loads(content)
        except Exception, e:
            return content
        return error.get('error', 'Unknown: %s' % content)

    def supports_format(self, response_format):
        return response_format == 'json'

