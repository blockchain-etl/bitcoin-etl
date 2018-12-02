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
from bitcoinetl.domain.transaction import TxnInput, TxnOutput

class BtcTransactionOutputMapper(object):
    def json_dict_to_output(self, json_dict):
        result = []
        for item in json_dict.get('vout'):
            vout = TxnOutput()

            vout.addresses     = item.get('addresses')
            vout.txinwitness   = item.get('txinwitness')
            vout.sequence      = item.get('sequence')
            vout.value         = item.get('value')
            vout.n             = item.get('n')
            if "scriptSig" in item:
                vout.asm           = (item.get('scriptSig')).get('asm')
                vout.hex           = (item.get('scriptSig')).get('hex')
            result.append(vout)
        return result

    def output_to_dict(self, outputs):
        result = []
        for item in outputs:
            vout = {
                "addresses": item.addresses,
                "asm": item.asm,
                "hex": item.hex,
                "txinwitness": item.txinwitness,
                "sequence": item.sequence,
                "value": int(item.value * math.pow(10, 8)),
                "n": item.n
            }
            result.append(vout)
        return result



