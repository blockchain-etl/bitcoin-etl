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


from datetime import datetime

import click
from bitcoinetl.rpc.bitcoin_rpc import BitcoinRpc

from bitcoinetl.service.btc_block_range_service import BtcBlockRangeService
from blockchainetl.file_utils import smart_open
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-p', '--provider-uri', default='http://user:pass@localhost:8332', type=str,
              help='The URI of the remote Bitcoin node')
@click.option('-d', '--date', required=True, type=lambda d: datetime.strptime(d, '%Y-%m-%d'),
              help='The date e.g. 2018-01-01.')
@click.option('-s', '--start-hour', default=0, required=False, type=click.IntRange(0, 23, clamp=True),
              help='The start hour in date e.g. 0, which is inclusive (means the block starts at starthour:00:00)')
@click.option('-e', '--end-hour', default=23, required=False, type=click.IntRange(0, 23, clamp=True),
              help='The end hour in date e.g. 23, which is inclusive (means the block ends at endhour:59:59)')
@click.option('-o', '--output', default='-', type=str, help='The output file. If not specified stdout is used.')
def get_block_range_for_date(provider_uri, date, start_hour, end_hour, output):
    """Outputs start and end blocks for given date."""

    if start_hour > end_hour:
        raise ValueError('end_hour should be greater than or equal to start_hour')

    bitcoin_rpc = BitcoinRpc(provider_uri)
    btc_service = BtcBlockRangeService(bitcoin_rpc)

    start_block, end_block = btc_service.get_block_range_for_date(date, start_hour, end_hour)

    with smart_open(output, 'w') as output_file:
        output_file.write('{},{}\n'.format(start_block, end_block))
