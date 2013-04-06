from rockefeller.services import OpenExchangeRates, ServiceError
from rockefeller.utils import basic_config_logging_handler

# use this for log the openexchangerates service request and response to the
# console.
basic_config_logging_handler()


APP_ID = 'your app id here'

service = OpenExchangeRates(app_id=APP_ID)

try:
    exchange_rates = service.latest()
except ServiceError as e:
    print e.message
else:
    for exchange_rate in exchange_rates:
        print exchange_rate
