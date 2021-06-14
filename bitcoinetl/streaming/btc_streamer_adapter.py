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


import logging

from bitcoinetl.enumeration.chain import Chain
from bitcoinetl.jobs.enrich_transactions import EnrichTransactionsJob
from bitcoinetl.jobs.export_blocks_job import ExportBlocksJob
from bitcoinetl.service.btc_service import BtcService
from bitcoinetl.streaming.btc_item_id_calculator import BtcItemIdCalculator
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter


class BtcStreamerAdapter:
    def __init__(
            self,
            bitcoin_rpc,
            item_exporter=ConsoleItemExporter(),
            chain=Chain.BITCOIN,
            batch_size=2,
            enable_enrich=True,
            max_workers=5):
        self.bitcoin_rpc = bitcoin_rpc
        self.chain = chain
        self.btc_service = BtcService(bitcoin_rpc, chain)
        self.item_exporter = item_exporter
        self.batch_size = batch_size
        self.enable_enrich = enable_enrich
        self.max_workers = max_workers
        self.item_id_calculator = BtcItemIdCalculator()

    def open(self):
        self.item_exporter.open()

    def get_current_block_number(self):
        return int(self.btc_service.get_latest_block().number)

    def export_all(self, start_block, end_block):
        # Export blocks and transactions
        blocks_and_transactions_item_exporter = InMemoryItemExporter(item_types=['block', 'transaction'])

        blocks_and_transactions_job = ExportBlocksJob(
            start_block=start_block,
            end_block=end_block,
            batch_size=self.batch_size,
            bitcoin_rpc=self.bitcoin_rpc,
            max_workers=self.max_workers,
            item_exporter=blocks_and_transactions_item_exporter,
            chain=self.chain,
            export_blocks=True,
            export_transactions=True
        )
        blocks_and_transactions_job.run()

        blocks = blocks_and_transactions_item_exporter.get_items('block')
        transactions = blocks_and_transactions_item_exporter.get_items('transaction')

        if self.enable_enrich:
            # Enrich transactions
            enriched_transactions_item_exporter = InMemoryItemExporter(item_types=['transaction'])

            enrich_transactions_job = EnrichTransactionsJob(
                transactions_iterable=transactions,
                batch_size=self.batch_size,
                bitcoin_rpc=self.bitcoin_rpc,
                max_workers=self.max_workers,
                item_exporter=enriched_transactions_item_exporter,
                chain=self.chain
            )
            enrich_transactions_job.run()
            enriched_transactions = enriched_transactions_item_exporter.get_items('transaction')
            if len(enriched_transactions) != len(transactions):
                raise ValueError('The number of transactions is wrong ' + str(transactions))
            transactions = enriched_transactions

        logging.info('Exporting with ' + type(self.item_exporter).__name__)

        all_items = blocks + transactions

        self.calculate_item_ids(all_items)

        self.item_exporter.export_items(all_items)

    def calculate_item_ids(self, items):
        for item in items:
            item['item_id'] = self.item_id_calculator.calculate(item)

    def close(self):
        self.item_exporter.close()
