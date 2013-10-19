# -*- coding: utf-8 -*-
from __future__ import division
import decimal
from collections import namedtuple

from six import PY3

from .exchange_rates import get_exchange_rate
from .exceptions import ExchangeError, MoneyError


def round_amount(amount, currency):
    """Round a given amount using curreny's exponent.

    :param amount: :class:`~decimal.Decimal` number.
    :param currency: :class:`~rockefeller.currency.Currency` object.

    :return: Rounded amount as a :class:`~decimal.Decimal` number.

    :raises: :class:`~rockefeller.exceptions.MoneyError` if an invalid currency
        is supplied.
    """
    try:
        exponent = currency.exponent
    except AttributeError:
        raise MoneyError('Wrong currency `{!r}` for money.'.format(currency))
    exponent = '1.' + '0' * currency.exponent
    return amount.quantize(decimal.Decimal(exponent), rounding=decimal.ROUND_HALF_UP)


def to_decimal(value):
    """Convert a value into a decimal value.

    :param value: Any value that can be casted into a numeric string.

    :return: Decimal value. :class:`~decimal.Decimal` instance.
    """
    if not isinstance(value, decimal.Decimal):
        value = decimal.Decimal(str(value))
    return value


def _check_operand(operation, operand):
    if not isinstance(operand, Money):
        msg = "unsupported operand type(s) for %s: 'Money' and '%r'" % (
            operation, operand.__class__)
        raise TypeError(msg)


class Money(namedtuple('Money', 'amount currency')):
    """Representation of money.

    Every `Money` objects has an amount and a currency associated to it and the amount is always a
    :class:`~decimal.Decimal` value.

    Initialization params:

        `amount`
            Amount of money.

        `currency`
            Money currency. :class:`~rockefeller.currency.Currency` instance.
    """
    indirection_currency = None

    def __new__(cls, amount, currency):
        return super(Money, cls).__new__(cls, to_decimal(amount), currency)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.amount == other.amount and self.currency == other.currency)

    def __add__(self, other):
        _check_operand('+', other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        _check_operand('-', other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other):
        _check_operand('*', other)
        return Money(self.amount * other.amount, self.currency)

    def __div__(self, other):
        _check_operand('/', other)
        return Money(self.amount / other.amount, self.currency)
    __floordiv__ = __div__
    __truediv__ = __div__

    def __divmod__(self, other):
        quotient, remainder = divmod(self.amount, other.amount)
        return Money(quotient, self.currency), Money(remainder, self.currency)

    def __float__(self):
        return float(round_amount(self.amount, self.currency))

    def __str__(self):
        value = self.__unicode__()
        if PY3:
            return value
        return value.encode('utf-8')

    def __unicode__(self):
        amount = self.amount
        parts = str(amount).split('.')
        if len(parts) == 2 and int(parts[1]) == 0:
            amount = parts[0]
        return u'{}{}'.format(self.currency.symbol, amount)

    def remove(self, other):
        result = self - other
        if result.amount < 0:
            result = Money(0, self.currency)
        return result

    def get_exchange_rate_to(self, currency, indirection_currency=None):
        """Get exchange rate of the currency of this money relatively to
        ``currency``.

        :param currency: Output currency.
            :class:`~rockefeller.currency.Currency` instance.
        :param indirection_currency: Use this currency as the indirection
            currency. :class:`~rockefeller.currency.Currency` instance.

        :return: Exchange rate as a ``decimal`` if found, else ``None``.
        """
        rate = get_exchange_rate(self.currency, currency)
        if rate is None:
            if not indirection_currency and Money.indirection_currency:
                indirection_currency = Money.indirection_currency
            rate_from_base = get_exchange_rate(self.currency, indirection_currency)
            rate_base_to = get_exchange_rate(indirection_currency, currency)
            if rate_from_base and rate_base_to:
                rate = rate_from_base * rate_base_to

        return rate

    @property
    def rounded_amount(self):
        return round_amount(self.amount, self.currency)

    def exchange_to(self, currency, indirection_currency=None,
                    exchange_rate=None):
        """Convert this money into money of another currency.

        :param currency: Convert this money into this currency.
            :class:`~rockefeller.currency.Currency` instance.
        :param indirection_currency: Use this currency as the indirection
            currency. :class:`~rockefeller.currency.Currency` instance.
        :param exchange_rate: Use this exchange rate instead of trying to find
            one.

        :return: Money in ``currency`` currency.
            :class:`~rockefeller.money.Money` instance.

        :raises: :class:`~rockefeller.exceptions.ExchangeError`
            if Exchange rate bettween currencies is not defined.
        """
        if exchange_rate is None:
            exchange_rate = self.get_exchange_rate_to(
                currency, indirection_currency=indirection_currency)
        else:
            exchange_rate = to_decimal(exchange_rate)

        if exchange_rate is None:
            raise ExchangeError('Exchange rate {}-{} not defined.'.format(
                self.currency, currency))

        amount = round_amount(self.amount * exchange_rate, currency)
        return self.__class__(amount=amount, currency=currency)
