# MIT License
#
# Copyright (c) 2018 Omidiora Samuel, Evgeny Medvedev, evge.medvedev@gmail.com, samparsky@gmail.com
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

import datetime
import json
import logging
import os
import shutil
from time import time

from bitcoinetl.jobs.export_blocks_job import ExportBlocksJob
from bitcoinetl.jobs.enrich_transactions import EnrichTransactionsJob
from bitcoinetl.jobs.exporters.blocks_and_transactions_item_exporter import blocks_and_transactions_item_exporter
from bitcoinetl.rpc.bitcoin_rpc import BitcoinRpc
from blockchainetl.file_utils import smart_open
from blockchainetl.logging_utils import logging_basic_config
from blockchainetl.misc_utils import filter_items
from blockchainetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()
logger = logging.getLogger('export_all')


def export_all(chain, partitions, output_dir, provider_uri, max_workers, batch_size, enrich):
    for batch_start_block, batch_end_block, partition_dir, *args in partitions:
        # # # start # # #

        start_time = time()

        padded_batch_start_block = str(batch_start_block).zfill(8)
        padded_batch_end_block = str(batch_end_block).zfill(8)
        block_range = '{padded_batch_start_block}-{padded_batch_end_block}'.format(
            padded_batch_start_block=padded_batch_start_block,
            padded_batch_end_block=padded_batch_end_block,
        )
        file_name_suffix = '{padded_batch_start_block}_{padded_batch_end_block}'.format(
            padded_batch_start_block=padded_batch_start_block,
            padded_batch_end_block=padded_batch_end_block,
        )

        # # # blocks_and_transactions # # #

        blocks_output_dir = '{output_dir}/blocks{partition_dir}'.format(
            output_dir=output_dir,
            partition_dir=partition_dir,
        )
        os.makedirs(os.path.dirname(blocks_output_dir), exist_ok=True)

        transactions_output_dir = '{output_dir}/transactions{partition_dir}'.format(
            output_dir=output_dir,
            partition_dir=partition_dir,
        )
        os.makedirs(os.path.dirname(transactions_output_dir), exist_ok=True)

        blocks_file = '{blocks_output_dir}/blocks_{file_name_suffix}.json'.format(
            blocks_output_dir=blocks_output_dir,
            file_name_suffix=file_name_suffix,
        )
        transactions_file = '{transactions_output_dir}/transactions_{file_name_suffix}.json'.format(
            transactions_output_dir=transactions_output_dir,
            file_name_suffix=file_name_suffix,
        )
        enriched_transactions_file = '{transactions_output_dir}/enriched_transactions_{file_name_suffix}.json'.format(
            transactions_output_dir=transactions_output_dir,
            file_name_suffix=file_name_suffix,
        )
        logger.info('Exporting blocks {block_range} to {blocks_file}'.format(
            block_range=block_range,
            blocks_file=blocks_file,
        ))
        logger.info('Exporting transactions from blocks {block_range} to {transactions_file}'.format(
            block_range=block_range,
            transactions_file=transactions_file,
        ))

        job = ExportBlocksJob(
            chain=chain,
            start_block=batch_start_block,
            end_block=batch_end_block,
            batch_size=batch_size,
            bitcoin_rpc=ThreadLocalProxy(lambda: BitcoinRpc(provider_uri)),
            max_workers=max_workers,
            item_exporter=blocks_and_transactions_item_exporter(blocks_file, transactions_file),
            export_blocks=blocks_file is not None,
            export_transactions=transactions_file is not None)
        job.run()

        if enrich == True:
            with smart_open(transactions_file, 'r') as transactions_file:
                job = EnrichTransactionsJob(
                    transactions_iterable = (json.loads(transaction) for transaction in transactions_file),
                    batch_size = batch_size,
                    bitcoin_rpc = ThreadLocalProxy(lambda: BitcoinRpc(provider_uri)),
                    max_workers = max_workers,
                    item_exporter = blocks_and_transactions_item_exporter(None, enriched_transactions_file),
                    chain = chain
                )
                job.run()


        if args is not None and len(args) > 0:
            date = args[0]
            logger.info('Filtering blocks {blocks_file} by date {date}'.format(
                blocks_file=blocks_file,
                date=date,
            ))

            def filter_by_date(item, field):
                return datetime.datetime.fromtimestamp(item[field]).astimezone(datetime.timezone.utc) \
                           .strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d')

            filtered_blocks_file = blocks_file + '.filtered'
            filter_items(blocks_file, filtered_blocks_file, lambda item: filter_by_date(item, 'timestamp'))
            shutil.move(filtered_blocks_file, blocks_file)

            logger.info('Filtering transactions {transactions_file} by date {date}'.format(
                transactions_file=transactions_file,
                date=date,
            ))

            filtered_transactions_file = transactions_file + '.filtered'
            filter_items(transactions_file, filtered_transactions_file, lambda item: filter_by_date(item, 'block_timestamp'))
            shutil.move(filtered_transactions_file, transactions_file)

        # # # finish # # #
        end_time = time()
        time_diff = round(end_time - start_time, 5)
        logger.info('Exporting blocks {block_range} took {time_diff} seconds'.format(
            block_range=block_range,
            time_diff=time_diff,
        ))
