"""
Geometry Module

Contains the core objects of the Cairo Pentagon Project.

Grid - plane on which all other obects are joined.
Point - a cartesian coordinate, x and y.
Wire - four points on a grid representing a single unit of the design.
WireFrame -
Block - two consecutive Wire objects. Can be horizontal or vertical. A flexible
    concept that is used to return the pentagon necessary to create the
    patterns.
"""


class Grid(object):
    """
    The representation of the two dimensional container that the Points are
    defined within.
    """

    def __init__(self, shift_x=False, shift_y=False):
        self.center = Point(2, 2)
        self.bottom_left = Point(0, 0)
        self.top_left = Point(0, 4)
        self.top_right = Point(4, 4)
        self.bottom_right = Point(4, 0)

    @classmethod
    def shift_x(cls):
        return

    @classmethod
    def shift_y(cls):
        pass


class Point(object):
    """
    A single cartesian coordinate on a 4 x 4 grid.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "P(x: {}, y: {})".format(self.x, self.y)

    def mirror(self):
        return Point(self.y, self.x)

    def shift_x(self, delta=4):
        return Point(self.x + delta, self.y)

    def shift_y(self, delta=4):
        return Point(self.x, self.y + delta)


class Wire(object):
    """
    The first layer and unit of the peice. A wire represents a single square of
    a grid that when chained with mirror versions on all four sides generates
    the cairo pentagon.

    In the physical version, one wire measres 1.5 inches by 1.5 inches.

    Arguments:
        grid (geometry.Grid)
        point1 (geometry.Point)
        point2 (geometry.Point)
        point3 (geometry.Point)
        point4 (geometry.Point)
    """

    def __init__(self,
                 grid=Grid(),
                 point1=Point(0, 1),
                 point2=Point(1, 4),
                 point3=Point(4, 3),
                 point4=Point(3, 0),
                 wire_type=0):
        self._grid = grid
        self._point1 = point1
        self._point2 = point2
        self._point3 = point3
        self._point4 = point4
        self._wire_type = wire_type

    def __repr__(self):
        return "Wire(1: {}, 2: {}, 3: {}, 4: {}, type: {})".format(
            self.point1, self.point2, self.point3, self.point4, self.wire_type)

    @property
    def wire_type(self):
        return self._wire_type

    @property
    def trapezium1(self):
        return (self._point1,
                self._grid.top_left,
                self._point2,
                self._grid.center)

    @property
    def trapezium2(self):
        return (self._point2,
                self._grid.top_right,
                self._point3,
                self._grid.center)

    @property
    def trapezium3(self):
        return (self._point3,
                self._grid.bottom_right,
                self._point4,
                self._grid.center)

    @property
    def trapezium4(self):
        return (self._point4,
                self._grid.bottom_left,
                self._point1,
                self._grid.center)

    def mirror(self):
        wire_type = 1 if self.wire_type == 0 else 0
        return Wire(self.point4.mirror(),
                    self.point3.mirror(),
                    self.point2.mirror(),
                    self.point1.mirror(),
                    wire_type=wire_type)

    def shift_x(self, delta=4):
        """Returns a new Wire with the point objects by a distance of four to
        the right."""
        return Wire(grid=Grid(),
                    point1=self._point1.shift_x(delta),
                    point2=self._point2.shift_x(delta),
                    point3=self._point3.shift_x(delta),
                    point4=self._point4.shift_x(delta),
                    wire_type=self.wire_type)

    def shift_y(self, delta=4):
        """Returns a new Wire with the point objects by a distance of four
        downwards."""
        return Wire(grid=Grid(),
                    point1=self._point1.shift_y(delta),
                    point2=self._point2.shift_y(delta),
                    point3=self._point3.shift_y(delta),
                    point4=self._point4.shift_y(delta),
                    wire_type=self.wire_type)


class WireFrame(object):
    """
    Takes a width and a height and returns a grid of Wire objects to fill the
    dimensions.

    Argments:

        width (int)
        height (int)
        origin (geometry.Wire): the initializing Wire object that is
            systematically mirrored to create the entire WireFrame object.
    """

    def __init__(self, initial_wire=None, width=12, height=16):
        self._width = width
        self._height = height
        self._initial_wire = initial_wire
        self._frame = self._build_frame()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def frame(self):
        return self._frame

    def _fill_row(self, initial=None):
        if not initial:
            initial = self._initial_wire
        row = self._fill_next([], initial)
        return row

    def _fill_next(self, row, next_el):
        if len(row) == self.width:
            return row
        else:
            row.append(next_el)
            next_el = next_el.mirror()
            return self._fill_next(row, next_el)

    def _build_frame(self, initial_row=None):
        if not initial_row:
            initial_row = self._fill_row()
        frame = self._next_column([], initial_row)
        return frame

    def _next_column(self, frame, next_row):
        if len(frame) == self.height:
            return frame
        else:
            frame.append(next_row)
            next_row = self._fill_row(next_row[-1])
            return self._next_column(frame, next_row)


class Block(object):

    def __init__(self,
                 row_index,
                 column_index,
                 row_height,
                 column_width,
                 wire1,
                 wire2):
        self.row_index = row_index
        self.column_index = column_index
        self.row_height = row_height
        self.column_width = column_height
        self.wire1 = wire1
        self.wire2 = wire2

    @property
    def pentagon(self):
        if row_height == 0:
            pass

    @property
    def edge_map(self):
