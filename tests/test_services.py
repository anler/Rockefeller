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
        s.get_url = mock.Mock(return_value='http://.../api/latest.json')
        s.latest()

        assert s.get_url.called

    def test_currencies(self):
        s = OpenExchangeRates(app_id='')
        s.get_url = mock.Mock()
        s.currencies()
        assert s.get_url.called
