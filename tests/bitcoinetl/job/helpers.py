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
import os
from bitcoinetl.providers.rpc import BatchRPCProvider
from tests.bitcoinetl.job.mock_rpc_provider import MockRPCProvider

def get_provider(provider_type, read_resource_lambda=None):
    if provider_type == "mock":
        if read_resource_lambda is None:
            raise ValueError('read_resource_lambda must not be None for provider type {}'.format(provider_type))
        provider = MockRPCProvider(read_resource_lambda)
        
    elif provider_type == "online":

        rpc_username = os.environ.get("RPC_USERNAME")
        rpc_password = os.environ.get("RPC_PASSWORD")
        rpc_host = os.environ.get("RPC_HOST") or "127.0.0.1"
        rpc_port = os.environ.get("RPC_PORT") or 8332
        if rpc_username is None or rpc_password is None:
            raise ValueError('RPC_USERNAME and RPC_PASSWORD are required environment variables')

        provider = BatchRPCProvider(rpc_username, rpc_password, rpc_host, rpc_port)
    return provider
