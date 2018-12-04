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

from bitcoinetl.jobs.export_blocks_job import ExportBlocksJob
from bitcoinetl.providers.auto import get_provider
from bitcoinetl.jobs.exporters.blocks_and_transactions_item_exporter import blocks_and_transactions_item_exporter
from blockchainetl.logging_utils import logging_basic_config
from blockchainetl.thread_local_proxy import ThreadLocalProxy

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-b', '--batch-size', default=1, type=int, help='The number of blocks to export at a time.')
@click.option('-t', '--rpc-host', default='localhost', type=str, help='The URI of the remote bitcoin node')
@click.option('-u', '--rpc-user', required=True, default=None, type=str, help='The RPC username of the bitcoin node')
@click.option('-p', '--rpc-pass', required=True, default=None, type=str, help='The RPC password of the bitcoin node')
@click.option('-o', '--rpc-port', default=8332, type=int, help='The RPC port of the bitcoin node')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--blocks-output', default=None, type=str,
              help='The output file for blocks. '
                   'If not provided blocks will not be exported. Use "-" for stdout')
@click.option('--transactions-output', default=None, type=str,
              help='The output file for transactions. '
                   'If not provided transactions will not be exported. Use "-" for stdout')
def export_blocks_and_transactions(start_block, end_block, batch_size, rpc_host, rpc_user, rpc_pass, rpc_port,
                                   max_workers, blocks_output, transactions_output):
    """Export blocks and transactions."""
    if blocks_output is None and transactions_output is None:
        raise ValueError('Either --blocks-output or --transactions-output options must be provided')

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        batch_rpc_provider=ThreadLocalProxy(lambda: get_provider(rpc_host, rpc_port, rpc_user, rpc_pass)),
        max_workers=max_workers,
        item_exporter=blocks_and_transactions_item_exporter(blocks_output, transactions_output),
        export_blocks=blocks_output is not None,
        export_transactions=transactions_output is not None)
    job.run()
