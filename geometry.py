
class Point(object):
    """The representation of a single cartesian coordinate on our 4 x 4 grid.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "P(x: {}, y: {})".format(self.x, self.y)

    def mirror(self):
        return Point(self.y, self.x)


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

    def return_tile(self):
        return Tile(self)


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
    """The atom of the Tile concept.

    Generated from a Wire object, this will contain the coordinates that trace
    the polygons of the Tile for a single grid.

    Arguments:
        wire (geometry.Wire)
    """

    def __init__(self, wire):
        self._point1 = wire.point1
        self._point2 = wire.point2
        self._point3 = wire.point3
        self._point4 = wire.point4
        self._bottom_left = Point(0, 0)
        self._top_left = Point(0, 4)
        self._top_right = Point(4, 0)
        self._bottom_right = Point(0, 4)
        self._center = Point(2, 2)

    def __repr__(self):
        return ("T(1. {}, 2. {}, 3. {}, 4. {})"
                .format(*self.tile_coords))

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
    def bottom_left(self):
        return self._bottom_left

    @property
    def top_left(self):
        return self._top_left

    @property
    def top_right(self):
        return self._top_right

    @property
    def bottom_right(self):
        return self._bottom_right

    @property
    def center(self):
        return self._center

    @property
    def tile_coords(self):
        return self._generate_polygons()

    def _generate_polygons(self):
        """Returns a list of coordinates representing a 4 sided polygon and
        half of the pentagon tile."""
        return [
            (self.point1, self.top_left, self.point2, self.center),
            (self.point2, self.top_right, self.point3, self.center),
            (self.point3, self.bottom_right, self.point4, self.center),
            (self.point4, self.bottom_left, self.point1, self.center)]


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
        for i in range(self._wireframe.height - 1):
            row = [wire.return_tile() for wire in self._wireframe.frame[i]]
            frame.append(row)
        return frame
