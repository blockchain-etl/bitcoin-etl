# The MIT License (MIT)
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
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

import decimal
import json

from bitcoinetl.rpc.request import make_post_request


class BitcoinRpc:

    def __init__(self, provider_uri, timeout=60):
        self.provider_uri = provider_uri
        self.timeout = timeout

    def batch(self, commands):
        rpc_calls = []
        for command in commands:
            m = command.pop(0)
            rpc_calls.append({"jsonrpc": "2.0", "method": m, "params": command, "id": "1"})
        text = json.dumps(rpc_calls)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            self.provider_uri,
            request_data,
            timeout=self.timeout
        )

        response = self._decode_rpc_response(raw_response)

        result = []
        for resp_item in response:
            if resp_item.get('result') is None:
                raise ValueError('"result" is None in the JSON RPC response {}. Request: {}', resp_item.get('error'), text)
            result.append(resp_item.get('result'))
        return result

    def getblockhash(self, param):
        response = self.batch([['getblockhash', param]])
        return response[0] if len(response) > 0 else None

    def getblock(self, param):
        response = self.batch([['getblock', param]])
        return response[0] if len(response) > 0 else None

    def getblockcount(self):
        response = self.batch([['getblockcount']])
        return response[0] if len(response) > 0 else None

    def _decode_rpc_response(self, response):
        response_text = response.decode('utf-8')
        return json.loads(response_text, parse_float=decimal.Decimal)
