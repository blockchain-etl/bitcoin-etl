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


import click
from bitcoinetl.enumeration.chain import Chain
from bitcoinetl.rpc.bitcoin_rpc import BitcoinRpc

from blockchainetl.logging_utils import logging_basic_config
from blockchainetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-l', '--last-synced-block-file', default='last_synced_block.txt', type=str, help='')
@click.option('--lag', default=0, type=int, help='The number of blocks to lag behind the network.')
@click.option('-p', '--provider-uri', default='http://user:pass@localhost:8332', type=str,
              help='The URI of the remote Bitcoin node')
@click.option('-o', '--output', type=str,
              help='Google PubSub topic path e.g. projects/your-project/topics/bitcoin_blockchain. '
                   'If not specified will print to console')
@click.option('-s', '--start-block', default=None, type=int, help='Start block')
@click.option('-c', '--chain', default=Chain.BITCOIN, type=click.Choice(Chain.ALL), help='The type of chain')
@click.option('-s', '--period-seconds', default=10, type=int, help='How many seconds to sleep between syncs')
@click.option('-b', '--batch-size', default=2, type=int, help='How many blocks to batch in single request')
@click.option('-B', '--block-batch-size', default=10, type=int, help='How many blocks to batch in single sync round')
@click.option('-w', '--max-workers', default=5, type=int, help='The number of workers')
def stream(last_synced_block_file, lag, provider_uri, output, start_block, chain=Chain.BITCOIN,
           period_seconds=10, batch_size=2, block_batch_size=10, max_workers=5):
    """Streams all data types to console or Google Pub/Sub."""
    from bitcoinetl.streaming.streaming_utils import get_item_exporter
    from bitcoinetl.streaming.stream import stream as do_stream

    do_stream(
        bitcoin_rpc=ThreadLocalProxy(lambda: BitcoinRpc(provider_uri)),
        last_synced_block_file=last_synced_block_file,
        lag=lag,
        item_exporter=get_item_exporter(output),
        start_block=start_block,
        chain=chain,
        period_seconds=period_seconds,
        batch_size=batch_size,
        block_batch_size=block_batch_size,
        max_workers=max_workers
    )
