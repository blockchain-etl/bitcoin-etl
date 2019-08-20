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

import pytest

from bitcoinetl.jobs.export_blocks_job import ExportBlocksJob
from bitcoinetl.jobs.exporters.blocks_and_transactions_item_exporter import blocks_and_transactions_item_exporter
from tests.bitcoinetl.job.helpers import get_bitcoin_rpc
from blockchainetl.thread_local_proxy import ThreadLocalProxy

import tests.resources
from tests.helpers import compare_lines_ignore_order, read_file, skip_if_slow_tests_disabled

RESOURCE_GROUP = 'test_export_blocks_job'


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize("start_block, end_block, batch_size, resource_group, provider_type, chain", [
    (0, 0, 1, 'bitcoin/block_0', 'mock', 'bitcoin'),
    skip_if_slow_tests_disabled([0, 0, 1, 'bitcoin/block_0', 'online', 'bitcoin']),
    (1, 1, 1, 'bitcoin/block_1', 'mock', 'bitcoin'),
    skip_if_slow_tests_disabled([1, 1, 1, 'bitcoin/block_1', 'online', 'bitcoin']),
    (50000, 50000, 1, 'bitcoin/block_without_transactions', 'mock', 'bitcoin'),
    skip_if_slow_tests_disabled([50000, 50000, 1, 'bitcoin/block_without_transactions', 'online', 'bitcoin']),
    (50001, 50002, 2, 'bitcoin/block_with_transactions', 'mock', 'bitcoin'),
    skip_if_slow_tests_disabled([50001, 50002, 2, 'bitcoin/block_with_transactions', 'online', 'bitcoin']),
    (2, 2, 1, 'dogecoin/block_without_transactions', 'mock', 'dogecoin'),
    skip_if_slow_tests_disabled([107212, 107212, 1, 'dogecoin/block_with_float_precision_loss', 'online', 'dogecoin'],
                                chain='dogecoin'),
    (0, 0, 1, 'zcash/block_0', 'mock', 'zcash'),
    skip_if_slow_tests_disabled([0, 0, 1, 'zcash/block_0', 'online', 'zcash'],
                                chain='zcash'),
    (508, 508, 1, 'zcash/block_with_shielded_addresses', 'mock', 'zcash'),
    skip_if_slow_tests_disabled([508, 508, 1, 'zcash/block_with_shielded_addresses', 'online', 'zcash'],
                                chain='zcash'),
    (462085, 462085, 1, 'zcash/block_with_value_balance', 'mock', 'zcash'),
    skip_if_slow_tests_disabled([462085, 462085, 1, 'zcash/block_with_value_balance', 'online', 'zcash'],
                                chain='zcash'),
    (91722, 91722, 1, 'bitcoin_cash/block_with_duplicate_txid', 'mock', 'bitcoin_cash'),
    skip_if_slow_tests_disabled([91722, 91722, 1, 'bitcoin_cash/block_with_duplicate_txid', 'online', 'bitcoin_cash'],
                                chain='bitcoin_cash'),
])
def test_export_blocks_job(tmpdir, start_block, end_block, batch_size, resource_group, provider_type, chain):
    blocks_output_file = str(tmpdir.join('actual_block.json'))
    transactions_output_file = str(tmpdir.join("actual_transactions.json"))

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        bitcoin_rpc=ThreadLocalProxy(
            lambda: get_bitcoin_rpc(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file),
                chain=chain)),
        max_workers=5,
        item_exporter=blocks_and_transactions_item_exporter(blocks_output_file, transactions_output_file),
        chain=chain,
        export_blocks=blocks_output_file is not None,
        export_transactions=transactions_output_file is not None)
    job.run()

    print('=====================')
    print(read_file(blocks_output_file))
    compare_lines_ignore_order(
        read_resource(resource_group, 'expected_blocks.json'), read_file(blocks_output_file)
    )

    print('=====================')
    print(read_file(transactions_output_file))
    compare_lines_ignore_order(
        read_resource(resource_group, 'expected_transactions.json'), read_file(transactions_output_file)
    )
