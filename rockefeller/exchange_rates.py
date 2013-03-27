

class ExchangeRates(object):
    def __init__(self, store):
        self.store = store

    def add_exchange_rate(self, base_currency, currency, exchange_rate):
        self.store.add_exchange_rate(base_currency, currency, exchange_rate)

    def get_exchange_rate(self, base_currency, currency):
        """Get exchange rate of a currency relatively to another one.

        If rate for ``currency`` relatively to ``base_currency`` can't be
        found the rate for ``base_currency`` relatively to ``currency`` will
        be searched and if it's found rate is going to be its inverse.

        :param base_currency: Currency used as the base.
            :class:`~rockefeller.currency.Currency` instance.
        :param currency: Currency you want to know its exchange rate in relation
            to ``base_currency.`` :class:`~rockefeller.currency.Currency` instance.

        :return: Exchange rate as a ``float.``
        """
        rate = self.store.get_exchange_rate(base_currency, currency)
        if rate is None:
            inverse = self.store.get_exchange_rate(currency, base_currency)
            if inverse:
                rate = 1.0 / inverse
        return rate


class MemoryExchangeRates(object):
    __slots__ = 'rates'

    def __init__(self):
        self.rates = {}

    def _get_key(self, base_currency, currency):
        return hash(base_currency), hash(currency)

    def add_exchange_rate(self, base_currency, currency, exchange_rate):
        print base_currency, currency, exchange_rate
        self.rates[self._get_key(base_currency, currency)] = exchange_rate

    def get_exchange_rate(self, base_currency, currency):
        return self.rates.get(self._get_key(base_currency, currency))

exchange_rates = ExchangeRates(store=MemoryExchangeRates())
add_exchange_rate = exchange_rates.add_exchange_rate
get_exchange_rate = exchange_rates.get_exchange_rate
