import math
from decimal import Decimal


def bitcoin_to_satoshi(bitcoin_value):
    if bitcoin_value is None:
        return bitcoin_value

    if isinstance(bitcoin_value, Decimal):
        return int(bitcoin_value * (Decimal(10) ** 8).to_integral_value())
    else:
        return int(bitcoin_value * math.pow(10, 8))
