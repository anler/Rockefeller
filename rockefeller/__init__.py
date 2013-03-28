from .exchange_rates import (ExchangeRates, MemoryExchangeRates,
                             exchange_rates, add_exchange_rate,
                             get_exchange_rate)
from .currency import Currency, MemoryCurrency
from .money import Money


def set_currency_store(store):
    Currency.store = store


def set_exchange_rates_store(store):
    exchange_rates.store = store


__all__ = ['add_exchange_rate', 'get_exchange_rate', 'Currency', 'Money',
           'ExchangeRates', 'MemoryExchangeRates', 'MemoryCurrency',
           'set_currency_store', 'set_exchange_rates_store']
