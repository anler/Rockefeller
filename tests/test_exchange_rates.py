# coding: utf-8
import decimal

import mock

import rockefeller
import rockefeller.gae.exchange_rates


def setup_module(module):
    module.usd = rockefeller.Currency(name='United States Dollar',
                                      code='USD', numeric='840',
                                      symbol=u'$', exponent=2).support()
    module.eur = rockefeller.Currency(name='Euro',
                                      code='EUR', numeric='978',
                                      symbol=u'€', exponent=2).support()


class TestExchangeRates:
    def test_add_exchange_rate(self):
        er = rockefeller.ExchangeRates(store=mock.Mock())
        er.add_exchange_rate(base_currency=usd, currency=eur,
                             exchange_rate=1.0)

        er.store.add_exchange_rate.assert_called_once_with(usd, eur, '1.0')

    def test_get_exchange_rate(self):
        er = rockefeller.ExchangeRates(store=mock.Mock())
        er.store.get_exchange_rate.return_value = 1.0
        rate = er.get_exchange_rate(base_currency=usd, currency=eur)

        er.store.get_exchange_rate.assert_called_once_with(usd, eur)
        assert rate == 1.0

    def test_get_exchange_equivalent(self):
        er = rockefeller.ExchangeRates(store=mock.Mock())
        er.store.get_exchange_rate.return_value = None
        rate = er.get_exchange_rate(base_currency=usd, currency=eur)

        assert er.store.get_exchange_rate.call_count == 2
        er.store.get_exchange_rate.assert_called_with(eur, usd)
        assert rate is None


class TestExchangeRate:
    def test_rate_as_decimal(self):
        er = rockefeller.ExchangeRate(usd, eur, .78)
        assert isinstance(er.rate, decimal.Decimal)


class TestMemoryExchangeRates:
    def test_add_get_exchange_rate(self):
        st = rockefeller.MemoryExchangeRates()
        st.add_exchange_rate(usd, eur, 1.0)

        assert st.get_exchange_rate(
            rockefeller.Currency.USD, rockefeller.Currency.EUR) == 1.0

    def test_not_stored_exchange_rate(self):
        st = rockefeller.MemoryExchangeRates()

        assert st.get_exchange_rate(
            rockefeller.Currency.USD, rockefeller.Currency.EUR) is None


class TestGAEExchangeRates:
    def test_add_exchange_rate(self):
        st = rockefeller.gae.exchange_rates.GAEExchangeRates(mock.Mock())
        st.add_exchange_rate(usd, eur, 1.0)

        st.model.add_exchange_rate.assert_called_once_with(usd, eur, 1.0)

    def test_get_exchange_rate(self):
        st = rockefeller.gae.exchange_rates.GAEExchangeRates(mock.Mock())
        st.get_exchange_rate(usd, eur)

        st.model.get_exchange_rate.assert_called_once_with(usd, eur)

    def test_exchange_rate_same_currency(self):
        st = rockefeller.gae.exchange_rates.GAEExchangeRates(mock.Mock())

        assert decimal.Decimal(1) == st.get_exchange_rate(eur, eur)
