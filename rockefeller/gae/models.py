from google.appengine.ext import ndb
from .. import currency


class Currency(ndb.Model):
    name = ndb.StringProperty(required=True)
    code = ndb.StringProperty(required=True)
    numeric = ndb.IntegerProperty(required=True)
    exponent = ndb.IntegerProperty(required=True)
    symbol = ndb.StringProperty(required=True)

    @classmethod
    def get_key(cls, code):
        return ndb.Key(cls, code)

    @classmethod
    def get(cls, code):
        obj = cls.get_key(code).get()
        if obj:
            return currency.Currency(**obj.to_dict())
        return None

    @classmethod
    def support(cls, currency):
        obj = cls(key=cls.get_key(currency.code), **currency._asdict())
        obj.put()

    @classmethod
    def not_support(cls, currency):
        cls.get_key(currency.code).delete()


class ExchangeRate(ndb.Model):
    base_currency = ndb.StringProperty(required=True)
    currency = ndb.StringProperty(required=True)
    exchange_rate = ndb.StringProperty(required=True)

    @classmethod
    def get_key(cls, base_currency, currency):
        key = '{}_{}'.format(hash(base_currency), hash(currency))
        return ndb.Key(cls, key)

    @classmethod
    def add_exchange_rate(cls, base_currency, currency, exchange_rate):
        obj = cls(key=cls.get_key(base_currency, currency),
                  base_currency=base_currency.code, currency=currency.code,
                  exchange_rate=exchange_rate)
        obj.put()

    @classmethod
    def remove_exchange_rate(cls, base_currency, currency):
        cls.get_key(base_currency, currency).delete()

    @classmethod
    def get_exchange_rate(cls, base_currency, currency):
        obj = cls.get_key(base_currency, currency).get()
        if obj:
            return obj.exchange_rate
        return None
