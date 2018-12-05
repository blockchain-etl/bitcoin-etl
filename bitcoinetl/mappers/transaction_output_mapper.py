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
import math

from bitcoinetl.domain.transaction_output import BtcTransactionOutput


class BtcTransactionOutputMapper(object):
    def json_dict_to_output(self, json_dict):
        result = []
        for item in json_dict.get('vout'):
            output = BtcTransactionOutput()

            output.addresses = item.get('addresses')
            output.txinwitness = item.get('txinwitness')
            output.sequence = item.get('sequence')
            output.value = item.get('value')
            output.n = item.get('n')
            if "scriptPubKey" in item:
                script_pub_key = item.get('scriptPubKey')
                output.asm = script_pub_key.get('asm')
                output.hex = script_pub_key.get('hex')
                output.req_sigs = script_pub_key.get('reqSigs')
                output.addresses = script_pub_key.get('addresses')
            result.append(output)
        return result

    def output_to_dict(self, outputs):
        result = []
        for output in outputs:
            item = {
                "addresses": output.addresses,
                "asm": output.asm,
                "hex": output.hex,
                "req_sigs": output.req_sigs,
                "sequence": output.sequence,
                "value": int(int(output.value) * math.pow(10, 8)),
                "n": output.n
            }
            result.append(item)
        return result
