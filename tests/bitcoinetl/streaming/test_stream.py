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
import os

import pytest

from bitcoinetl.streaming.btc_streamer_adapter import BtcStreamerAdapter
from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter
from blockchainetl.streaming.streamer import Streamer

import tests.resources
from blockchainetl.thread_local_proxy import ThreadLocalProxy
from tests.bitcoinetl.job.helpers import get_bitcoin_rpc
from tests.helpers import compare_lines_ignore_order, read_file, skip_if_slow_tests_disabled

RESOURCE_GROUP = 'test_export_blocks_job'


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize("start_block, end_block, batch_size, resource_group ,provider_type,chain", [
    (50001, 50002, 1, 'bitcoin/stream_50001_50002', 'mock', 'bitcoin'),
    skip_if_slow_tests_disabled([50001, 50002, 1, 'bitcoin/stream_50001_50002', 'online', 'bitcoin']),
])
def test_stream(tmpdir, start_block, end_block, batch_size, resource_group, provider_type, chain):
    try:
        os.remove('last_synced_block.txt')
    except OSError:
        pass

    blocks_output_file = str(tmpdir.join('actual_block.json'))
    transactions_output_file = str(tmpdir.join("actual_transactions.json"))

    streamer_adapter = BtcStreamerAdapter(
        bitcoin_rpc=ThreadLocalProxy(
            lambda: get_bitcoin_rpc(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file),
                chain=chain)),
        batch_size=batch_size,
        item_exporter=CompositeItemExporter(
            filename_mapping={
                'block': blocks_output_file,
                'transaction': transactions_output_file,
            }
        ),
    )
    streamer = Streamer(
        blockchain_streamer_adapter=streamer_adapter,
        start_block=start_block,
        end_block=end_block,
        retry_errors=False
    )
    streamer.stream()

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
