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
import os
import time

from bitcoinetl.enumeration.chain import Chain
from bitcoinetl.jobs.enrich_transactions import EnrichTransactionsJob
from bitcoinetl.jobs.export_blocks_job import ExportBlocksJob
from bitcoinetl.service.btc_service import BtcService
from blockchainetl.file_utils import smart_open
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()


def write_last_synced_block(file, last_synced_block):
    with smart_open(file, 'w') as last_synced_block_file:
        return last_synced_block_file.write(str(last_synced_block) + '\n')


def init_last_synced_block_file(start_block, last_synced_block_file):
    if os.path.isfile(last_synced_block_file):
        raise ValueError(
            '{} should not exist if --start-block option is specified. '
            'Either remove the {} file or the --start-block option.'
                .format(last_synced_block_file, last_synced_block_file))
    write_last_synced_block(last_synced_block_file, start_block)


def read_last_synced_block(file):
    with smart_open(file, 'r') as last_synced_block_file:
        return int(last_synced_block_file.read())


def stream(
        bitcoin_rpc,
        last_synced_block_file='last_synced_block.txt',
        lag=0,
        item_exporter=ConsoleItemExporter(),
        start_block=None,
        end_block=None,
        chain=Chain.BITCOIN,
        period_seconds=10,
        batch_size=2,
        block_batch_size=10,
        max_workers=5):
    if start_block is not None or not os.path.isfile(last_synced_block_file):
        init_last_synced_block_file((start_block or 0) - 1, last_synced_block_file)

    last_synced_block = read_last_synced_block(last_synced_block_file)
    btc_service = BtcService(bitcoin_rpc, chain)

    item_exporter.open()

    while True and (end_block is None or last_synced_block < end_block):
        blocks_to_sync = 0

        try:
            current_block = int(btc_service.get_latest_block().number)
            target_block = current_block - lag
            target_block = min(target_block, last_synced_block + block_batch_size)
            target_block = min(target_block, end_block) if end_block is not None else target_block
            blocks_to_sync = max(target_block - last_synced_block, 0)
            logging.info('Current block {}, target block {}, last synced block {}, blocks to sync {}'.format(
                current_block, target_block, last_synced_block, blocks_to_sync))

            if blocks_to_sync == 0:
                logging.info('Nothing to sync. Sleeping for {} seconds...'.format(period_seconds))
                time.sleep(period_seconds)
                continue

            # Export blocks and transactions
            blocks_and_transactions_item_exporter = InMemoryItemExporter(item_types=['block', 'transaction'])

            blocks_and_transactions_job = ExportBlocksJob(
                start_block=last_synced_block + 1,
                end_block=target_block,
                batch_size=batch_size,
                bitcoin_rpc=bitcoin_rpc,
                max_workers=max_workers,
                item_exporter=blocks_and_transactions_item_exporter,
                chain=chain,
                export_blocks=True,
                export_transactions=True
            )
            blocks_and_transactions_job.run()

            blocks = blocks_and_transactions_item_exporter.get_items('block')
            transactions = blocks_and_transactions_item_exporter.get_items('transaction')

            # Enrich transactions
            enriched_transactions_item_exporter = InMemoryItemExporter(item_types=['transaction'])

            enrich_transactions_job = EnrichTransactionsJob(
                transactions_iterable=transactions,
                batch_size=batch_size,
                bitcoin_rpc=bitcoin_rpc,
                max_workers=max_workers,
                item_exporter=enriched_transactions_item_exporter,
                chain=chain
            )
            enrich_transactions_job.run()
            enriched_transactions = enriched_transactions_item_exporter.get_items('transaction')
            if len(enriched_transactions) != len(transactions):
                raise ValueError('The number of transactions is wrong ' + str(transactions))

            logging.info('Exporting with ' + type(item_exporter).__name__)
            item_exporter.export_items(blocks + enriched_transactions)

            logging.info('Writing last synced block {}'.format(target_block))
            write_last_synced_block(last_synced_block_file, target_block)
            last_synced_block = target_block
        except Exception as e:
            # https://stackoverflow.com/a/4992124/1580227
            logging.exception('An exception occurred while fetching block data.')

        if blocks_to_sync != block_batch_size and last_synced_block != end_block:
            logging.info('Sleeping {} seconds...'.format(period_seconds))
            time.sleep(period_seconds)

    item_exporter.close()
