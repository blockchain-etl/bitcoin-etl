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
        self.hash = None
        self.size = None
        self.virtual_size = None
        self.version = None
        self.lock_time = None
        self.block_number = None
        self.block_hash = None
        self.block_timestamp = None
        self.is_coinbase = False
        self.index = None

        self.inputs = []
        self.outputs = []

        # Only for Zcash
        self.join_splits = []
        self.value_balance = 0

    def add_input(self, input):
        if len(self.inputs) > 0:
            input.index = self.inputs[len(self.inputs) - 1].index + 1
            self.inputs.append(input)
        else:
            input.index = 0
            self.inputs.append(input)

    def add_output(self, output):
        if len(self.outputs) > 0:
            output.index = self.outputs[len(self.outputs) - 1].index + 1
            self.outputs.append(output)
        else:
            output.index = 0
            self.outputs.append(output)

    def calculate_input_value(self):
        return sum([input.value for input in self.inputs if input.value is not None])

    def calculate_output_value(self):
        return sum([output.value for output in self.outputs if output.value is not None])

    def calculate_fee(self):
        if self.is_coinbase:
            return 0
        else:
            return self.calculate_input_value() - self.calculate_output_value()
