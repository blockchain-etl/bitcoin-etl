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


import click

from datetime import datetime
from web3 import Web3

from blockchainetl.file_utils import smart_open
from blockchainetl.logging_utils import logging_basic_config
from bitcoinetl.providers.auto import get_provider
from bitcoinetl.service.bitcoin_service import BtcService
# from bitcoinetl.utils import check_classic_provider_uri

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-t', '--rpc-host', default='localhost', type=str, help='The URI of the remote bitcoin node')
@click.option('-u', '--rpc-user', required=True, default=None, type=str, help='The RPC username of the bitcoin node')
@click.option('-p', '--rpc-pass', required=True, default=None, type=str, help='The RPC password of the bitcoin node')
@click.option('-o', '--rpc-port', default=8332, type=int, help='The RPC port of the bitcoin node')
@click.option('-d', '--date', required=True, type=lambda d: datetime.strptime(d, '%Y-%m-%d'),
              help='The date e.g. 2018-01-01.')
@click.option('-o', '--output', default='-', type=str, help='The output file. If not specified stdout is used.')

def get_block_range_for_date(rpc_host, rpc_user, rpc_pass, rpc_port, date, output):
    """Outputs start and end blocks for given date."""
   
    rpc_connection = get_provider(rpc_host, rpc_port, rpc_user, rpc_pass)
    btc_service = BtcService(rpc_connection)

    start_block, end_block = btc_service.get_block_range_for_date(date)

    with smart_open(output, 'w') as output_file:
        output_file.write('{},{}\n'.format(start_block, end_block))
