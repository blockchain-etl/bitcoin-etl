# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, Omidiora Samuel evge.medvedev@gmail.com, samparsky@gmail.com
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

from bitcoinetl.enumeration.chain import Chain, CoinPriceType
from bitcoinetl.jobs.export_blocks_job import ExportBlocksJob
from bitcoinetl.jobs.exporters.blocks_and_transactions_item_exporter import blocks_and_transactions_item_exporter
from bitcoinetl.rpc.bitcoin_rpc import BitcoinRpc
from blockchainetl.logging_utils import logging_basic_config
from blockchainetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-b', '--batch-size', default=1, type=int, help='The number of blocks to export at a time.')
@click.option('-p', '--provider-uri', default='http://user:pass@localhost:8332', type=str,
              help='The URI of the remote Bitcoin node')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--blocks-output', default=None, type=str,
              help='The output file for blocks. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--transactions-output', default=None, type=str,
              help='The output file for transactions. '
                   'If not provided transactions will not be exported. Use "-" for stdout')
@click.option('-c', '--chain', default=Chain.BITCOIN, type=click.Choice(Chain.ALL),
              help='The type of chain')
@click.option('--coin-price-type', default=CoinPriceType.empty, type=int,
              help='Enable querying CryptoCompare for coin prices. 0 for no price, 1 for daily price, 2 for hourly price.')
def export_blocks_and_transactions(start_block, end_block, batch_size, provider_uri,
                                   max_workers, blocks_output, transactions_output, chain,
                                   coin_price_type):
    """Export blocks and transactions."""
    if blocks_output is None and transactions_output is None:
        raise ValueError('Either --blocks-output or --transactions-output options must be provided')

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        bitcoin_rpc=ThreadLocalProxy(lambda: BitcoinRpc(provider_uri)),
        max_workers=max_workers,
        item_exporter=blocks_and_transactions_item_exporter(blocks_output, transactions_output),
        chain=chain,
        export_blocks=blocks_output is not None,
        export_transactions=transactions_output is not None,
        coin_price_type=coin_price_type
    )
    job.run()
