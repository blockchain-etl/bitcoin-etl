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

    def get_blocks(self, block_number_batch, with_transactions=True):
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

        if self.chain == 'dogecoin' and with_transactions:
            blocks = self._enrich_blocks_with_transactions(blocks)

        return blocks

    def get_block_hashes(self, block_number_batch):
        block_hash_rpc = list(generate_get_block_hash_by_number_json_rpc(block_number_batch))
        block_hashes_response = self.bitcoin_rpc.batch(block_hash_rpc)
        block_hashes = rpc_response_batch_to_results(block_hashes_response)
        return block_hashes

    def _enrich_blocks_with_transactions(self, blocks):
        all_txids = [block.transactions for block in blocks]
        flat_txids = [txid for txids in all_txids for txid in txids]
        raw_transactions = self._get_raw_transactions_by_txids_batched(flat_txids)

        for block in blocks:
            raw_block_transactions = [tx for tx in raw_transactions if tx.get('blockhash') == block.hash]
            block.transactions = [self.transaction_mapper.json_dict_to_transaction(tx, block)
                                  for tx in raw_block_transactions]
            block.transaction_count = len(block.transactions)

        return blocks

    def _get_raw_transactions_by_txids_batched(self, txids):
        if txids is None or len(txids) == 0:
            return []

        result = []
        batch_size = 100
        for batch in dynamic_batch_iterator(txids, lambda: batch_size):
            result.extend(self._get_raw_transactions_by_txids(batch))

        return result

    def _get_raw_transactions_by_txids(self, txids):
        if txids is None or len(txids) == 0:
            return []

        filtered_txids = [txid for txid in txids if txid != DOGECOIN_ERROREOUS_TRANSACTION['txid']]
        transaction_detail_rpc = list(generate_get_transaction_by_id_json_rpc(filtered_txids))
        transaction_detail_response = self.bitcoin_rpc.batch(transaction_detail_rpc)
        transaction_detail_results = rpc_response_batch_to_results(transaction_detail_response)
        raw_transactions = list(transaction_detail_results)

        if DOGECOIN_ERROREOUS_TRANSACTION['txid'] in txids:
            raw_transactions.append(DOGECOIN_ERROREOUS_TRANSACTION)

        return raw_transactions


# The transaction in 0th block in Dogecoin returns error for getrawtransaction rpc
DOGECOIN_ERROREOUS_TRANSACTION = {
    'txid': '5b2a3f53f605d62c53e62932dac6925e3d74afa5a4b459745c36d42d0ed26a69',
    'blockhash': '1a91e3dace36e2be3bf030a65679fe821aa1d6ef92e7c9902eb318182c355691',
    'locktime': 0,
    'vin': [],
    'vout': [],
    'version': 1
}
