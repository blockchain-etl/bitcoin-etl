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

from blockchainetl.service.graph_operations import GraphOperations, Point

SIMPLE_GRAPH = {
    0: 100,
    1: 200,
    2: 300,
    3: 400,
    4: 500,
}

NON_MONOTONIC_GRAPH = {
    0: 100,
    1: 200,
    2: 300,
    3: 400,
    4: 350,
    5: 340,
    6: 360,
    7: 410,
}


@pytest.mark.parametrize('graph, y, expected_bounds', [
    (SIMPLE_GRAPH, 250, (1, 2)),
    (SIMPLE_GRAPH, 400, (3, 3)),
    (SIMPLE_GRAPH, 100, (0, 0)),
    (SIMPLE_GRAPH, 101, (0, 1)),
    (NON_MONOTONIC_GRAPH, 345, (5, 3)),
    (NON_MONOTONIC_GRAPH, 330, (2, 3)),
    (NON_MONOTONIC_GRAPH, 400, (6, 3)),
    (NON_MONOTONIC_GRAPH, 340, (5, 3)),
])
def test_get_bounds_for_y_coordinate_simple(graph, y, expected_bounds):
    graph = MockGraph(graph)
    graph_operations = GraphOperations(graph)
    bounds = graph_operations.get_bounds_for_y_coordinate(y)
    assert bounds == expected_bounds


class MockGraph(object):
    def __init__(self, points_dict):
        self.points = [Point(x, y) for x, y in points_dict.items()]

    def get_first_point(self):
        return self.points[0] if len(self.points) > 0 else None

    def get_last_point(self):
        return self.points[len(self.points) - 1] if len(self.points) > 0 else None

    def get_point(self, x):
        if len(self.points) <= x:
            raise ValueError('Out of bounds')
        return self.points[x]

    def get_points(self, xs):
        return [self.get_point(x) for x in xs]
