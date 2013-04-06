import urllib
import urllib2
import json

from .utils import LoggingHandler

try:
    import requests
except ImportError:
    requests = None

try:
    from google.appengine.api import urlfetch
except ImportError:
    urlfetch = None


class DefaultOpener(object):
    opener = urllib2.build_opener(LoggingHandler(__name__))

    def open(self, url, params):
        if not url.endswith('?'):
            url += '?'
        url += urllib.urlencode(params)
        try:
            response = self.opener.open(url)
        except urllib2.HTTPError as e:
            response = e

        return json.load(response)

