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


from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter


BLOCK_FIELDS_TO_EXPORT = [
    "hash",
    "number",
    "timestamp",
    "median_timestamp",
    "merkle_root",
    "coinbase_param",
    "coinbase_param_decoded",
    "coinbase_txid",
    "previous_block_hash",
    "next_block_hash",
    "nonce",
    "difficulty",
    "chain_work",
    "version",
    "version_hex",
    "size",
    "stripped_size",
    "weight",
    "bits",
    "transaction_count",
    "transaction_fees",
    "block_reward",
    "input_value",
    "transaction_ids",
    "coin_price_usd",
]


TRANSACTION_FIELDS_TO_EXPORT = [
    'transaction_id',
    'hash',
    'block_number',
    'block_hash',
    'block_timestamp',
    'is_coinbase',
    'lock_time',
    'size',
    'virtual_size',
    'weight',
    'version',
    'index',
    'input_count',
    'output_count',
    'input_value',
    'output_value',
    'inputs',
    'outputs',
    'coin_price_usd',
]


def blocks_and_transactions_item_exporter(blocks_output=None, transactions_output=None):
    filename_mapping = {}
    field_mapping = {}

    if blocks_output is not None:
        filename_mapping['block'] = blocks_output
        field_mapping['block'] = BLOCK_FIELDS_TO_EXPORT

    if transactions_output is not None:
        filename_mapping['transaction'] = transactions_output
        field_mapping['transaction'] = TRANSACTION_FIELDS_TO_EXPORT

    return CompositeItemExporter(
        filename_mapping=filename_mapping,
        field_mapping=field_mapping
    )
