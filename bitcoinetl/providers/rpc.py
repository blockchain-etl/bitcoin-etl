# The MIT License (MIT)
#
# Copyright (c) 2018 Omidiora Samuel
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

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

# from web3 import HTTPProvider
# from web3.utils.request import make_post_request

# from pythonbitconi

# Mostly copied from web3.py/providers/rpc.py. Supports batch requests.
# Will be removed once batch feature is added to web3.py https://github.com/ethereum/web3.py/issues/832
class BatchRPCProvider():
    def __init__(self, rpc_user, rpc_password, rpc_host, rpc_port ):
        self.rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_host, rpc_port))

    def make_request(self, commands):
        print(self.rpc_connection.getinfo())
        response = self.rpc_connection.batch_(commands)
        return response

        # self.logger.debug("Making request HTTP. URI: %s, Request: %s",
        #                   self.endpoint_uri, text)
        # request_data = text.encode('utf-8')
        # raw_response = make_post_request(
        #     self.endpoint_uri,
        #     request_data,
        #     **self.get_request_kwargs()
        # )
        # response = self.decode_rpc_response(raw_response)
        # self.logger.debug("Getting response HTTP. URI: %s, "
        #                   "Request: %s, Response: %s",
        #                   self.endpoint_uri, text, response)
