# coding: utf-8
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

    def test_exponent_rounding(self):
        usd = rockefeller.Money(amount=100.235,
                                currency=rockefeller.Currency.USD)
        clp = rockefeller.Money(amount=60551.984324,
                                currency=rockefeller.Currency.CLP)

        assert 100.24 == float(usd)
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

    def test_exchange_indirectional(self):
        rockefeller.Money.indirection_currency = rockefeller.Currency.USD
        eur = rockefeller.Money(amount=100, currency=rockefeller.Currency.EUR)
        clp = rockefeller.Money(amount=60551,
                                currency=rockefeller.Currency.CLP)

        exchange = eur.exchange_to(rockefeller.Currency.CLP)
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
