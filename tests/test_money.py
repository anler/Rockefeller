# coding: utf-8
import decimal

import pytest

import rockefeller


def setup_module(module):
    rockefeller.Currency(name='United States Dollar', code='USD', numeric=840,
                         symbol=u'$', exponent=2).support()
    rockefeller.Currency(name='Euro', code='EUR', numeric=978, symbol=u'€',
                         exponent=2).support()
    rockefeller.Currency(name='Chilean Peso', code='CLP', numeric=152,
                         symbol=u'$', exponent=0).support()

    rockefeller.add_exchange_rate(rockefeller.Currency.USD,
                                  rockefeller.Currency.EUR,
                                  exchange_rate=.78)
    rockefeller.add_exchange_rate(rockefeller.Currency.USD,
                                  rockefeller.Currency.CLP,
                                  exchange_rate=472.30)


class TestMoney:
    def test_as_float(self):
        usd = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        assert 100.00 == float(usd)

    def test_as_float_invalid_currency(self):
        usd = rockefeller.Money(amount=100, currency=None)

        with pytest.raises(rockefeller.MoneyError):
            float(usd)

    def test_exponent_rounding(self):
        usd = rockefeller.Money(amount=100.235,
                                currency=rockefeller.Currency.USD)
        clp = rockefeller.Money(amount=60551.984324,
                                currency=rockefeller.Currency.CLP)

        assert decimal.Decimal('100.235') == usd.amount
        assert 100.24 == float(usd)

        assert decimal.Decimal('60551.984324') == clp.amount
        assert 60552 == float(clp)

    def test_representation(self):
        usd = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)
        eur = rockefeller.Money(amount=78, currency=rockefeller.Currency.EUR)

        assert u'€78' == unicode(eur)
        assert u'$100' == unicode(usd)

    def test_exchange_to(self):
        usd = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)
        eur = rockefeller.Money(amount=78, currency=rockefeller.Currency.EUR)

        exchange = usd.exchange_to(rockefeller.Currency.EUR)
        assert exchange == eur

    def test_exchange_to_not_set(self):
        rockefeller.Money.indirection_currency = None
        usd = rockefeller.Money(amount=100, currency=rockefeller.Currency.EUR)

        with pytest.raises(rockefeller.exceptions.ExchangeError):
            exchange = usd.exchange_to(rockefeller.Currency.CLP)

    def test_exchange_indirectional(self):
        rockefeller.Money.indirection_currency = rockefeller.Currency.USD
        eur = rockefeller.Money(amount=100, currency=rockefeller.Currency.EUR)
        clp = rockefeller.Money(amount=60551,
                                currency=rockefeller.Currency.CLP)

        exchange = eur.exchange_to(rockefeller.Currency.CLP)
        assert exchange == clp

    def test_exchange_indirectional_param(self):
        eur = rockefeller.Money(amount=100, currency=rockefeller.Currency.EUR)
        clp = rockefeller.Money(amount=60551,
                                currency=rockefeller.Currency.CLP)

        exchange = eur.exchange_to(rockefeller.Currency.CLP,
                                   indirection_currency=rockefeller.Currency.USD)
        assert exchange == clp

    def test_equality(self):
        usd1 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)
        usd2 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        assert usd1 == usd2

        usd1 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)
        usd2 = rockefeller.Money(amount=100, currency=rockefeller.Currency.EUR)

        assert usd1 != usd2

        usd1 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)
        usd2 = rockefeller.Money(amount=78, currency=rockefeller.Currency.USD)

        assert usd1 != usd2

    def test_addition(self):
        usd1 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)
        usd2 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        assert rockefeller.Money(200, rockefeller.Currency.USD) == usd1 + usd2

    def test_unsupported_addition(self):
        usd1 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        with pytest.raises(TypeError):
            usd1 + 100

    def test_substraction(self):
        usd1 = rockefeller.Money(amount=90, currency=rockefeller.Currency.USD)
        usd2 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        assert rockefeller.Money(-10, rockefeller.Currency.USD) == usd1 - usd2

    def test_unsupported_substraction(self):
        usd1 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        with pytest.raises(TypeError):
            usd1 - 100

    def test_substraction_saturating(self):
        usd1 = rockefeller.Money(amount=90, currency=rockefeller.Currency.USD)
        usd2 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        assert rockefeller.Money(0, rockefeller.Currency.USD) == usd1.remove(usd2)
        assert rockefeller.Money(10, rockefeller.Currency.USD) == usd2.remove(usd1)

    def test_multiplication(self):
        usd1 = rockefeller.Money(amount=10, currency=rockefeller.Currency.USD)
        usd2 = rockefeller.Money(amount=10, currency=rockefeller.Currency.USD)

        assert rockefeller.Money(100, rockefeller.Currency.USD) == usd1 * usd2

    def test_unsupported_multiplication(self):
        usd1 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        with pytest.raises(TypeError):
            usd1 * 100

    def test_division(self):
        usd1 = rockefeller.Money(amount=10, currency=rockefeller.Currency.USD)
        usd2 = rockefeller.Money(amount=10, currency=rockefeller.Currency.USD)

        assert rockefeller.Money(1, rockefeller.Currency.USD) == usd1 / usd2

    def test_unsupported_division(self):
        usd1 = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)

        with pytest.raises(TypeError):
            usd1 / 100
