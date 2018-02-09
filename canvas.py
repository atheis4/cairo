

class Canvas(object):
    """Represents the container for the entire cairo pentagon image.

    Defined by (w * h), each unit represents a sigle tile.

    The original stenciled version of the cairo pentagon measured 9" x 12".
    This would be translated as 6 x 8 units.

    The size of the second edition of the spray stencils measured 12" x 15".
    This would be translated as 8 x 10 units.

    The digitized version would have measured 18" x 24". It is represented by a
    rectangle of 12 x 16 units.

    The conversion from inches to unit space is: x * 3 / 2."""

    def __init__(self, width=8, height=10):
        self.width = width
        self.height = height

    def create_wireframe(self):
        pass

    def create_tileframe(self):
        pass

    def create_lattice(self):
        pass
