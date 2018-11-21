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
from blockchainetl.utils import hex_to_dec, to_normalized_address


class BtcBlockMapper(object):
    def __init__(self, transaction_mapper=None):
        if transaction_mapper is None:
            self.transaction_mapper = BtcTransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def json_dict_to_block(self, json_dict):
        block = BtcBlock()
        block.hash = json_dict.get('hash')
        block.confirmations = json_dict.get('confirmations')
        block.size = json_dict.get('size')
        block.strippedsize = json_dict.get('strippedsize')
        block.weight = json_dict.get('weight')
        block.height = json_dict.get('height')
        block.version = json_dict.get('version')
        block.versionHex = json_dict.get('versionHex')
        block.merkleroot = json_dict.get('merkleroot')
        block.time = json_dict.get('time')
        block.mediantime = json_dict.get('mediantime')
        block.nonce = json_dict.get('nonce')
        block.bits = json_dict.get('bits')
        block.difficulty = json_dict.get('difficulty')
        block.chainwork = json_dict.get('chainwork')
        block.previousblockhash = json_dict.get('previousblockhash')
        block.nextblockhash = json_dict.get('nextblockhash')

        if 'tx' in json_dict:
            block.transactions = [
                self.transaction_mapper.json_dict_to_transaction(tx) for tx in json_dict['tx']
                if isinstance(tx, dict)
            ]

            block.transaction_count = len(json_dict['transactions'])

        return block

    def block_to_dict(self, block):
        return {
            'type': 'block',
            'number': block.number,
            'hash': block.hash,
            'parent_hash': block.parent_hash,
            'nonce': block.nonce,
            'sha3_uncles': block.sha3_uncles,
            'logs_bloom': block.logs_bloom,
            'transactions_root': block.transactions_root,
            'state_root': block.state_root,
            'receipts_root': block.receipts_root,
            'miner': block.miner,
            'difficulty': block.difficulty,
            'total_difficulty': block.total_difficulty,
            'size': block.size,
            'extra_data': block.extra_data,
            'gas_limit': block.gas_limit,
            'gas_used': block.gas_used,
            'timestamp': block.timestamp,
            'transaction_count': block.transaction_count,
        }
