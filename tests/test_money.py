import rockefeller


def setup_module(module):
    rockefeller.Currency(name='United States Dollar', code='USD', numeric=840,
                         symbol=u'$', exponent=2).support()
    rockefeller.Currency(name='Euro', code='EUR', numeric=978, symbol=u'€',
                         exponent=2).support()
    rockefeller.add_exchange_rate(rockefeller.Currency.USD,
                                  rockefeller.Currency.EUR,
                                  exchange_rate=.78)


class TestMoney:
    def test_exchange_to(self):
        usd = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)
        eur = rockefeller.Money(amount=78, currency=rockefeller.Currency.EUR)

        exchange = usd.exchange_to(rockefeller.Currency.EUR)
        assert exchange == eur

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
