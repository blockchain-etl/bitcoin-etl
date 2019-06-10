class Chain:
    BITCOIN = 'bitcoin'
    BITCOIN_CASH = 'bitcoin_cash'
    DOGECOIN = 'dogecoin'
    LITECOIN = 'litecoin'
    DASH = 'dash'
    ZCASH = 'zcash'
    MONACOIN = 'monacoin'

    ALL = [BITCOIN, BITCOIN_CASH, DOGECOIN, LITECOIN, DASH, ZCASH, MONACOIN]
    # Old API doesn't support verbosity for getblock which doesn't allow querying all transactions in a block in 1 go.
    HAVE_OLD_API = [BITCOIN_CASH, DOGECOIN, DASH, MONACOIN]
