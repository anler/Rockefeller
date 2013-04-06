from .exchange_rates import ExchangeRate
from .openers import DefaultOpener


class OpenExchangeRates(object):
    """Interface to openexchangerates.org service.

    Initialization params:
        `app_id`
            Your account `app_id`

        `use_https`
            Defaults to `False`. Whether or not use https as the protocol.
    """
    api_endpoint = '{protocol}://openexchangerates.org/api/{endpoint}'
    url_opener = DefaultOpener()

    def __init__(self, app_id, use_https=False):
        self.app_id = app_id
        self.use_https = use_https

    def get_url(self, endpoint):
        protocol = 'https' if self.use_https else 'http'
        if not endpoint.endswith('.json'):
            endpoint += '.json'
        return self.api_endpoint.format(protocol=protocol, endpoint=endpoint)

    def latest(self, **params):
        """Get latest exchange rates.

        :param \*\*params: Get params passed to the service.

        :return: Generator object. Each yielded value is a
            :class:`rockefeller.exchange_rates.ExchangeRate` instance.
        """
        params.update(app_id=self.app_id)
        rates = self.url_opener.open(self.get_url('latest'), params)
        base = rates['base']

        for code, rate in rates['rates'].iteritems():
            yield ExchangeRate(base, code, rate)
