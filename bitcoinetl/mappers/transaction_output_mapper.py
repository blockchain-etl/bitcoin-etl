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

from bitcoinetl.btc_utils import bitcoin_to_satoshi
from bitcoinetl.domain.transaction_output import BtcTransactionOutput


class BtcTransactionOutputMapper(object):

    def vout_to_outputs(self, vout):
        outputs = []
        for item in (vout or []):
            output = self.json_dict_to_output(item)
            outputs.append(output)
        return outputs

    def json_dict_to_output(self, json_dict):
        output = BtcTransactionOutput()

        output.index = json_dict.get('n')
        output.addresses = json_dict.get('addresses')
        output.txinwitness = json_dict.get('txinwitness')
        output.value = bitcoin_to_satoshi(json_dict.get('value'))
        if 'scriptPubKey' in json_dict:
            script_pub_key = json_dict.get('scriptPubKey')
            output.script_asm = script_pub_key.get('asm')
            output.script_hex = script_pub_key.get('hex')
            output.required_signatures = script_pub_key.get('reqSigs')
            output.type = script_pub_key.get('type')
            if script_pub_key.get('addresses') is not None and len(script_pub_key.get('addresses')) > 0:
                output.addresses = script_pub_key.get('addresses')
            elif script_pub_key.get('address') is None:
                output.addresses = []
            else:
                output.addresses = [script_pub_key.get('address')]

        return output

    def outputs_to_dicts(self, outputs):
        result = []
        for output in outputs:
            item = {
                'index': output.index,
                'script_asm': output.script_asm,
                'script_hex': output.script_hex,
                'required_signatures': output.required_signatures,
                'type': output.type,
                'addresses': output.addresses,
                'value': output.value
            }
            result.append(item)
        return result

    def dicts_to_outputs(self, dicts):
        result = []
        for dict in dicts:
            input = BtcTransactionOutput()
            input.index = dict.get('index')
            input.script_asm = dict.get('script_asm')
            input.script_hex = dict.get('script_hex')
            input.required_signatures = dict.get('required_signatures')
            input.type = dict.get('type')
            input.addresses = dict.get('addresses')
            input.value = dict.get('value')

            result.append(input)
        return result
