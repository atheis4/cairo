import numpy as np

from geometry import Point, Wire, Tile, WireFrame, TileFrame


init_coords = np.array([[0, 1], [1, 4], [4, 3], [3, 0]])
points = [Point(x=init_coords[i][0], y=init_coords[i][1]) for i in range(4)]
init_wire = Wire(*points)
wire_frame = WireFrame(init_wire)
tile_frame = TileFrame(wire_frame)
