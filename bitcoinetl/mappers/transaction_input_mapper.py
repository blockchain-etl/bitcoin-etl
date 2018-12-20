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


from bitcoinetl.domain.transaction_input import BtcTransactionInput


class BtcTransactionInputMapper(object):
    def json_dict_to_input(self, json_dict):
        result = []

        index = 0
        for item in json_dict.get('vin', []):
            input = BtcTransactionInput()

            input.index = index
            index = index + 1
            input.spent_transaction_hash = item.get('txid')
            input.spent_output_index = item.get('vout')
            input.coinbase_param = item.get('coinbase')
            input.sequence = item.get('sequence')
            input.value = item.get('value')
            if 'scriptSig' in item:
                input.script_asm = (item.get('scriptSig')).get('asm')
                input.script_hex = (item.get('scriptSig')).get('hex')
            result.append(input)

        return result

    def input_to_dict(self, inputs):
        result = []
        for input in inputs:
            item = {
                'index': input.index,
                'spent_transaction_hash': input.spent_transaction_hash,
                'spent_output_index': input.spent_output_index,
                'script_asm': input.script_asm,
                'script_hex': input.script_hex,
                'sequence': input.sequence,
                'value': input.value,
            }
            result.append(item)
        return result
