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
from bitcoinetl.enumeration.chain import Chain


def generate_get_block_by_hash_json_rpc(block_hashes, include_transactions, chain=Chain.BITCOIN):
    for _, block_hash in enumerate(block_hashes):
        if not include_transactions:
            yield ["getblock", block_hash]
        else:
            if chain in Chain.HAVE_OLD_API:
                verbosity = include_transactions
            else:
                verbosity = 2 if include_transactions else 1
            yield ["getblock", block_hash, verbosity]


def generate_get_block_hash_by_number_json_rpc(block_numbers):
    for _, block_number in enumerate(block_numbers):
        yield ["getblockhash", block_number]


def generate_get_transaction_by_id_json_rpc(hashes):
    for hash in hashes:
        yield ["getrawtransaction", hash, 1]
