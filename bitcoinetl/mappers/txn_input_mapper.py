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


from bitcoinetl.domain.transaction import TxnInput


class BtcTransactionInputMapper(object):
    def json_dict_to_input(self, json_dict):
        result = []

        for item in json_dict.get('vin'):
            vin = TxnInput()

            vin.txid = item.get('txid')
            vin.vout = item.get('vout')
            vin.coinbase = item.get('coinbase')
            vin.txinwitness = item.get('txinwitness')
            vin.sequence = item.get('sequence')
            vin.value = item.get('value')
            if "scriptSig" in item:
                vin.asm = (item.get('scriptSig')).get('asm')
                vin.hex = (item.get('scriptSig')).get('hex')
            result.append(vin)

        return result

    def input_to_dict(self, vins):
        result = []
        for item in vins:
            vin = {
                "txid": item.txid,
                "vout": item.vout,
                "asm": item.asm,
                "hex": item.hex,
                "coinbase": item.coinbase,
                "tx_in_witness": item.txinwitness,
                "sequence": item.sequence,
                "value": item.value,
            }
            result.append(vin)
        return result
