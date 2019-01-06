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

from bitcoinetl.btc_utils import bitcoin_to_satoshi
from bitcoinetl.domain.join_split import BtcJoinSplit


class BtcJoinSplitMapper(object):
    def vjoinsplit_to_join_splits(self, vjoinsplit):
        join_splits = []
        index = 0
        for item in (vjoinsplit or []):
            join_split = self.json_dict_to_join_split(item)
            join_split.index = index
            index = index + 1
            join_splits.append(join_split)

        return join_splits

    def json_dict_to_join_split(self, json_dict):
        join_split = BtcJoinSplit()

        join_split.public_input_value = bitcoin_to_satoshi(json_dict.get('vpub_new'))
        join_split.public_output_value = bitcoin_to_satoshi(json_dict.get('vpub_old'))

        return join_split
