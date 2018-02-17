
class Origin(object):
    """
    The origin object begins the spiral. It is defined by an hourglass
    coordinate on the wire_frame of the peice.

    Arguments:

    """

    def __init__(self):
        pass


class Pivot(object):
    pass


class Spiral(object):
    """
    For positive v negative space: consider everything to be positive space
    during rendering... Negative space will represent tiles without color,
    carved into an entire TileFrame of a single color.
    """

    def __init__(self, rotation=1, positive=True):
        self._rotation = rotation
        self._positive = positive

    @property
    def rotation(self):
        return self._rotation

    @property
    def positive(self):
        return self._positive


class SquareSpiral(Spiral):
    pass
