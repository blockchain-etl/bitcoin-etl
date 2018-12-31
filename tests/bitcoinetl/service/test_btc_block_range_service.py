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

import pytest
from dateutil.parser import parse

from bitcoinetl.service.btc_block_range_service import BtcBlockRangeService
from blockchainetl.service.graph_operations import OutOfBoundsError
from tests.bitcoinetl.job.helpers import get_bitcoin_rpc
from tests.helpers import skip_if_slow_tests_disabled


@pytest.mark.parametrize("chain,date,expected_start_block,expected_end_block", [
    skip_if_slow_tests_disabled(['bitcoin', '2009-01-03', 0, 0], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2009-01-09', 1, 14], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2009-03-01', 5924, 6028], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2009-05-06', 13448, 13582], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2009-05-07', 13583, 13704], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2009-05-08', 13705, 13811], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2009-06-05', 16534, 16563], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2013-10-09', 262452, 262645], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2014-04-18', 296393, 296552], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2014-04-19', 296553, 296711], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', '2017-01-02', 446189, 446347], chain='bitcoin'),
    skip_if_slow_tests_disabled(['dogecoin', '2014-01-20', 63869, 65347], chain='dogecoin'),
    skip_if_slow_tests_disabled(['dogecoin', '2014-01-21', 65322, 66853], chain='dogecoin'),
    skip_if_slow_tests_disabled(['litecoin', '2011-10-07', 0, 0], chain='litecoin'),
    skip_if_slow_tests_disabled(['dash', '2014-01-19', 0, 4138], chain='dash'),
    skip_if_slow_tests_disabled(['zcash', '2016-10-28', 0, 629], chain='zcash'),
])
def test_get_block_range_for_date(chain, date, expected_start_block, expected_end_block):
    btc_block_range_service = get_new_btc_block_range_service(chain)
    parsed_date = parse(date)
    blocks = btc_block_range_service.get_block_range_for_date(parsed_date)
    assert blocks == (expected_start_block, expected_end_block)


@pytest.mark.parametrize("chain,date", [
    skip_if_slow_tests_disabled(['bitcoin','2030-01-01'], chain='bitcoin')
])
def test_get_block_range_for_date_fail(chain, date):
    btc_service = get_new_btc_block_range_service(chain)
    parsed_date = parse(date)
    with pytest.raises(OutOfBoundsError):
        btc_service.get_block_range_for_date(parsed_date)


@pytest.mark.parametrize("chain,start_timestamp,end_timestamp,expected_start_block,expected_end_block", [
    skip_if_slow_tests_disabled(['bitcoin', 1235952055, 1235995140, 6029, 6082], chain='bitcoin'),
    skip_if_slow_tests_disabled(['bitcoin', 1328227200, 1328248800, 165081,165132], chain='bitcoin'),
])
def test_get_block_range_for_timestamps(chain, start_timestamp, end_timestamp, expected_start_block, expected_end_block):
    eth_service = get_new_btc_block_range_service(chain)
    blocks = eth_service.get_block_range_for_timestamps(start_timestamp, end_timestamp)
    assert blocks == (expected_start_block, expected_end_block)


def get_new_btc_block_range_service(chain):
    rpc = get_bitcoin_rpc("online", chain=chain)
    return BtcBlockRangeService(rpc)
