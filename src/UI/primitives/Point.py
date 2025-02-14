from typing import Callable

from PyQt5.QtGui import QColor, QPainter

from src.UI.primitives.Object import _Object
from src.UI.primitives.values import DEFAULT_POINT_SIZE, DEFAULT_COLOR, DEFAULT_LINE_WIDTH
from src.utils.utils import distance


class Point(_Object):
    def __init__(
            self,
            x: float,
            y: float,
            size=DEFAULT_POINT_SIZE,
            color=DEFAULT_COLOR,
            lineWidth=DEFAULT_LINE_WIDTH,
            movable=False,
            hoverable: bool = False,
            hoverColor: QColor = None,
            onMoveCallback: Callable = None,
            onClickCallback: Callable = None,
            onClickCallbackArgs: list = [],
            clickable: bool = None):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.lineWidth = lineWidth
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
        painter.drawLine(int(self.x), int(self.y - self.size / 2), int(self.x), int(self.y + self.size / 2))
        painter.drawLine(int(self.x - self.size / 2), int(self.y), int(self.x + self.size / 2), int(self.y))
        if self.movable:
            color = self._brush.color()
            color.setAlpha(10)
            self._brush.setColor(color)
            painter.drawEllipse(int(self.x - self.size / 3), int(self.y - self.size / 3), int(self.size / 3 * 2),
                                int(self.size / 3 * 2))

    def isHover(self, x: float, y: float):
        if not self.visible:
            return False
        return distance(x, y, float(self.x), float(self.y)) <= (self.size / 2)
