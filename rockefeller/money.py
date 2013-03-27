from collections import namedtuple

from .exchange_rates import get_exchange_rate


class Money(namedtuple('Money', 'amount currency')):
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.amount == other.amount and self.currency == other.currency)

    def exchange_to(self, currency):
        rate = get_exchange_rate(self.currency, currency)
        if rate:
            return self.__class__(amount=self.amount * rate, currency=currency)
