from typing import Any, Dict, Optional, Tuple, Union


Column = Optional[Union[int, Tuple[int, int]]]
CompoundDimension = Union[int, Tuple[int, int]]
DimensionMap = Dict[Tuple[str, str], Dict[str, Tuple[int, int]]]
Key = Tuple[str, Union[int, Tuple[int, int]], Union[Tuple[int, int], int]]
Origin = Tuple[int, int]
Row = Optional[Union[int, Tuple[int, int]]]
