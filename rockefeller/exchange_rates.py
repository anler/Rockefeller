# -*- coding: utf-8 -*-
import decimal
from collections import namedtuple


class ExchangeRate(namedtuple('ExchangeRate', 'code_from code_to rate')):
    """Class for creating exchange rate objects. An exchange rate object
    stores the ``rate`` between two currency codes.

    Initialization params:

        ``code_from``
            Code of currency used as the base.

        ``code_to``
            Code of currency used as the target.

        ``rate``
            Exchange rate between currency codes. numeric or string.
    """
    def __new__(cls, code_from, code_to, rate):
        if not isinstance(rate, decimal.Decimal):
            rate = decimal.Decimal(str(rate))
        return super(ExchangeRate, cls).__new__(cls, code_from, code_to, rate)


class ExchangeRates(object):
    def __init__(self, store):
        self.store = store

    def add_exchange_rate(self, base_currency, currency, exchange_rate):
        """Store an exchange rate between two currencies.

        :param base_currency: Currency to use as base.
        :param currency: Currency to use as target.
        :param exchange_rate: Exchange rate between ``base_currency`` and
            ``currency``.
        """
        self.store.add_exchange_rate(base_currency, currency,
                                     str(exchange_rate))

    def remove_exchange_rate(self, base_currency, currency):
        """Remove an exchange rate between two currencies.

        :param base_currency: Currency to use as base.
        :param currency: Currency to use as target.
        :param exchange_rate: Exchange rate between ``base_currency`` and
            ``currency``.
        """
        self.store.remove_exchange_rate(base_currency, currency)

    def get_exchange_rate(self, base_currency, currency):
        """Get exchange rate of a currency relatively to another one.

        If rate for ``currency`` relatively to ``base_currency`` can't be
        found the rate for ``base_currency`` relatively to ``currency`` will
        be searched and if it's found rate is going to be its inverse.

        :param base_currency: Currency used as the base.
            :class:`~rockefeller.currency.Currency` instance.
        :param currency: Currency you want to know its exchange rate in
            relation to ``base_currency``.
            :class:`~rockefeller.currency.Currency` instance.

        :return: Exchange rate as a ``decimal``.
        """
        rate = self.store.get_exchange_rate(base_currency, currency)
        if rate is None:
            inverse = self.store.get_exchange_rate(currency, base_currency)
            if inverse:
                rate = decimal.Decimal(1) / decimal.Decimal(inverse)
        else:
            rate = decimal.Decimal(str(rate))

        return rate


class MemoryExchangeRates(object):

    def __init__(self):
        self.rates = {}

    def _get_key(self, base_currency, currency):
        return hash(base_currency), hash(currency)

    def add_exchange_rate(self, base_currency, currency, exchange_rate):
        """Store exchange rate of one currency relatively to another one.

        :param base_currency: Currency used as the base.
            :class:`~rockefeller.currency.Currency` instance.
        :param currency: Currency you want to know its exchange rate in
            relation to ``base_currency``.
            :class:`~rockefeller.currency.Currency` instance.
        :param exchange_rate: Exchange rate as a string. :class:`str` instance.
        """
        self.rates[self._get_key(base_currency, currency)] = exchange_rate

    def remove_exchange_rate(self, base_currency, currency):
        """Remove exchange rate of one currency relatively to another one.

        If an exchange rate between ``base_currency`` and ``currency`` can't be
        found is going to try to find a rate between ``currency`` and
        ``base_currency``.

        :param base_currency: Currency used as the base.
            :class:`~rockefeller.currency.Currency` instance.
        :param currency: Currency you want to know its exchange rate in
            relation to ``base_currency``.
            :class:`~rockefeller.currency.Currency` instance.
        """
        self.rates.pop(self._get_key(base_currency, currency), None)
        self.rates.pop(self._get_key(currency, base_currency), None)

    def get_exchange_rate(self, base_currency, currency):
        """Get exchange rate of a currency relatively to another one.

        :param base_currency: Currency used as the base.
            :class:`~rockefeller.currency.Currency` instance.
        :param currency: Currency you want to know its exchange rate in
            relation to ``base_currency``.
            :class:`~rockefeller.currency.Currency` instance.

        :return: Exchange rate as a string. :class:`str` instance.
        """
        return self.rates.get(self._get_key(base_currency, currency))

exchange_rates = ExchangeRates(store=MemoryExchangeRates())
add_exchange_rate = exchange_rates.add_exchange_rate
remove_exchange_rate = exchange_rates.remove_exchange_rate
get_exchange_rate = exchange_rates.get_exchange_rate
