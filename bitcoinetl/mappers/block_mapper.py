# MIT License
#
# Copyright (c) 2018 Omidiora Samuel, samparsky@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from bitcoinetl.domain.block import BtcBlock
from bitcoinetl.mappers.transaction_mapper import BtcTransactionMapper


class BtcBlockMapper(object):
    def __init__(self, transaction_mapper=None):
        if transaction_mapper is None:
            self.transaction_mapper = BtcTransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def json_dict_to_block(self, json_dict):
        block = BtcBlock()
        block.hash = json_dict.get('hash')
        block.size = json_dict.get('size')
        block.stripped_size = json_dict.get('strippedsize')
        block.weight = json_dict.get('weight')
        block.number = json_dict.get('height')
        block.version = json_dict.get('version')
        block.merkle_root = json_dict.get('merkleroot')
        block.timestamp = json_dict.get('time')
        # bitcoin and all clones except zcash return integer nonce, zcash return hex string
        block.nonce = to_hex(json_dict.get('nonce'))
        block.bits = json_dict.get('bits')

        raw_transactions = json_dict.get('tx')
        if raw_transactions is not None and len(raw_transactions) > 0:
            if isinstance(raw_transactions[0], dict):
                block.transactions = [
                    self.transaction_mapper.json_dict_to_transaction(tx, block, idx) for idx, tx in enumerate(raw_transactions)
                ]
            else:
                # Transaction hashes
                block.transactions = raw_transactions

            block.transaction_count = len(raw_transactions)

        return block

    def block_to_dict(self, block):
        return {
            'type': 'block',
            'hash': block.hash,
            'size': block.size,
            'stripped_size': block.stripped_size,
            'weight': block.weight,
            'number': block.number,
            'version': block.version,
            'merkle_root': block.merkle_root,
            'timestamp': block.timestamp,
            'nonce': block.nonce,
            'bits': block.bits,
            'coinbase_param': block.coinbase_param,
            'transaction_count': len(block.transactions)
        }


def to_hex(val):
    if val is None:
        return None

    if isinstance(val, str):
        return val
    elif isinstance(val, int):
        return format(val, 'x')
    else:
        return val
