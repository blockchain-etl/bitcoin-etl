class Chain:
    BITCOIN = 'bitcoin'
    BITCOIN_CASH = 'bitcoin_cash'
    BITCOIN_SV = 'bitcoin_sv'
    DOGECOIN = 'dogecoin'
    LITECOIN = 'litecoin'
    DASH = 'dash'
    ZCASH = 'zcash'
    MONACOIN = 'monacoin'

    ALL = [BITCOIN, BITCOIN_CASH, DOGECOIN, LITECOIN, DASH, ZCASH, MONACOIN]
    # Old API doesn't support verbosity for getblock which doesn't allow querying all transactions in a block in 1 go.
    HAVE_OLD_API = [BITCOIN_CASH, DOGECOIN, DASH, MONACOIN]

    @classmethod
    def ticker_symbol(cls, chain):
        symbols = {
            'bitcoin': 'BTC',
            'bitcoin_cash': 'BCH',
            'bitcoin_sv': 'BSV',
            'dogecoin': 'DOGE',
            'litecoin': 'LTC',
            'dash': 'DASH',
            'zcash': 'ZEC',
            'monacoin': 'MONA',
        }
        return symbols.get(chain, None)


class CoinPriceType:

    empty = 0
    daily = 1
    hourly = 2
