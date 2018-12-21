# MIT License
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

import pytest

from bitcoinetl.service.btc_script_service import script_hex_to_non_standard_address


@pytest.mark.parametrize('script_hex,expected_address', [
    ('204e0000c93ad870ee0ca407cdc17ddc61c71b12906ad1fa476a9b56', 'nonstandard0cbd12ed8f1b1d8979f7f50d5083e9f21b7f5f78'),
    ('', 'nonstandarde3b0c44298fc1c149afbf4c8996fb92427ae41e4'),
])
def test_script_hex_to_non_standard_address(script_hex, expected_address):
    assert script_hex_to_non_standard_address(script_hex) == expected_address
