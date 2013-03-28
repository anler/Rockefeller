

class GAEExchangeRates(object):

    def __init__(self, model):
        self.model = model

    def add_exchange_rate(self, base_currency, currency, exchange_rate):
        self.model.add_exchange_rate(base_currency, currency, exchange_rate)

    def get_exchange_rate(self, base_currency, currency):
        return self.model.get_exchange_rate(base_currency, currency)
