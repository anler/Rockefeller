# -*- coding: utf-8 -*-

class ExchangeError(Exception):
    """Exception raised when converting between currencies using a not
    supported exchange rate.
    """


class MoneyError(Exception):
    """Exception raised when a Money object is in a not usable state."""
