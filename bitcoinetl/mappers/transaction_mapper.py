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

from bitcoinetl.btc_utils import bitcoin_to_satoshi
from bitcoinetl.domain.transaction import BtcTransaction
from bitcoinetl.mappers.join_split_mapper import BtcJoinSplitMapper
from bitcoinetl.mappers.transaction_input_mapper import BtcTransactionInputMapper
from bitcoinetl.mappers.transaction_output_mapper import BtcTransactionOutputMapper


# http://chainquery.com/bitcoin-api/getblock
# http://chainquery.com/bitcoin-api/getrawtransaction
class BtcTransactionMapper(object):

    def __init__(self):
        self.transaction_input_mapper = BtcTransactionInputMapper()
        self.transaction_output_mapper = BtcTransactionOutputMapper()
        self.join_split_mapper = BtcJoinSplitMapper()

    def json_dict_to_transaction(self, json_dict, block=None, index=None):
        transaction = BtcTransaction()
        transaction.hash = json_dict.get('txid')
        transaction.size = json_dict.get('size')
        transaction.virtual_size = json_dict.get('vsize')
        transaction.version = json_dict.get('version')
        transaction.lock_time = json_dict.get('locktime')

        if block is not None:
            transaction.block_number = block.number

        transaction.block_hash = json_dict.get('blockhash')
        if block is not None:
            transaction.block_hash = block.hash

        transaction.block_timestamp = json_dict.get('blocktime')
        if block is not None:
            transaction.block_timestamp = block.timestamp

        if index is not None:
            transaction.index = index

        transaction.inputs = self.transaction_input_mapper.vin_to_inputs(json_dict.get('vin'))
        transaction.outputs = self.transaction_output_mapper.vout_to_outputs(json_dict.get('vout'))

        # Only Zcash
        transaction.join_splits = self.join_split_mapper.vjoinsplit_to_join_splits(json_dict.get('vjoinsplit'))
        transaction.value_balance = bitcoin_to_satoshi(json_dict.get('valueBalance'))

        return transaction

    def transaction_to_dict(self, transaction):
        result = {
            'type': 'transaction',
            'hash': transaction.hash,
            'size': transaction.size,
            'virtual_size': transaction.virtual_size,
            'version': transaction.version,
            'lock_time': transaction.lock_time,
            'block_number': transaction.block_number,
            'block_hash': transaction.block_hash,
            'block_timestamp': transaction.block_timestamp,
            'is_coinbase': transaction.is_coinbase,
            'index': transaction.index,

            'inputs': self.transaction_input_mapper.inputs_to_dicts(transaction.inputs),
            'outputs': self.transaction_output_mapper.outputs_to_dicts(transaction.outputs),

            'input_count': len(transaction.inputs),
            'output_count': len(transaction.outputs),
            'input_value': transaction.calculate_input_value(),
            'output_value': transaction.calculate_output_value(),
            'fee': transaction.calculate_fee(),
        }
        return result

    def dict_to_transaction(self, dict):
        transaction = BtcTransaction()
        transaction.hash = dict.get('hash')
        transaction.size = dict.get('size')
        transaction.virtual_size = dict.get('virtual_size')
        transaction.version = dict.get('version')
        transaction.lock_time = dict.get('lock_time')
        transaction.block_number = dict.get('block_number')
        transaction.block_hash = dict.get('block_hash')
        transaction.block_timestamp = dict.get('block_timestamp')
        transaction.is_coinbase = dict.get('is_coinbase')
        transaction.index = dict.get('index')

        transaction.inputs = self.transaction_input_mapper.dicts_to_inputs(dict.get('inputs'))
        transaction.outputs = self.transaction_output_mapper.dicts_to_outputs(dict.get('outputs'))

        return transaction
