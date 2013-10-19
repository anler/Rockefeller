# -*- coding: utf-8 -*-
from rockefeller.utils import LoggingHandler


class TestLoggingHandler:
    def test_logger_name(self):
        h = LoggingHandler('logs')
        assert 'logs' == h.logger.name

    def test_logger_default_name(self):
        h = LoggingHandler()
        assert 'rockefeller.utils' == h.logger.name
