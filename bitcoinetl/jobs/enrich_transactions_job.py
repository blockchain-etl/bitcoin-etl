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


from bitcoinetl.json_rpc_requests import generate_get_transaction_by_id_json_rpc
from bitcoinetl.mappers.transaction_mapper import BtcTransactionMapper
from blockchainetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob

from blockchainetl.utils import dynamic_batch_iterator


# Enrich transactions
class EnrichTransactionsJob(BaseJob):
    def __init__(
            self,
            transactions_iterable,
            batch_size,
            bitcoin_rpc,
            max_workers,
            item_exporter):
        self.transactions_iterable = transactions_iterable
        self.bitcoin_rpc = bitcoin_rpc

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers, exponential_backoff=False)
        self.item_exporter = item_exporter

        self.transaction_mapper = BtcTransactionMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(self.transactions_iterable, self._enrich_transactions)

    def _enrich_transactions(self, transactions):
        all_inputs = [transaction.get('inputs', []) for transaction in transactions]
        flat_inputs = [input for inputs in all_inputs for input in inputs]
        txids = [input.get('spent_txid') for input in flat_inputs if input.get('spent_txid') is not None]

        if len(txids) == 0:
            return

        txids = set(txids)

        input_transactions = self._get_transactions(txids, len(transactions))
        input_transactions_map = {input_transaction.txid: input_transaction for input_transaction in input_transactions}

        for input in flat_inputs:
            spent_txid = input.get('spent_txid')
            if spent_txid is None:
                continue
            input_transaction = input_transactions_map.get(spent_txid)
            if input_transaction is None:
                raise ValueError('Input transaction with txid {} not found'.format(spent_txid))

            spent_output_index = input.get('spent_output_index')
            if input_transaction.outputs is None or len(input_transaction.outputs) < (spent_output_index + 1):
                raise ValueError(
                    'There is no output with index {} in transaction with txid {}'.format(
                        spent_output_index, spent_txid))

            output = input_transaction.outputs[spent_output_index]
            input['addresses'] = output.addresses
            input['value'] = output.value

        for transaction in transactions:
            transaction['type'] = 'transaction'
            self.item_exporter.export_item(transaction)

    def _get_transactions(self, txids, batch_size):
        result = []
        for batch in dynamic_batch_iterator(txids, lambda: batch_size):
            transaction_detail_rpc = list(generate_get_transaction_by_id_json_rpc(batch))
            transaction_detail_response = self.bitcoin_rpc.batch(transaction_detail_rpc)

            transactions = [self.transaction_mapper.json_dict_to_transaction(raw_transaction)
                            for raw_transaction in transaction_detail_response]

            result.extend(transactions)

        return result

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
