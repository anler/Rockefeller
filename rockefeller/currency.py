# -*- coding: utf-8 -*-
from collections import namedtuple

from six import add_metaclass


class MemoryCurrency(object):
    __slots__ = 'currencies'

    def __init__(self):
        self.currencies = {}

    def support(self, currency):
        """Store a currency.

        :param currency: :class:`rockefeller.currency.Currency` instance.
        """
        self.currencies[currency.code] = currency

    def not_support(self, currency):
        """Remove a currency support.

        :param currency: :class:`rockefeller.currency.Currency` instance.
        """
        code = currency.code
        if code in self.currencies:
            del self.currencies[code]

    def get(self, code):
        """Get a currency by its code.

        :param code: ISO 4217 currency code.

        :return: :class:`rockefeller.currency.Currency` instance.
        """
        return self.currencies.get(code)


class CurrencyType(type):
    def __getattr__(cls, code):
        return cls.get(code)


@add_metaclass(CurrencyType)
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
    store = MemoryCurrency()

    def __str__(self):
        return self.code

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.code == other.code

    def __hash__(self):
        return int(self.numeric)

    def _get_store(self, store=None):
        """Get the corresponding store.

        :param store: A currency store object.

        :return: If ``store`` param is not ``None`` is returned, otherwise
            ``Currency.store`` is returned.
        """
        if store is None:
            store = self.__class__.store

        return store

    def support(self, store=None):
        """Support/store a currency.

        :param store: Use this store instead of ``Currency.store``.

        :return: ``self`` :class:`~rockefeller.currency.Currency` instance.
        """
        self._get_store(store).support(self)
        return self

    def not_support(self, store=None):
        """Stop supporting a currency.

        :param store: Use this store instead of ``Currency.store``.

        :return: ``self`` :class:`~rockefeller.currency.Currency` instance.
        """
        self._get_store(store).not_support(self)
        return self

    @classmethod
    def get(cls, code):
        return cls.store.get(code)
