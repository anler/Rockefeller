# -*- coding: utf-8 -*-
from .exchange_rates import (ExchangeRate, ExchangeRates, MemoryExchangeRates,
                             exchange_rates, add_exchange_rate,
                             remove_exchange_rate, get_exchange_rate)
from .currency import Currency, MemoryCurrency
from .money import Money, round_amount
from .exceptions import ExchangeError, MoneyError


def set_currency_store(store):
    Currency.store = store


def set_exchange_rates_store(store):
    exchange_rates.store = store


__all__ = ['add_exchange_rate', 'get_exchange_rate', 'Currency', 'Money',
           'ExchangeRates', 'MemoryExchangeRates', 'MemoryCurrency',
           'set_currency_store', 'set_exchange_rates_store', 'round_amount']

__title__ = 'rockefeller'
__version__ = '1.2.0'
