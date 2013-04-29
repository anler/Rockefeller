import decimal


class GAEExchangeRates(object):

    def __init__(self, model):
        self.model = model

    def add_exchange_rate(self, base_currency, currency, exchange_rate):
        self.model.add_exchange_rate(base_currency, currency, exchange_rate)

    def get_exchange_rate(self, base_currency, currency):
        if base_currency == currency:
            rate = decimal.Decimal(1)
        else:
            rate = self.model.get_exchange_rate(base_currency, currency)
        return rate
