# -*- coding: utf-8 -*-
import json

try:
    from urllib.parse import urlencode
    from urllib.request import build_opener
    from urllib.error import HTTPError
except ImportError:
    from urllib import urlencode
    from urllib2 import build_opener, HTTPError

try:
    import requests
except ImportError:
    requests = None

try:
    from google.appengine.api import urlfetch
except ImportError:
    urlfetch = None

from .utils import LoggingHandler


class DefaultOpener(object):
    opener = build_opener(LoggingHandler(__name__))

    def open(self, url, params):
        if not url.endswith('?'):
            url += '?'
        url += urlencode(params)
        try:
            response = self.opener.open(url)
        except HTTPError as e:
            response = e

        return json.load(response)


class GaeOpener(object):
    def __new__(cls, *args, **kwargs):
        if urlfetch is None:
            raise ImportError('cannot import name urlfetch')
        return object.__new__(cls, *args, **kwargs)

    def open(self, url, params):
        if not url.endswith('?'):
            url += '?'
        url += urlencode(params)
        response = urlfetch.fetch(url)

        return json.load(response.content)
