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

from bitcoinetl.enumeration.chain import Chain
from bitcoinetl.mappers.transaction_mapper import BtcTransactionMapper
from bitcoinetl.service.btc_service import BtcService
from blockchainetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from blockchainetl.utils import dynamic_batch_iterator


# Add required_signatures, type, addresses, and value to transaction inputs
class EnrichTransactionsJob(BaseJob):
    def __init__(
            self,
            transactions_iterable,
            batch_size,
            bitcoin_rpc,
            max_workers,
            item_exporter,
            chain=Chain.BITCOIN):
        self.transactions_iterable = transactions_iterable
        self.btc_service = BtcService(bitcoin_rpc, chain)

        self.batch_size = batch_size
        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers, exponential_backoff=False)
        self.item_exporter = item_exporter

        self.transaction_mapper = BtcTransactionMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(self.transactions_iterable, self._enrich_transactions)

    def _enrich_transactions(self, transactions):
        transactions = [self.transaction_mapper.dict_to_transaction(transaction) for transaction in transactions]

        all_inputs = [transaction.inputs for transaction in transactions]
        flat_inputs = [input for inputs in all_inputs for input in inputs]

        for transaction_input_batch in dynamic_batch_iterator(flat_inputs, lambda: self.batch_size):
            input_transactions_map = self._get_input_transactions_as_map(transaction_input_batch)
            for input in transaction_input_batch:
                output = self._get_output_for_input(input, input_transactions_map) \
                    if input.spent_transaction_hash is not None else None
                if output is not None:
                    input.required_signatures = output.required_signatures
                    input.type = output.type
                    input.addresses = output.addresses
                    input.value = output.value

        for transaction in transactions:
            self.item_exporter.export_item(self.transaction_mapper.transaction_to_dict(transaction))

    def _get_input_transactions_as_map(self, transaction_inputs):
        transaction_hashes = [input.spent_transaction_hash for input in transaction_inputs
                              if input.spent_transaction_hash is not None]

        transaction_hashes = set(transaction_hashes)
        if len(transaction_hashes) > 0:
            transactions = self.btc_service.get_transactions_by_hashes(transaction_hashes)
            return {transaction.hash: transaction for transaction in transactions}
        else:
            return {}

    def _get_output_for_input(self, transaction_input, input_transactions_map):
        spent_transaction_hash = transaction_input.spent_transaction_hash
        input_transaction = input_transactions_map.get(spent_transaction_hash)
        if input_transaction is None:
            raise ValueError('Input transaction with hash {} not found'.format(spent_transaction_hash))

        spent_output_index = transaction_input.spent_output_index
        if input_transaction.outputs is None or len(input_transaction.outputs) < (spent_output_index + 1):
            raise ValueError(
                'There is no output with index {} in transaction with hash {}'.format(
                    spent_output_index, spent_transaction_hash))

        output = input_transaction.outputs[spent_output_index]
        return output

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
