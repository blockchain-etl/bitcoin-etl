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


# https://bitcoin.org/en/developer-reference#raw-transaction-format
class BtcTransaction(object):
    def __init__(self):
        # https://bitcoin.stackexchange.com/questions/77699/whats-the-difference-between-txid-and-hash-getrawtransaction-bitcoind
        self.txid = None
        self.hash = None
        self.size = None
        self.virtual_size = None
        self.version = None
        self.lock_time = None
        self.block_height = None
        self.block_hash = None
        self.block_time = None
        # TODO: Add fee
        self.inputs = []
        self.outputs = []
