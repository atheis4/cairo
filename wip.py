import numpy as np

from geometry import Block, Grid, Point, Wire, WireFrame


grid = Grid()
init_wire = Wire(grid=grid, Point(0, 1), Point(1, 4), Point(4, 3), Point(3, 0))
wire_frame = WireFrame(init_wire)

frame = wire_frame.frame
