
class Origin(object):
    """The origin object begins the spiral. It is defined by an hourglass
    coordinate on the wire_frame of the peice.

    Arguments:
        coordinates (pattern.HourGlass)
        rotation (int): default 1, 'clockwise'
        positive_space (bool): does the origin represent positive or negative
            space.
        version_id (int): the version of spiral from the original work.
            1: square spiral (originally A).
            2:
            3:
    """

    def __init__(self, coordinates, rotation=1, positive_space=True,
                 version_id=1):
        self.coordinates = coordinates
        self._rotation = rotation
        self._positive_space = positive_space
