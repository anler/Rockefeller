

class OpenExchangeRates(object):

    api_endpoint = '{protocol}://openexchangerates.org/api/{endpoint}'

    def __init__(self, app_id, use_https=False):
        self.app_id = app_id
        self.use_https = use_https

    def get_url(self, endpoint):
        protocol = 'https' if self.use_https else 'http'
        if not endpoint.endswith('.json'):
            endpoint += '.json'
        return self.api_endpoint.format(protocol=protocol, endpoint=endpoint)

    def latest(self, **params):
        params.update(app_id=self.app_id)
        self.get_url('latest')

    def currencies(self, **params):
        params.update({'app_id': self.app_id})
        self.get_url('currencies')
