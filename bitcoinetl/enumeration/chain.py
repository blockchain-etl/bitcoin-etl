class Chain:
    BITCOIN = 'bitcoin'
    BITCOIN_CASH = 'bitcoin_cash'
    BITCOIN_CASH_SV = 'bitcoin_cash_sv'
    BITCOIN_GOLD = 'bitcoin_gold'
    DOGECOIN = 'dogecoin'
    LITECOIN = 'litecoin'
    DASH = 'dash'
    ZCASH = 'zcash'
    MONACOIN = 'monacoin'

    ALL = [BITCOIN, BITCOIN_CASH, BITCOIN_CASH_SV, BITCOIN_GOLD, DOGECOIN, LITECOIN, DASH, ZCASH, MONACOIN]
    # Old API doesn't support verbosity for getblock which doesn't allow querying all transactions in a block in 1 go.
    HAVE_OLD_API = [BITCOIN_CASH, DOGECOIN, DASH, MONACOIN]

    @classmethod
    def ticker_symbol(cls, chain):
        symbols = {
            'bitcoin': 'BTC',
            'bitcoin_cash': 'BCH',
            'bitcoin_cash_sv': 'BSV',
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
