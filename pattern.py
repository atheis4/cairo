
class Origin(object):
    """
    The origin object begins the spiral. It is defined by an hourglass
    coordinate on the wire_frame of the peice.

    Arguments:
        row_index (int):
        col_index (int):
        row_height (int):
        col_height (int):
        tile_one (int):
        tile_two (int):
    """

    def __init__(self,
                 row_index=0,
                 col_index=0,
                 row_height=0,
                 col_height=1,
                 tile_one=0,
                 tile_two=1):
        self._row_index = row_index
        self._col_index = col_index
        self._row_height = row_height
        self._col_height = col_height
        self._tile_one = tile_one
        self._tile_two = tile_two


class SpiralArm(object):
    """
    For positive v negative space: consider everything to be positive space
    during rendering... Negative space will represent tiles without color,
    carved into an entire TileFrame of a single color.

    Arguments:
        rotation (String): 'cw' or 'ccw' (default 'cw')
        space (String): 'pos' or 'neg' (default 'pos')
    """

    def __init__(self, rotation='cw', space='pos', origin=None):
        self._rotation = rotation
        self._space = space
        self._origin = origin

    @property
    def rotation(self):
        return self._rotation

    @property
    def space(self):
        return self._space

    def run(self):
        raise NotImplementedError(
            "The run method cannot be run on the base class: SpiralArm")


class SquareSpiralArm(Spiral):
    def __init__(self, rotation='cw', space='pos', origin=None):
        super().__init__(rotation, space, origin)

    def run(self):
        pass

    def return_next(self, current, pivot=None):
        pass


class Peice(object):
    pass


class PeiceOneThree(Peice):
    pass


class PeiceOneFour(Peice):
    pass
