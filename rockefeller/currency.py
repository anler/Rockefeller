from collections import namedtuple


class MemoryCurrency(object):
    __slots__ = 'currencies'

    def __init__(self):
        self.currencies = {}

    def support(self, currency):
        self.currencies[currency.code] = currency

    def get(self, code):
        return self.currencies.get(code)


class CurrencyType(type):
    def __getattr__(cls, code):
        return cls.get(code)


class Currency(namedtuple('Currency', 'name code numeric exponent symbol')):
    """The currency objects factory.

    Currency objects keeps track of several information associated to the
    currency.

    Initialization params:

        `name`
            Name of the currency. For example: "Euro"

        `code`
            Alpha code of the currency in the ISO 4217.

        `numeric`
            Numeric code of the currency in the ISO 4217. As an ``int``.
            This value is used as the return value for __hash__ method so
            you can use instances as dictionary keys.

        `exponent`
            Currency exponent (number of digits after the decimal separator).
            As an ``int``.

        `symbol`
            Currency unicode symbol. For currencies without a symbol just use
            empty string ``''``.
    """
    __metaclass__ = CurrencyType
    store = MemoryCurrency()

    def __str__(self):
        return self.code

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.code == other.code

    def __hash__(self):
        return int(self.numeric)

    def support(self):
        Currency.store.support(self)
        return self

    @classmethod
    def get(cls, code):
        return cls.store.get(code)
