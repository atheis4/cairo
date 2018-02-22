import numpy as np

from geometry import Block, Grid, Point, Wire, WireFrame


grid = Grid()
init_wire = Wire(grid=grid,
                 point1=Point(0, 1),
                 point2=Point(1, 4),
                 point3=Point(4, 3),
                 point4=Point(3, 0),
                 wire_type=0)
wire_frame = WireFrame(init_wire)

frame = wire_frame.frame
