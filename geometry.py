
class Grid(object):
    """The representation of the two dimensional container that the Points are
    defined within."""

    center = Point(2, 2)
    b_left = Point(0, 0)
    t_left = Point(0, 4)
    t_right = Point(4, 4)
    b_right = Poing(4, 0)


class Point(object):
    """A single cartesian coordinate on our 4 x 4 grid."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "P(x: {}, y: {})".format(self.x, self.y)

    def mirror(self):
        return Point(self.y, self.x)


class Polygon(object):
    """The atom of the tile concept.

    Generated from four Points."""

    def __init__(self, point1, point2, point3, point4, polygon_type):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4
        self.polygon_type = polygon_type


class Wire(object):
    """The first layer and unit of the peice. A wire represents a single square
    of a grid that when chained with mirror versions on all four sides
    generates the cairo pentagon.

    In the physical version, one wire measres 1.5 inches by 1.5 inches.

    Arguments:
        point1 (geometry.Point)
        point2 (geometry.Point)
        point3 (geometry.Point)
        point4 (geometry.Point)
    """

    def __init__(self, point1, point2, point3, point4, wire_type='a'):
        self._point1 = point1
        self._point2 = point2
        self._point3 = point3
        self._point4 = point4
        self._wire_type = wire_type

    def __repr__(self):
        return "W(1. {}, 2. {}, 3. {}, 4. {}, type: {})".format(
            self.point1, self.point2, self.point3, self.point4, self.wire_type)

    @property
    def point1(self):
        return self._point1

    @property
    def point2(self):
        return self._point2

    @property
    def point3(self):
        return self._point3

    @property
    def point4(self):
        return self._point4

    @property
    def wire_type(self):
        return self._wire_type

    def mirror(self):
        wire_type = 'b' if self.wire_type == 'a' else 'a'
        return Wire(self.point4.mirror(), self.point3.mirror(),
                    self.point2.mirror(), self.point1.mirror(),
                    wire_type=wire_type)

    def return_polygons(self, grid):
        return [
            Polygon(self.point1, grid.t_left, self.point2, grid.center,
                    self.wire_type),
            Polygon(self.point2, grid.t_right, self.point3, grid.center,
                    self.wire_type),
            Polygon(self.point3, grid.b_right, self.point4, grid.center,
                    self.wire_type),
            Polygon(self.point4, grid.b_left, self.point1, grid.center,
                    self.wire_type)]


class WireFrame(object):
    """Takes a width and a height and returns a grid of Wire objects to fill
    the dimensions.

    Argments:

        width (int)
        height (int)
        origin (geometry.Wire): the initializing Wire object that is
            systematically mirrored to create the entire WireFrame object."""

    def __init__(self, origin=None, width=12, height=16):
        self._width = width
        self._height = height
        self._origin = origin
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
            initial = self._origin
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


class Tile(object):

    def __init__(self, polygon1, polygon2, polygon3, polygon4):
        self.polygon1 = polygon1
        self.polygon2 = polygon2
        self.polygon3 = polygon3
        self.polygon4 = polygon4


class Tile(object):
    """The atom of the Tile concept.

    Generated from four Polygon objects, this will contain the coordinates that
    trace the polygons of the Tile for a single grid.

    Arguments:
        wire (geometry.Wire)
    """

    def __init__(self, wire):
        self._wire = wire
        self._b_left = Point(0, 0)
        self._t_left = Point(0, 4)
        self._t_right = Point(4, 4)
        self._b_right = Point(0, 4)
        self._center = Point(2, 2)
        self._tile_type = wire.wire_type

    def __repr__(self):
        return ("T(1. {}, 2. {}, 3. {}, 4. {}, type: {type})"
                .format(*self.tile_coords, type=self.tile_type))

    @property
    def b_left(self):
        return self._b_left

    @property
    def t_left(self):
        return self._t_left

    @property
    def t_right(self):
        return self._t_right

    @property
    def b_right(self):
        return self._b_right

    @property
    def center(self):
        return self._center

    @property
    def tile_type(self):
        return self._tile_type

    @property
    def tile_coords(self):
        return self._generate_polygons()

    def _generate_polygons(self):
        """Returns a list of coordinates representing a 4 sided polygon and
        half of a single pentagon tile."""
        return [
            (self.wire.point1, self.t_left, self.wire.point2, self.center),
            (self.wire.point2, self.t_right, self.wire.point3, self.center),
            (self.wire.point3, self.b_right, self.wire.point4, self.center),
            (self.wire.point4, self.b_left, self.wire.point1, self.center)]


class TileFrame(object):
    """Represents the second layer of abstraction on the cairo pentagon image.

    The TileFrame creates the solid polygons that are defined by the wireframe
    and will eventually house the colors and be a container for the patterns.

    Arguments:
        wireframe (geometry.WireFrame)
    """

    def __init__(self, wireframe):
        self._wireframe = wireframe
        self._frame = self._translate_wireframe()

    @property
    def frame(self):
        return self._frame

    def _translate_wireframe(self):
        frame = []
        for i in range(self._wireframe.height):
            row = [wire.return_tile() for wire in self._wireframe.frame[i]]
            frame.append(row)
        return frame

    @classmethod
    def return_compliment_tile(cls, tile):
        pass
        # TODO:


class Pentagon(object):

    def __init__(self, )
