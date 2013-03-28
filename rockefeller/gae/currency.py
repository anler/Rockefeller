

class GAECurrency(object):

    def __init__(self, model):
        self.model = model

    def support(self, currency):
        self.model.support(currency)

    def get(self, code):
        return self.model.get(code)
