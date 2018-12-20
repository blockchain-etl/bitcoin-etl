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


from bitcoinetl.json_rpc_requests import generate_get_block_hash_by_number_json_rpc, \
    generate_get_block_by_hash_json_rpc, generate_get_transaction_by_id_json_rpc
from bitcoinetl.mappers.block_mapper import BtcBlockMapper
from bitcoinetl.mappers.transaction_mapper import BtcTransactionMapper
from blockchainetl.utils import rpc_response_batch_to_results, dynamic_batch_iterator


class BtcService(object):
    def __init__(self, bitcoin_rpc, chain='bitcoin'):
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

        if self.chain in ('dogecoin', 'bitcoin_cash') and with_transactions:
            blocks = self._enrich_blocks_with_transactions(blocks)

        self._remove_coinbase_inputs(blocks)

        return blocks

    def get_block_hashes(self, block_number_batch):
        block_hash_rpc = list(generate_get_block_hash_by_number_json_rpc(block_number_batch))
        block_hashes_response = self.bitcoin_rpc.batch(block_hash_rpc)
        block_hashes = rpc_response_batch_to_results(block_hashes_response)
        return block_hashes

    def _enrich_blocks_with_transactions(self, blocks):
        all_transaction_hashes = [block.transactions for block in blocks]
        flat_transaction_hashes = [hash for transaction_hashes in all_transaction_hashes for hash in transaction_hashes]
        raw_transactions = self._get_raw_transactions_by_hashes_batched(flat_transaction_hashes)

        for block in blocks:
            raw_block_transactions = [tx for tx in raw_transactions if tx.get('blockhash') == block.hash]
            block.transactions = [self.transaction_mapper.json_dict_to_transaction(tx, block)
                                  for tx in raw_block_transactions]

        return blocks

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

        genesis_transaction_hashes = [transaction['txid'] for transaction in GENESIS_TRANSACTIONS.values()]
        filtered_hashes = [transaction_hash for transaction_hash in hashes
                           if transaction_hash not in genesis_transaction_hashes]
        transaction_detail_rpc = list(generate_get_transaction_by_id_json_rpc(filtered_hashes))
        transaction_detail_response = self.bitcoin_rpc.batch(transaction_detail_rpc)
        transaction_detail_results = rpc_response_batch_to_results(transaction_detail_response)
        raw_transactions = list(transaction_detail_results)

        for genesis_transaction in GENESIS_TRANSACTIONS.values():
            if genesis_transaction['txid'] in hashes:
                raw_transactions.append(genesis_transaction)

        return raw_transactions

    def _remove_coinbase_inputs(self, blocks):
        for block in blocks:
            self._remove_coinbase_input(block)

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


# Transactions in genesis blocks return error for getrawtransaction API
# The genesis block coinbase is not considered an ordinary transaction and cannot be retrieved
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
                "value": 50.00000000,
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
                "value": 50.00000000,
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
    }
}
