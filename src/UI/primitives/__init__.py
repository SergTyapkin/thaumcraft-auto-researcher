from typing import Union

from UI.primitives.Circle import Circle
from UI.primitives.Image import Image
from UI.primitives.Line import Line
from UI.primitives.Point import Point
from UI.primitives.Rect import Rect
from UI.primitives.Text import Text
from UI.primitives.Image import Image

UIPrimitive = Union[Point, Line, Circle, Rect, Text, Image]
