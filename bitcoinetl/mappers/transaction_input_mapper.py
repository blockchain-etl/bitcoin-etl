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
    def vin_to_inputs(self, vin):
        inputs = []
        index = 0
        for item in (vin or []):
            input = self.json_dict_to_input(item)
            input.index = index
            index = index + 1
            inputs.append(input)

        return inputs

    def json_dict_to_input(self, json_dict):
        input = BtcTransactionInput()

        input.spent_transaction_hash = json_dict.get('txid')
        input.spent_output_index = json_dict.get('vout')
        input.coinbase_param = json_dict.get('coinbase')
        input.sequence = json_dict.get('sequence')
        if 'scriptSig' in json_dict:
            input.script_asm = (json_dict.get('scriptSig')).get('asm')
            input.script_hex = (json_dict.get('scriptSig')).get('hex')

        return input

    def inputs_to_dicts(self, inputs):
        result = []
        for input in inputs:
            item = {
                'index': input.index,
                'spent_transaction_hash': input.spent_transaction_hash,
                'spent_output_index': input.spent_output_index,
                'script_asm': input.script_asm,
                'script_hex': input.script_hex,
                'sequence': input.sequence,
                'required_signatures': input.required_signatures,
                'type': input.type,
                'addresses': input.addresses,
                'value': input.value,
            }
            result.append(item)
        return result

    def dicts_to_inputs(self, dicts):
        result = []
        for dict in dicts:
            input = BtcTransactionInput()
            input.index = dict.get('index')
            input.spent_transaction_hash = dict.get('spent_transaction_hash')
            input.spent_output_index = dict.get('spent_output_index')
            input.script_asm = dict.get('script_asm')
            input.script_hex = dict.get('script_hex')
            input.sequence = dict.get('sequence')
            input.required_signatures = dict.get('required_signatures')
            input.type = dict.get('type')
            input.addresses = dict.get('addresses')
            input.value = dict.get('value')

            result.append(input)
        return result
