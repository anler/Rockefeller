import pytest
import mock

import rockefeller
import rockefeller.gae.currency


def setup_module(module):
    module.usd = rockefeller.Currency(name='United States Dollar',
                                      code='USD', numeric='840',
                                      symbol=u'$', exponent=2)


class TestCurrency:
    def setup_method(self, method):
        rockefeller.Currency.store = mock.Mock()

    def teardown_method(self, method):
        rockefeller.Currency.store = rockefeller.MemoryCurrency()

    def test_support(self):
        rockefeller.Currency.store = mock.Mock()
        usd.support()

        rockefeller.Currency.store.support.assert_called_once_with(usd)

    def test_get(self):
        rockefeller.Currency.store = mock.Mock()
        rockefeller.Currency.get('EUR')

        rockefeller.Currency.store.get.assert_called_once_with('EUR')

    def test_code_attribute(self):
        rockefeller.Currency.store = mock.Mock()
        rockefeller.Currency.EUR

        rockefeller.Currency.store.get.assert_called_once_with('EUR')

    def test_inmutability(self):
        with pytest.raises(AttributeError):
            usd.code = 'EUR'

    def test_equality(self):
        assert usd == rockefeller.Currency(name='', code='USD', numeric='',
                                           symbol='', exponent=2)

    def test_not_equality(self):
        assert usd != rockefeller.Currency(name='', code='EUR', numeric='',
                                           symbol='', exponent=2)

    def test_string_representation(self):
        assert 'USD' == str(usd)


class TestMemoryCurrency:
    def test_support_get(self):
        st = rockefeller.MemoryCurrency()
        st.support(usd)

        assert st.get('USD') == usd

    def test_not_stored_currency(self):
        st = rockefeller.MemoryCurrency()

        assert st.get('USD') is None


class TestGAECurrency:
    def test_support(self):
        st = rockefeller.gae.currency.GAECurrency(mock.Mock())
        st.support(usd)

        st.model.support.assert_called_once_with(usd)

    def test_get(self):
        st = rockefeller.gae.currency.GAECurrency(mock.Mock())
        st.get('USD')

        st.model.get.assert_called_once_with('USD')
