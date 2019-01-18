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


from blockchainetl.utils import pairwise

MAX_ITERATIONS_FIND_POINT_AROUND = 119


class GraphOperations(object):
    def __init__(self, graph):
        """x axis on the graph must be integers"""
        self._graph = graph
        self._cached_points = []

    def get_bounds_for_y_coordinate(self, y):
        """given the y coordinate, outputs a pair of x coordinates for closest points that bound the y coordinate.
        Left and right bounds are equal in case given y is equal to one of the points y coordinate"""
        initial_bounds = find_best_bounds(y, self._cached_points)
        if initial_bounds is None:
            initial_bounds = self._get_first_point(), self._get_last_point()

        bounds = self._get_bounds_for_y_coordinate_recursive(y, *initial_bounds)

        # block times in Bitcoin are not monotonic so need to find other bounds around the found ones
        result = self._find_point_around_y(y, bounds[0], find_below=True, move_left=False), \
                 self._find_point_around_y(y, bounds[1], find_below=False, move_left=True)

        return result

    def _get_bounds_for_y_coordinate_recursive(self, y, start, end):
        if y < start.y or y > end.y:
            raise OutOfBoundsError('y coordinate {} is out of bounds for points {}-{}'.format(y, start, end))

        if y == start.y:
            return start.x, start.x
        elif y == end.y:
            return end.x, end.x
        elif (end.x - start.x) <= 1:
            return start.x, end.x
        else:
            if start.y > end.y:
                raise ValueError('Start y must be lesser or equal to end y coordinate. Was {}, {}'
                                 .format(start.y, end.y))

            # Interpolation Search https://en.wikipedia.org/wiki/Interpolation_search, O(log(log(n)) average case.
            # Improvements for worst case:
            # Find the 1st estimation by linear interpolation from start and end points.
            # If the 1st estimation is below the needed y coordinate (graph is concave),
            # drop the next estimation by interpolating with the start and 1st estimation point
            # (likely will be above the needed y).
            # If 1st estimation is above the needed y coordinate (graph is convex),
            # drop the next estimation by interpolating with the 1st estimation and end point
            # (likely will be below the needed y).

            estimation1_x = interpolate(start, end, y)
            estimation1_x = bound(estimation1_x, (start.x, end.x))
            estimation1 = self._get_point(estimation1_x)

            if estimation1.y < y:
                points = (start, estimation1)
            else:
                points = (estimation1, end)

            estimation2_x = interpolate(*points, y)
            estimation2_x = bound(estimation2_x, (start.x, end.x))
            estimation2 = self._get_point(estimation2_x)

            all_points = [start, estimation1, estimation2, end]

            bounds = find_best_bounds(y, all_points)
            if bounds is None:
                raise ValueError('Unable to find bounds for points {} and y coordinate {}'.format(points, y))

            return self._get_bounds_for_y_coordinate_recursive(y, *bounds)

    def _find_point_around_y(self, y, x, find_below, move_left):
        find_above = not find_below
        move_right = not move_left

        last_point = self._get_last_point()
        point = self._get_point(x)

        next_point = point
        best_point = point
        iteration = 0

        increment = - 1 if move_left else 1
        while iteration < MAX_ITERATIONS_FIND_POINT_AROUND and 0 <= (next_point.x + increment) <= last_point.x:
            prev_point = next_point

            next_point_x = next_point.x + increment

            prefetch_left = min(20 if move_left else 0, next_point_x)
            prefetch_right = min(20 if move_right else 0, max(last_point.x - next_point_x - 1, 0))
            next_point = self._get_point(next_point_x, prefetch_left=prefetch_left, prefetch_right=prefetch_right)

            if find_below and move_left and (next_point.y == y or next_point.y < y < prev_point.y):
                best_point = next_point
            if find_below and move_right and (prev_point.y == y or prev_point.y < y < next_point.y):
                best_point = prev_point
            if find_above and move_left and (prev_point.y == y or next_point.y < y < prev_point.y):
                best_point = prev_point
            if find_above and move_right and (next_point.y == y or prev_point.y < y < next_point.y):
                best_point = next_point

            iteration = iteration + 1

        return best_point.x

    def _find_point_in_cache(self, x):
        for point in self._cached_points:
            if point.x == x:
                return point
        return None

    def _get_point(self, x, prefetch_left=0, prefetch_right=0):
        prefetch_left = max(prefetch_left, 0)
        prefetch_right = max(prefetch_right, 0)
        cached_point = self._find_point_in_cache(x)
        if cached_point is not None:
            return cached_point
        else:
            if prefetch_left == 0 and prefetch_right == 0:
                point = self._graph.get_point(x)
                self._cached_points.append(point)
                return point
            else:
                xs = [x]
                for i in range(x - prefetch_left, x):
                    xs.append(i)
                for i in range(x + 1, x + prefetch_right + 1):
                    xs.append(i)
                points = self._graph.get_points(xs)
                for point in points:
                    self._cached_points.append(point)
                point = [p for p in points if p.x == x][0]
                return point

    def _get_first_point(self):
        point = self._graph.get_first_point()
        self._cached_points.append(point)
        return point

    def _get_last_point(self):
        point = self._graph.get_last_point()
        self._cached_points.append(point)
        return point


def find_best_bounds(y, points):
    sorted_points = sorted(points, key=lambda point: point.x)
    for point1, point2 in pairwise(sorted_points):
        if point1.y <= y <= point2.y:
            return point1, point2
    return None


def interpolate(point1, point2, y):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    if y1 == y2:
        x = int((x1 + x2) / 2)
    else:
        x = int((y - y1) * (x2 - x1) / (y2 - y1) + x1)
    return x


def bound(x, bounds):
    x1, x2 = bounds
    if x1 > x2:
        x1, x2 = x2, x1
    if x <= x1:
        return x1 + 1
    elif x >= x2:
        return x2 - 1
    else:
        return x


class OutOfBoundsError(Exception):
    pass


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({},{})'.format(self.x, self.y)
