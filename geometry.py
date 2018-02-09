

class Wire(object):
    """The core layer and unit of the peice. A wire represents a single square
    of a grid that when chained with mirror versions on all four sides
    generates the cairo pentagon

    In the physical version, one wire measres 1.5 inches by 1.5 inches.
    """

    def __init__(self, x1=0, y1=1, x2=4, y2=3, x3=1, y3=0, x4=3, y4=4):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.pt1 = (x1, y1)
        self.pt2 = (x2, y2)
        self.pt3 = (x3, y3)
        self.pt4 = (x4, y4)

    def __repr__(self):
        return "W(pt1: {}, pt2: {}, pt3: {}, pt4: {})".format(
            self.pt1, self.pt2, self.pt3, self.pt4)

    def return_mirror(self):
        return Wire(self.y1, self.x1, self.y2, self.x2,
                    self.y3, self.x3, self.y4, self.x4)

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
            next_el = next_el.return_mirror()
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
        self.pt1 = wire.pt1
        self.pt2 = wire.pt2
        self.pt3 = wire.pt3
        self.pt4 = wire.pt4
        self.bottom_left = (0, 0)
        self.top_left = (0, 4)
        self.top_right = (4, 0)
        self.bottom_right = (0, 4)
        self.center = (2, 2)

    def __repr__(self):
        return ("T(polygon1: {}, polygon2: {}, polygon3: {}, polygon4: {})"
                .format(*self.tile_coords))

    @property
    def tile_coords(self):
        return self._generate_polygons()

    def _generate_polygons(self):
        """Returns a list of coordinates representing a 4 sided polygon and
        half of the pentagon tile."""
        return [
            (self.pt1, self.top_left, self.pt2, self.center),
            (self.pt2, self.top_right, self.pt3, self.center),
            (self.pt3, self.bottom_right, self.pt4, self.center),
            (self.pt4, self.bottom_left, self.pt1, self.center)
        ]


class TileFrame(object):
    """Represents the second layer of abstraction on the cairo pentagon image.

    The TileFrame creates the solid polygons that are defined by the wireframe
    and will eventually house the colors and be a container for the patterns.

    Arguments:
        wireframe (geometry.WireFrame)
    """

    def __init__(self, wireframe):
        self.wireframe = wireframe

    @property
    def frame(self):
        return self._translate_wireframe()

    def _translate_wireframe(self):
        frame = []
        for i in range(self.wireframe.height - 1):
            row = [wire.return_tile() for wire in self.wireframe.frame[i]]
            frame.append(row)
        return frame
