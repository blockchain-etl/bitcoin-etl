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
from blockchainetl.file_utils import smart_open
from bitcoinetl.jobs.export_blocks_job import ExportBlocksJob
from blockchainetl.jobs.exporters.console_item_exporter import ConsoleItemExporter
from blockchainetl.jobs.exporters.google_pubsub_item_exporter import GooglePubSubItemExporter
from blockchainetl.jobs.exporters.in_memory_item_exporter import InMemoryItemExporter
from blockchainetl.logging_utils import logging_basic_config
from bitcoinetl.rpc.bitcoin_rpc import BitcoinRpc
from bitcoinetl.service.btc_service import BtcService
from blockchainetl.thread_local_proxy import ThreadLocalProxy
from google.api_core.exceptions import GoogleAPIError

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


def enrich_transactions(transactions):
    return transactions


def stream(last_synced_block_file, lag, provider_uri, output, start_block, chain=Chain.BITCOIN,
           period_seconds=10, batch_size=2, max_workers=5):
    if start_block is not None:
        init_last_synced_block_file(start_block, last_synced_block_file)

    max_batch_size = 10

    last_synced_block = read_last_synced_block(last_synced_block_file)
    btc_service = BtcService(BitcoinRpc(provider_uri), chain)

    if output is not None:
        item_exporter = GooglePubSubItemExporter(output)
    else:
        item_exporter = ConsoleItemExporter()

    while True:
        blocks_to_sync = 0
        try:
            current_block = int(btc_service.get_latest_block().number)
            target_block = current_block - lag
            target_block = min(target_block, last_synced_block + max_batch_size)
            blocks_to_sync = max(target_block - last_synced_block, 0)
            logging.info('Current block {}, target block {}, last synced block {}, blocks to sync {}'.format(
                current_block, target_block, last_synced_block, blocks_to_sync))

            if blocks_to_sync == 0:
                logging.info('Nothing to sync. Sleeping {} seconds...'.format(period_seconds))
                time.sleep(period_seconds)
                continue

            # Export blocks and transactions
            blocks_and_transactions_item_exporter = InMemoryItemExporter(item_types=['block', 'transaction'])

            blocks_and_transactions_job = ExportBlocksJob(
                start_block=last_synced_block + 1,
                end_block=target_block,
                batch_size=batch_size,
                bitcoin_rpc=ThreadLocalProxy(lambda: BitcoinRpc(provider_uri)),
                max_workers=max_workers,
                item_exporter=blocks_and_transactions_item_exporter,
                chain=chain,
                export_blocks=True,
                export_transactions=True
            )
            blocks_and_transactions_job.run()

            blocks = blocks_and_transactions_item_exporter.get_items('block')
            transactions = blocks_and_transactions_item_exporter.get_items('transaction')

            enriched_transactions = enrich_transactions(transactions)
            if len(enriched_transactions) != len(transactions):
                raise ValueError('The number of transactions is wrong ' + str(enriched_transactions))

            logging.info('Pushing to ' + ('console' if output is None else 'PubSub'))
            item_exporter.export_items(blocks + enriched_transactions)

            logging.info('Writing last synced block {}'.format(target_block))
            write_last_synced_block(last_synced_block_file, target_block)
            last_synced_block = target_block
        except (GoogleAPIError, RuntimeError, OSError, IOError, TypeError, NameError, ValueError) as e:
            logging.info('An exception occurred {}'.format(repr(e)))

        if blocks_to_sync != max_batch_size:
            logging.info('Sleeping {} seconds...'.format(period_seconds))
            time.sleep(period_seconds)
