# Transactions in genesis blocks return error for getrawtransaction API
# The genesis block coinbase is not considered an ordinary transaction and cannot be retrieved
from decimal import Decimal

GENESIS_TRANSACTIONS = {
    'dogecoin': {
        'txid': '5b2a3f53f605d62c53e62932dac6925e3d74afa5a4b459745c36d42d0ed26a69',
        'blockhash': '1a91e3dace36e2be3bf030a65679fe821aa1d6ef92e7c9902eb318182c355691',
        'locktime': 0,
        'vin': [
            {
                "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73",
                "sequence": 4294967295
            }
        ],
        'vout': [
            {
                "value": Decimal('50.00000000'),
                "n": 0,
                "scriptPubKey": {
                    "asm": "040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac OP_CHECKSIG",
                    "hex": "41040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac",
                    "reqSigs": 1,
                    "type": "pubkey",
                    "addresses": [
                        "BZv7UykZdDFxh48RNjKPeH2PvGxcCKDuW"
                    ]
                }
            }
        ],
        'version': 1
    },
    'bitcoin_cash': {
        'txid': '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b',
        'blockhash': '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
        'locktime': 0,
        'vin': [
            {
                "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73",
                "sequence": 4294967295
            }
        ],
        'vout': [
            {
                "value": Decimal('50.00000000'),
                "n": 0,
                "scriptPubKey": {
                    "asm": "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f OP_CHECKSIG",
                    "hex": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac",
                    "reqSigs": 1,
                    "type": "pubkey",
                    "addresses": [
                        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
                    ]
                }
            }
        ],
        'version': 1
    },
    'dash': {
        'txid': 'e0028eb9648db56b1ac77cf090b99048a8007e2bb64b68f092c03c7f56a662c7',
        'blockhash': '00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6',
        'locktime': 0,
        'vin': [
            {
                "coinbase": "04ffff001d01044c5957697265642030392f4a616e2f3230313420546865204772616e64204578706572696d656e7420476f6573204c6976653a204f76657273746f636b2e636f6d204973204e6f7720416363657074696e6720426974636f696e73",
                "sequence": 4294967295
            }
        ],
        'vout': [
            {
                "value": Decimal('50.00000000'),
                "n": 0,
                "scriptPubKey": {
                    "asm": "040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9 OP_CHECKSIG",
                    "hex": "41040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac",
                    "reqSigs": 1,
                    "type": "pubkey",
                    "addresses": [
                        "XmFkwjdeXLRr7deiHG3YFAxpEFred8L5C9"
                    ]
                }
            }
        ],
        'version': 1
    },
    'monacoin': {
        'txid': '35e405a8a46f4dbc1941727aaf338939323c3b955232d0317f8731fe07ac4ba6',
        'blockhash': 'ff9f1c0116d19de7c9963845e129f9ed1bfc0b376eb54fd7afa42e0d418c8bb6',
        'locktime': 0,
        'vin': [
            {
                "coinbase": "04ffff001d01044c564465632e20333174682032303133204a6170616e2c205468652077696e6e696e67206e756d62657273206f6620746865203230313320596561722d456e64204a756d626f204c6f74746572793a32332d313330393136",
                "sequence": 4294967295
            }
        ],
        'vout': [
            {
                "value": Decimal('50.00000000'),
                "n": 0,
                "scriptPubKey": {
                    "asm": "040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac OP_CHECKSIG",
                    "hex": "41040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": [
                        "MTXGFakp6JUSpdYhf63fN3Yx5Rz88pantR"
                    ]
                }
            }
        ],
        'version': 1
    },
}
