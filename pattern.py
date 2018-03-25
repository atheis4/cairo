
class Origin(object):
    """
    The origin object begins the spiral. It is defined by an hourglass
    coordinate on the wire_frame of the peice.

    Arguments:

    """

    def __init__(self, row, column, row_height, col_height, space='pos'):
        self.row = row
        self.column = column
        self.row_height = row_height
        self.col_height = col_height
        self.space = space


class Spiral(object):
    """
    For positive v negative space: consider everything to be positive space
    during rendering... Negative space will represent tiles without color,
    carved into an entire TileFrame of a single color.
    """

    def __init__(self, origin, rotation='cw'):
        self.origin = origin
        self._rotation = rotation

    @property
    def rotation(self):
        return self._rotation


class SpiralA(Spiral):
    """Represents the square spiral."""

    def __init__(self, origin, rotation='cw'):
        super().__init__(origin, rotation)


class SpiralB(Spiral):

    def __init__(self, origin, rotation='cw'):
        super().__init__(origin, rotation)


class SpiralC(Spiral):

    def __init__(self, origin, rotation='cw'):
        super().__init__(origin, rotation)


class SpiralD(Spiral):

    def __init__(self, origin, rotation='cw'):
        super().__init__(origin, rotation)


class SpiralE(Spiral):

    def __init__(self, origin, rotation='cw'):
        super().__init__(origin, rotation)
