# -*- coding: utf-8 -*-
import logging
try:
    from urllib.request import BaseHandler
except ImportError:
    from urllib2 import BaseHandler


class LoggingHandler(BaseHandler):
    def __init__(self, name=None, level=None):
        if name is None:
            name = __name__
        if level is None:
            level = logging.INFO
        self.logger = logging.getLogger(name)
        self.level = level

    def log(self, line, headers):
        self.logger.log(self.level, '\n'.join((line, headers)))

    def request_line(self, method, url, version):
        return '{method} {url} HTTP/{version}'.format(method=method, url=url,
                                                      version=version)

    def response_line(self, version, status, msg):
        return 'HTTP/{version} {status} {msg}'.format(version=version,
                                                      status=status, msg=msg)

    def headers(self, headers):
        return '\n'.join('{}: {}'.format(h, v) for h, v in headers) + '\n'

    def http_request(self, request):
        request_line = self.request_line(request.get_method(),
                                         request.get_full_url(), '1.X')
        headers = self.headers(request.header_items())
        self.log(request_line, headers)
        return request

    def http_response(self, request, response):
        response_line = self.response_line('1.X', response.code, response.msg)
        headers = self.headers(response.headers.dict.iteritems())
        self.log(response_line, headers)
        return response


def basic_config_logging_handler(name='rockefeller.services'):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
