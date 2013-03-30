Rockefeller
===========

Library for dealing with money and currency conversion in Python. It provides
tools for __storing__ currencies and exchange rates, __converting__ from one
currency to another and __fetching__ exchange rates from different services.

![http://floqq.github.com/Rockefeller/](http://floqq.github.com/Rockefeller/)

Tutorial
--------

### Working with currencies

Currencies are represented by the ``Currency`` class.

``` python
import rockefeller

usd = rockefeller.Currency(name='United States Dollar', code='USD',
                            numeric='840', symbol='$', exponent=2)
str(usd)
# => 'USD'
```


If you want to globally store a currency in your program, you first need to
__support it__.

``` python
import rockefeller

usd = rockefeller.Currency(name='United States Dollar', code='USD',
                            numeric='840', symbol='$', exponent=2)

# You only have access to the currency stored in ``usd`` variable
rockefeller.Currency.USD
# => None

# Globally support the currency (See `setting currency store`)
usd.support()

# Now you can access it directly via the ``Currency`` class
rockefeller.Currency.USD
# => Currency(code='USD', ...)
rockefeller.Currency.get('USD')
# => Currency(code='USD', ...)

usd == rockefeller.Currency.USD
# => True

usd is rockefeller.Currency.USD
# => False
```


### Exchange rates

Exchange rates between currencies are represented through the ``ExchangeRate``
class but you can __add__ and __retrieve__ exchange rates directly like this:

``` python
import rockefeller

eur = rockefeller.Currency(name='Euro', code='EUR', numeric='978',
                            symbol=u'€', exponent=2)
clp = rockefeller.Currency(name='Chilean Peso', code='CLP', numeric='152',
                            symbol='$', exponent=0)

rockefeller.get_exchange_rate(eur, clp)
# => None

# Store exchange rate for EUR => CLP
rockefeller.add_exchange_rate(eur, clp, 604.10)

rockefeller.get_exchange_rate(eur, clp)
# => Decimal('604.10')

# You can also get the inverse even if not explicitly defined
rockefeller.get_exchange_rate(clp, eur)
# => Decimal('0.001655355073663300778016884622')

rate == 604.10
# => False (604.10 doesn't have an exact float representation)

float(rate) == 604.10
# => True
```


### Money

For working with currencies and amounts of it there's the convenient ``Money``
class.

``` python

money = rockefeller.Money(amount=100.235, currency=rockefeller.Currency.USD)
```

#### Money arithmetic

#### Sum

``` python
(rockefeller.Money(100, rockefeller.Currency.USD) + 
    rockefeller.Money(100, rockefeller.Currency.USD))
# => Money(200, rockefeller.Currency.USD)
```

#### Subtraction

``` python
(rockefeller.Money(80, rockefeller.Currency.USD) - 
    rockefeller.Money(100, rockefeller.Currency.USD))
# => Money(-20, rockefeller.Currency.USD)
```

#### Subtraction (saturating)

``` python
rockefeller.Money(80, rockefeller.Currency.USD).remove(
    rockefeller.Money(100, rockefeller.Currency.USD))
# => Money(0, rockefeller.Currency.USD)
```

#### Multiplication

``` python
(rockefeller.Money(10, rockefeller.Currency.USD) * 
    rockefeller.Money(10, rockefeller.Currency.USD))
# => Money(100, rockefeller.Currency.USD)
```

#### Division

``` python
(rockefeller.Money(100, rockefeller.Currency.USD) / 
    rockefeller.Money(100, rockefeller.Currency.USD))
# => Money(1, rockefeller.Currency.USD)
```

#### Float rounding using currency's exponent

``` python
usd_money = rockefeller.Money(amount=100.235, currency=rockefeller.Currency.USD)
clp_money = rockefeller.Money(amount=60551.984324, currency=rockefeller.Currency.CLP)

usd_money.amount
# => Decimal('100.235')

clp_money.amount
# => Decimal('60551.984324')

float(usd_money)
# => 100.24

float(clp_money)
# = > 60552
```

#### String representation

``` python
u'$100.24' == unicode(usd_money)
# => True
```

#### Equality

``` python
usd_money == rockefeller.Money(amount=100.235, currency=rockefeller.Currency.USD)
# => True
```

#### Conversion between currencies

``` python
import rockefeller

usd = rockefeller.Money(amount=100, currency=rockefeller.Currency.USD)
eur = rockefeller.Money(amount=78, currency=rockefeller.Currency.EUR)

rockefeller.add_exchange_rate(usd, eur, .78)

usd.exchange_to(rockefeller.Currency.EUR)
# => Money(78, rockefeller.Currency.EUR)

eur.exchange_to(rockefeller.Currency.USD)
# => Money(100, rockefeller.Currency.USD)
```

#### Conversion between currencies using indirection

Is common that third-party exchange-rate services gives you the rates of each
currency relative to a common one.
Take for example, [openexchangerates.org](https://openexchangerates.org) that
returns all rates relative to __USD Dollars__.

``` javascript
/* latest.json (7 mins ago) */
{
    "timestamp": 1364680868,
    "base": "USD",
    "rates": {
        "AED": 3.6729,
        "AFN": 53.0133,
        "ALL": 109.122501,
        "AMD": 421.240004,
        /* 164 currencies */
        "YER": 214.800258,
        "ZAR": 9.233264,
        "ZMK": 5227.108333,
        "ZMW": 5.3855,
        "ZWL": 322.322775
    }
}
```

Thi is how Rockefeller library works when you try to convert __currency 1__ to
__currency 2__:

1. get_exchange_rate(currency1, currency2)
2. if not found try the inverse: get_exchange_rate(currency2, currency1)
3. if not found, try using the __indirection currency__

The __indirection currency__ is a currency you set as the common/base currency
to which the rest of the currency rates are related.

So, let's say we have the following:

``` python
rockefeller.add_exchange_rate(usd, eur, .78)
rockefeller.add_exchange_rate(usd, clp, 472.03735)
```

And you want to get the exchange rate from __eur__ to __clp__:

``` python
rockefeller.Money(40, eur).exchange_to(clp)
# => None
```

It will be ``None`` since there's no direct relation between __eur -> clp__ or
__clp -> eur__. Of course, this behavior is not desired because storing all the
rates between currencies will require 33,856 associations (taking into account
that there's 184 different currencies).

The workaround to this problem is setting the __indirection currency__ like
this:

``` python
rockefeller.Money.indirection_currency = rockefeller.Currency.USD
```

With that in place, any time an exchange rate can't be found, the indirection
currency will be checked, and if set, then this:

``` python
rockefeller.Money(40, eur).exchange_to(clp)
# => None
```

will be treated internally as this:

``` python
rockefeller.Money(40, eur).exchange_to(usd).exchange_to(clp)
# => Decimal('24177.16', rockefeller.Currency.CLP)
```

**NOTICE**
Take into account that the __indirection currency__ is just a workaround used
by the ``Money`` class to convert money from one currency into another, if you
try to get the exchange rate between two unrelated currencies using
``get\_exchange\_rate()`` you will keep getting ``None``.


Installation
------------

The library has 0 dependencies outside of the standard library. In order to
install it just download the source and run:

    python setup.py install

Or you can install it directly from git using pip:

    pip install -e git+http://github.com/Floqq/Rockefeller.git#egg=Rockefeller

Running tests
-------------

    python setup.py test
