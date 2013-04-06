import decimal

import mock

from rockefeller.services import OpenExchangeRates


class TestOpenExchangeRates:
    def test_http(self):
        s = OpenExchangeRates(app_id='', use_https=False)
        assert 'http' in s.get_url('')
        assert 'https' not in s.get_url('')

    def test_https(self):
        s = OpenExchangeRates(app_id='', use_https=True)
        assert 'https' in s.get_url('')

    def test_endpoint(self):
        s = OpenExchangeRates(app_id='')
        assert 'endpoint.json' in s.get_url('endpoint')
        assert 'endpoint.json' in s.get_url('endpoint.json')

    def test_latest(self):
        s = OpenExchangeRates(app_id='123')
        s.get_url = mock.Mock()
        s.url_opener.open = mock.Mock(return_value={'base': '', 'rates': {}})
        # if we don't consume all the generator the assertion doesn't works
        list(s.latest())

        assert s.get_url.called
        assert s.url_opener.open.called

    def test_result(self):
        s = OpenExchangeRates(app_id='123')
        s.get_url = mock.Mock()
        s.url_opener.open = mock.Mock(
            return_value={'base': 'USD', 'rates': {'EUR': '0.78'}})

        usd_clp, = list(s.latest())

        assert usd_clp.code_from == 'USD'
        assert usd_clp.code_to == 'EUR'
        assert usd_clp.rate == decimal.Decimal('0.78')
