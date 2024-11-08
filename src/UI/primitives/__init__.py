from typing import Union

from src.UI.primitives.Circle import Circle
from src.UI.primitives.Image import Image
from src.UI.primitives.Line import Line
from src.UI.primitives.Point import Point
from src.UI.primitives.Rect import Rect
from src.UI.primitives.Text import Text
from src.UI.primitives.Image import Image

UIPrimitive = Union[Point, Line, Circle, Rect, Text, Image]
