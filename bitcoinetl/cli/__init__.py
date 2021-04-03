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

import click

from bitcoinetl.cli.export_blocks_and_transactions import export_blocks_and_transactions
from bitcoinetl.cli.enrich_transactions import enrich_transactions
from bitcoinetl.cli.export_all import export_all
from bitcoinetl.cli.filter_items import filter_items
from bitcoinetl.cli.get_block_range_for_date import get_block_range_for_date
from bitcoinetl.cli.stream import stream


@click.group()
@click.version_option(version='1.5.0')
@click.pass_context
def cli(ctx):
    pass


# export
cli.add_command(export_blocks_and_transactions, "export_blocks_and_transactions")
cli.add_command(enrich_transactions, "enrich_transactions")
cli.add_command(export_all, "export_all")

# streaming
cli.add_command(stream, "stream")

# utils
cli.add_command(filter_items, "filter_items")
cli.add_command(get_block_range_for_date, "get_block_range_for_date")
