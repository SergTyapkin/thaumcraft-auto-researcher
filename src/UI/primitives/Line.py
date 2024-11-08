import math
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter

from src.UI.primitives.Object import _Object
from src.UI.primitives.Point import Point
from src.UI.primitives.values import DEFAULT_COLOR, DEFAULT_LINE_WIDTH


class Line(_Object):
    def __init__(
            self,
            x1: float,
            y1: float,
            x2: float,
            y2: float,
            color=DEFAULT_COLOR,
            width=DEFAULT_LINE_WIDTH,
            dashed=False,
            movable: bool = False,
            hoverable: bool = False,
            hoverColor: QColor = None,
            onMoveCallback: Callable = None,
            onClickCallback: Callable = None,
            onClickCallbackArgs: list = [],
            clickable: bool = None):
        self.S = Point(x1, y1, color)
        self.E = Point(x2, y2, color)
        self.color = color
        self.lineWidth = width
        self.movable = movable
        self.hoverable = hoverable
        self.hoverColor = hoverColor
        self.onMoveCallback = onMoveCallback
        self.onClickCallback = onClickCallback
        self.onClickCallbackArgs = onClickCallbackArgs
        self.clickable = clickable if clickable is not None else (onClickCallback is not None)

        super().__init__()
        if dashed:
            self._pen.setStyle(Qt.PenStyle.DashLine)
            self._pen.setDashPattern([8, 5])

    def render(self, painter: QPainter):
        if not super().render(painter): return
        painter.drawLine(int(self.S.x), int(self.S.y), int(self.E.x), int(self.E.y))

    def isHover(self, x: float, y: float):
        if not self.visible:
            return False
        dxLine = self.E.x - self.S.x
        dyLine = self.E.y - self.S.y
        dxPoint = x - float(self.S.x)
        dyPoint = y - float(self.S.y)
        S = dxLine * dyPoint - dyLine * dxPoint
        lenLine = math.sqrt(dxLine * dxLine + dyLine * dyLine)
        h = S / lenLine
        return (
                math.fabs(h) < self.lineWidth / 2 and
                (
                        min(self.S.x, self.E.x) <= x <= max(self.S.x, self.E.x)
                    # or min(self.S.y, self.E.y) <= y <= max(self.S.y, self.E.y)
                )
        )
