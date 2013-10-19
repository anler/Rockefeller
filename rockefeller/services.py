# -*- coding: utf-8 -*-
from six import iteritems

from .exchange_rates import ExchangeRate
from .openers import DefaultOpener


class ServiceError(Exception):
    """Raised when the request to the exchange rates service is invalid and
    the service is not able to fullfil it.
    """


class OpenExchangeRates(object):
    """Interface to openexchangerates.org service.

    Initialization params:
        `app_id`
            Your account `app_id`

        `use_https`
            Defaults to `False`. Whether or not use https as the protocol.
    """
    class Results(object):
        def __init__(self, rates):
            self.rates = rates

        def __iter__(self):
            base = self.rates['base']
            rates = self.rates['rates']
            for code, rate in iteritems(rates):
                yield ExchangeRate(base, code, rate)

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
        if not 'base' in rates:
            raise ServiceError(rates.get('description', 'Unknow Error'))
        return self.Results(rates)
