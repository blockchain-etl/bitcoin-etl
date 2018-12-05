import math


def bitcoin_to_satoshi(bitcoin_value):
    if bitcoin_value is None:
        return bitcoin_value

    return int(bitcoin_value * math.pow(10, 8))
