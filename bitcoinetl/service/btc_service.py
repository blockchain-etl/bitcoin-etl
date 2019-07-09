# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
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

from bitcoinetl.domain.transaction_input import BtcTransactionInput
from bitcoinetl.domain.transaction_output import BtcTransactionOutput
from bitcoinetl.enumeration.chain import Chain
from bitcoinetl.json_rpc_requests import generate_get_block_hash_by_number_json_rpc, \
    generate_get_block_by_hash_json_rpc, generate_get_transaction_by_id_json_rpc
from bitcoinetl.mappers.block_mapper import BtcBlockMapper
from bitcoinetl.mappers.transaction_mapper import BtcTransactionMapper
from bitcoinetl.service.btc_script_service import script_hex_to_non_standard_address
from bitcoinetl.service.genesis_transactions import GENESIS_TRANSACTIONS
from blockchainetl.utils import rpc_response_batch_to_results, dynamic_batch_iterator


class BtcService(object):
    def __init__(self, bitcoin_rpc, chain=Chain.BITCOIN):
        self.bitcoin_rpc = bitcoin_rpc
        self.block_mapper = BtcBlockMapper()
        self.transaction_mapper = BtcTransactionMapper()
        self.chain = chain

    def get_block(self, block_number, with_transactions=False):
        block_hashes = self.get_block_hashes([block_number])
        blocks = self.get_blocks_by_hashes(block_hashes, with_transactions)
        return blocks[0] if len(blocks) > 0 else None

    def get_genesis_block(self, with_transactions=False):
        return self.get_block(0, with_transactions)

    def get_latest_block(self, with_transactions=False):
        block_number = self.bitcoin_rpc.getblockcount()
        return self.get_block(block_number, with_transactions)

    def get_blocks(self, block_number_batch, with_transactions=False):
        if not block_number_batch:
            return []

        block_hashes = self.get_block_hashes(block_number_batch)
        return self.get_blocks_by_hashes(block_hashes, with_transactions)

    def get_blocks_by_hashes(self, block_hash_batch, with_transactions=True):
        if not block_hash_batch:
            return []

        # get block details by hash
        block_detail_rpc = list(generate_get_block_by_hash_json_rpc(block_hash_batch, with_transactions, self.chain))
        block_detail_response = self.bitcoin_rpc.batch(block_detail_rpc)
        block_detail_results = list(rpc_response_batch_to_results(block_detail_response))

        blocks = [self.block_mapper.json_dict_to_block(block_detail_result)
                  for block_detail_result in block_detail_results]

        if self.chain in Chain.HAVE_OLD_API and with_transactions:
            self._fetch_transactions(blocks)

        for block in blocks:
            self._remove_coinbase_input(block)
            if block.has_full_transactions():
                for transaction in block.transactions:
                    self._add_non_standard_addresses(transaction)
                    if self.chain == Chain.ZCASH:
                        self._add_shielded_inputs_and_outputs(transaction)

        return blocks

    def get_block_hashes(self, block_number_batch):
        block_hash_rpc = list(generate_get_block_hash_by_number_json_rpc(block_number_batch))
        block_hashes_response = self.bitcoin_rpc.batch(block_hash_rpc)
        block_hashes = rpc_response_batch_to_results(block_hashes_response)
        return block_hashes

    def get_transactions_by_hashes(self, hashes):
        if hashes is None or len(hashes) == 0:
            return []

        raw_transactions = self._get_raw_transactions_by_hashes_batched(hashes)
        transactions = [self.transaction_mapper.json_dict_to_transaction(tx) for tx in raw_transactions]
        for transaction in transactions:
            self._add_non_standard_addresses(transaction)
            if self.chain == Chain.ZCASH:
                self._add_shielded_inputs_and_outputs(transaction)
        return transactions

    def _fetch_transactions(self, blocks):
        all_transaction_hashes = [block.transactions for block in blocks]
        flat_transaction_hashes = [hash for transaction_hashes in all_transaction_hashes for hash in transaction_hashes]
        raw_transactions = self._get_raw_transactions_by_hashes_batched(flat_transaction_hashes)

        for block in blocks:
            raw_block_transactions = [tx for tx in raw_transactions if tx.get('txid') in block.transactions]
            block.transactions = [self.transaction_mapper.json_dict_to_transaction(tx, block)
                                  for tx in raw_block_transactions]

    def _get_raw_transactions_by_hashes_batched(self, hashes):
        if hashes is None or len(hashes) == 0:
            return []

        result = []
        batch_size = 100
        for batch in dynamic_batch_iterator(hashes, lambda: batch_size):
            result.extend(self._get_raw_transactions_by_hashes(batch))

        return result

    def _get_raw_transactions_by_hashes(self, hashes):
        if hashes is None or len(hashes) == 0:
            return []

        genesis_transaction = GENESIS_TRANSACTIONS.get(self.chain)
        genesis_transaction_hash = genesis_transaction.get('txid') if genesis_transaction is not None else None
        filtered_hashes = [transaction_hash for transaction_hash in hashes
                           if transaction_hash != genesis_transaction_hash]
        transaction_detail_rpc = list(generate_get_transaction_by_id_json_rpc(filtered_hashes))
        transaction_detail_response = self.bitcoin_rpc.batch(transaction_detail_rpc)
        transaction_detail_results = rpc_response_batch_to_results(transaction_detail_response)
        raw_transactions = list(transaction_detail_results)

        if genesis_transaction_hash is not None and genesis_transaction_hash in hashes:
            raw_transactions.append(genesis_transaction)

        return raw_transactions

    def _remove_coinbase_input(self, block):
        if block.has_full_transactions():
            for transaction in block.transactions:
                coinbase_inputs = [input for input in transaction.inputs if input.is_coinbase()]
                if len(coinbase_inputs) > 1:
                    raise ValueError('There must be no more than 1 coinbase input in any transaction. Was {}, hash {}'
                                     .format(len(coinbase_inputs), transaction.hash))
                coinbase_input = coinbase_inputs[0] if len(coinbase_inputs) > 0 else None
                if coinbase_input is not None:
                    block.coinbase_param = coinbase_input.coinbase_param
                    transaction.inputs = [input for input in transaction.inputs if not input.is_coinbase()]
                    transaction.is_coinbase = True

    def _add_non_standard_addresses(self, transaction):
        for output in transaction.outputs:
            if output.addresses is None or len(output.addresses) == 0:
                output.type = 'nonstandard'
                output.addresses = [script_hex_to_non_standard_address(output.script_hex)]

    def _add_shielded_inputs_and_outputs(self, transaction):
        if transaction.join_splits is not None and len(transaction.join_splits) > 0:
            for join_split in transaction.join_splits:
                input_value = join_split.public_input_value or 0
                output_value = join_split.public_output_value or 0
                if input_value > 0:
                    input = BtcTransactionInput()
                    input.type = ADDRESS_TYPE_SHIELDED
                    input.value = input_value
                    transaction.add_input(input)
                if output_value > 0:
                    output = BtcTransactionOutput()
                    output.type = ADDRESS_TYPE_SHIELDED
                    output.value = output_value
                    transaction.add_output(output)
        if transaction.value_balance is not None and transaction.value_balance != 0:
            if transaction.value_balance > 0:
                input = BtcTransactionInput()
                input.type = ADDRESS_TYPE_SHIELDED
                input.value = transaction.value_balance
                transaction.add_input(input)
            if transaction.value_balance < 0:
                output = BtcTransactionOutput()
                output.type = ADDRESS_TYPE_SHIELDED
                output.value = -transaction.value_balance
                transaction.add_output(output)


ADDRESS_TYPE_SHIELDED = 'shielded'
