from typing import Callable

from PyQt5.QtGui import QColor, QPainter

from src.UI.primitives.Object import _Object
from src.UI.primitives.values import DEFAULT_COLOR, DEFAULT_LINE_WIDTH
from src.utils.utils import distance


class Circle(_Object):
    def __init__(
            self,
            x: float,
            y: float,
            r: float,
            color=DEFAULT_COLOR,
            lineWidth=DEFAULT_LINE_WIDTH,
            movable: bool = False,
            hoverable: bool = False,
            hoverColor: QColor = None,
            onMoveCallback: Callable = None,
            onClickCallback: Callable = None,
            onClickCallbackArgs: list = [],
            clickable: bool = None):  # , fill=None, fillOpacity=1):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.lineWidth = lineWidth
        self.movable = movable
        self.hoverable = hoverable
        self.hoverColor = hoverColor
        self.onMoveCallback = onMoveCallback
        self.onClickCallback = onClickCallback
        self.onClickCallbackArgs = onClickCallbackArgs
        self.clickable = clickable if clickable is not None else (onClickCallback is not None)
        # self.fill = fill
        # if fill is not None: self.fill.setAlpha(opacityToAlpha(fillOpacity))

        super().__init__()

    def render(self, painter: QPainter):
        if not super().render(painter): return
        painter.drawEllipse(int(self.x - self.r), int(self.y - self.r), int(self.r * 2), int(self.r * 2))

    def isHover(self, x: float, y: float):
        return distance(x, y, self.x, self.y) <= self.r
