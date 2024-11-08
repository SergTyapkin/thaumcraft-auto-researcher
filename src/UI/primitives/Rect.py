from typing import Callable

from PyQt5.QtGui import QColor, QPainter

from src.UI.primitives.Line import Line
from src.UI.primitives.Object import _Object
from src.UI.primitives.Point import Point
from src.UI.primitives.values import DEFAULT_COLOR, DEFAULT_LINE_WIDTH


def opacityToAlpha(opacity: float) -> int:
    return int(opacity * 255)


class Rect(_Object):
    def __init__(
            self,
            x1: float,
            y1: float,
            x2: float,
            y2: float,
            color=DEFAULT_COLOR,
            lineWidth=DEFAULT_LINE_WIDTH,
            dashed=False,
            fill=None,
            fillOpacity=1,
            movable: bool = False,
            hoverable: bool = False,
            hoverColor: QColor = None,
            onMoveCallback: Callable = None,
            onClickCallback: Callable = None,
            onClickCallbackArgs: list = [],
            clickable: bool = None):
        self.LT = Point(x1, y1, color)
        self.RT = Point(x2, y1, color)
        self.RB = Point(x2, y2, color)
        self.LB = Point(x1, y2, color)
        self.T = Line(x1, y1, x2, y1, color, lineWidth, dashed)
        self.R = Line(x2, y1, x2, y2, color, lineWidth, dashed)
        self.B = Line(x2, y2, x1, y2, color, lineWidth, dashed)
        self.L = Line(x1, y2, x1, y1, color, lineWidth, dashed)
        self.w = x2 - x1
        self.h = y2 - y1
        self.color = color
        self.lineWidth = lineWidth
        self.fill = fill
        if fill is not None: self.fill.setAlpha(opacityToAlpha(fillOpacity))
        self.movable = movable
        self.hoverable = hoverable
        self.hoverColor = hoverColor
        self.onMoveCallback = onMoveCallback
        self.onClickCallback = onClickCallback
        self.onClickCallbackArgs = onClickCallbackArgs
        self.clickable = clickable if clickable is not None else (onClickCallback is not None)

        super().__init__()

    def render(self, painter: QPainter):
        if not super().render(painter): return
        self.T.render(painter)
        self.R.render(painter)
        self.B.render(painter)
        self.L.render(painter)
        if self.fill is not None: painter.fillRect(int(self.LT.x), int(self.LT.y), int(self.w), int(self.h), self.fill)

    def isHover(self, x: float, y: float):
        if not self.visible:
            return False
        return (
                min(self.LT.x, self.RB.x) <= x <= max(self.LT.x, self.RB.x) and
                min(self.LT.y, self.RB.y) <= y <= max(self.LT.y, self.RB.y)
        )

    def setLx(self, val):
        self.LT.x = val
        self.LB.x = val
        self.L.S.x = val
        self.L.E.x = val
        self.T.S.x = val
        self.B.E.x = val
        self.w = self.RB.x - self.LT.x

    def setLy(self, val):
        self.LT.y = val
        self.LB.y = val
        self.L.E.y = val
        self.R.S.y = val
        self.T.S.y = val
        self.T.E.y = val
        self.h = self.RB.y - self.LT.y

    def setRx(self, val):
        self.RT.x = val
        self.RB.x = val
        self.R.S.x = val
        self.R.E.x = val
        self.T.E.x = val
        self.B.S.x = val
        self.w = self.RB.x - self.LT.x

    def setRy(self, val):
        self.RT.y = val
        self.RB.y = val
        self.L.S.y = val
        self.R.E.y = val
        self.B.S.y = val
        self.B.E.y = val
        self.h = self.RB.y - self.LT.y

    def setCoords(self, xLT, yLT, xRB, yRB):
        self.setLx(xLT)
        self.setLy(yLT)
        self.setRx(xRB)
        self.setRy(yRB)
