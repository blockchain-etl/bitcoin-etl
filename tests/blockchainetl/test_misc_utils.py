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

from blockchainetl.misc_utils import filter_items
from tests.helpers import compare_lines_ignore_order, read_file


def test_filter_items(tmpdir):
    input_file = str(tmpdir.join('input.json'))
    open(input_file, 'w').write('''{"field1": "x1", "field2": "y1"}    
{"field1": "x2", "field2": "y2"}    
''')

    output_file = str(tmpdir.join('output.json'))
    filter_items(input_file, output_file, lambda item: item['field1'] == 'x1')

    expected_file = str(tmpdir.join('expected.json'))
    open(expected_file, 'w').write('''{"field1": "x1", "field2": "y1"}     
''')

    compare_lines_ignore_order(
        read_file(expected_file), read_file(output_file)
    )
