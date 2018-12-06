# The MIT License (MIT)
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
import base64
import json
from json import JSONDecodeError

from web3 import HTTPProvider
from web3.utils.request import make_post_request

from bitcoinetl.providers.authproxy import AuthServiceProxy
import logging

logging.getLogger("BitcoinRPC").setLevel(logging.INFO)


# class BatchRPCProvider():
#     def __init__(self, rpc_user, rpc_password, rpc_host, rpc_port):
#         self.rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_host, rpc_port))
#
#     def make_request(self, commands):
#         response = self.rpc_connection.batch_(commands)
#         return response
#
#     def getblockhash(self, param):
#         response = self.rpc_connection.getblockhash(param)
#         return response
#
#     def getblock(self, *param):
#         response = self.rpc_connection.getblock(*param)
#         return response
#
#     def getblockcount(self, *param):
#         response = self.rpc_connection.getblockcount(*param)
#         return response

class BatchRPCProvider(HTTPProvider):

    def __init__(self, rpc_user, rpc_password, rpc_host, rpc_port):
        self.rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_host, rpc_port))

    def make_request(self, commands):
        user = "a"
        passwd = "a"
        try:
            user = user.encode('utf8')
        except AttributeError:
            pass
        try:
            passwd = passwd.encode('utf8')
        except AttributeError:
            pass
        authpair = user + b':' + passwd
        auth_header = b'Basic ' + base64.b64encode(authpair)

        rpc_calls = []
        for command in commands:
            m = command.pop(0)
            rpc_calls.append({"jsonrpc": "2.0", "method": m, "params": command, "id": "1"})
        text = json.dumps(rpc_calls)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            "http://localhost:8332/",
            request_data,
            headers={
                'Authorization': auth_header
            },
            timeout=60
        )

        try:
            response = self.decode_rpc_response(raw_response)
        except JSONDecodeError as error:
            open('error.out', 'w+').write(text + " ================= " + error.doc)
            raise

        result = []
        for resp_item in response:
            result.append(resp_item.get('result'))
        return result
