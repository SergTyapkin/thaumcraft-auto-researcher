import itertools
import math
from enum import Enum
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont, QPen, QBrush

from src.LinkableValue import LinkableValue, editLinkableValue
from src.utils import distance

DEFAULT_POINT_SIZE = 21
DEFAULT_COLOR = QColor('red')
DEFAULT_LINE_WIDTH = 3
DEFAULT_FONT = QFont('Arial', 14, 500, False)
DEFAULT_PADDING = 20


def opacityToAlpha(opacity: float) -> int:
    return int(opacity * 255)


_objectIdValue = itertools.count()
class _Object:
    id = None
    lineWidth = DEFAULT_LINE_WIDTH
    color = DEFAULT_COLOR

    def __init__(self):
        self.id = next(_objectIdValue)
        self._pen = QPen(self.color, self.lineWidth, cap=Qt.RoundCap, join=Qt.RoundJoin)
        if self.lineWidth == 0:
            self._pen.setColor(QColor('transparent'))
        self._brush = QBrush(self.color)

    def render(self, painter: QPainter) -> None:
        painter.setBrush(self._brush)
        painter.setPen(self._pen)

    def isHover(self, x: float, y: float) -> bool:
        return False

class Point(_Object):
    def __init__(self, x: float, y: float, size=DEFAULT_POINT_SIZE, color=DEFAULT_COLOR, lineWidth=DEFAULT_LINE_WIDTH,
                 movable=False, onMoveCallback: Callable = None):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.lineWidth = lineWidth
        self.movable = movable
        self.onMoveCallback = onMoveCallback

        super().__init__()

    def render(self, painter: QPainter):
        super().render(painter)
        painter.drawLine(int(self.x), int(self.y - self.size / 2), int(self.x), int(self.y + self.size / 2))
        painter.drawLine(int(self.x - self.size / 2), int(self.y), int(self.x + self.size / 2), int(self.y))
        if self.movable:
            color = self._brush.color()
            color.setAlpha(10)
            self._brush.setColor(color)
            painter.drawEllipse(int(self.x - self.size / 3), int(self.y - self.size / 3), int(self.size / 3 * 2),
                                int(self.size / 3 * 2))

    def isHover(self, x: float, y: float):
        return distance(x, y, self.x, self.y) <= (self.size / 2)


class Line(_Object):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color=DEFAULT_COLOR, width=DEFAULT_LINE_WIDTH,
                 dashed=False):
        self.S = Point(x1, y1, color)
        self.E = Point(x2, y2, color)
        self.color = color
        self.lineWidth = width

        super().__init__()
        if dashed:
            self._pen.setStyle(Qt.PenStyle.DashLine)
            self._pen.setDashPattern([8, 5])

    def render(self, painter: QPainter):
        super().render(painter)
        painter.drawLine(int(self.S.x), int(self.S.y), int(self.E.x), int(self.E.y))

    def isHover(self, x: float, y: float):
        dxLine = self.E.x - self.S.x
        dyLine = self.E.y - self.S.y
        dxPoint = x - self.S.x
        dyPoint = y - self.S.y
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

class Rect(_Object):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color=DEFAULT_COLOR, lineWidth=DEFAULT_LINE_WIDTH,
                 dashed=False, fill=QColor('transparent'), fillOpacity=0):
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
        self.fill.setAlpha(opacityToAlpha(fillOpacity))

        super().__init__()

    def render(self, painter: QPainter):
        super().render(painter)
        self.T.render(painter)
        self.R.render(painter)
        self.B.render(painter)
        self.L.render(painter)
        painter.fillRect(int(self.LT.x), int(self.LT.y), int(self.w), int(self.h), self.fill)

    def isHover(self, x: float, y: float):
        return (
            min(self.LT.x, self.RB.x) <= x <= max(self.LT.x, self.RB.x) and
            min(self.LT.y, self.RB.y) <= y <= max(self.LT.y, self.RB.y)
        )

class Align(Enum):
    left = Qt.AlignLeft
    right = Qt.AlignRight
    top = Qt.AlignTop
    bottom = Qt.AlignBottom
    center = Qt.AlignCenter


class Text(_Object):
    def __init__(self, x: float, y: float, text: str, font=DEFAULT_FONT, color=DEFAULT_COLOR, align: Align = Align.left,
                 withBackground=False, backgroundColor=QColor('black'), backgroundOpacity=0.5, padding=DEFAULT_PADDING,
                 movable=False, UI=None):
        lines = text.split('\n')
        self.w = max(map(len, lines)) * font.pointSize() / 1.1
        self.h = font.pointSize() * 2 * len(lines)
        self.x = x
        self.y = y
        if align == Align.center:
            self.x = editLinkableValue(self.x, self.x - self.w / 2)
            self.y = editLinkableValue(self.y, self.y - self.h / 2)
        self.text = text
        self.font = font
        self.color = color
        self.align = align
        self.backgroundColor = QColor('transparent')
        self.withBackground = withBackground
        if self.withBackground:
            self.backgroundColor = backgroundColor
            self.backgroundColor.setAlpha(opacityToAlpha(backgroundOpacity))
            self.padding = padding
            self.w += padding * 2
            self.h += padding * 2

        self.movable = movable
        self.UI = UI
        if self.movable:
            if self.UI is None:
                raise TypeError("<class Text>: If argument movable=True, argument UI must be provided!")
            if not isinstance(self.x, LinkableValue):
                self.x = LinkableValue(self.x)
            if not isinstance(self.y, LinkableValue):
                self.y = LinkableValue(self.y)
            pointColor = QColor(self.backgroundColor)
            pointColor.setAlpha(255)
            self.LT = Point(self.x, self.y, movable=True, color=pointColor)
            self.UI.addObject(self.LT)

        super().__init__()

    def render(self, painter: QPainter):
        super().render(painter)
        painter.setFont(self.font)
        if self.withBackground:
            painter.fillRect(int(self.x), int(self.y), int(self.w), int(self.h), self.backgroundColor)
            painter.drawText(int(self.x + self.padding), int(self.y + self.padding), int(self.w - self.padding * 2),
                             int(self.h - self.padding * 2), self.align.value, self.text)
        else:
            painter.drawText(int(self.x), int(self.y), int(self.w), int(self.h), self.align.value, self.text)

        if self.movable:
            self.LT.render(painter)

    def isHover(self, x: float, y: float):
        return (
            self.x <= x <= self.x + self.w and
            self.y <= y <= self.y + self.h
        )

class Image(_Object):
    def __init__(self, x: float, y: float, w: float, h: float, path: str):
        self.rect = Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
        self.w = w
        self.h = h
        self.path = path
        self.image = QPixmap(path)

        # self.image = self.image.scaledToWidth(int(w))
        # self.image = self.image.scaledToHeight(int(h))
        # self._label = QLabel()
        # self._label.setPixmap(self.image)
        # self._layout = QHBoxLayout()
        # self._layout.setContentsMargins(0, 0, 0, 0)
        # self._layout.addWidget(self._label)

        super().__init__()

    def render(self, painter: QPainter):
        super().render(painter)
        painter.drawPixmap(int(self.rect.LT.x), int(self.rect.LB.y), int(self.rect.w), int(self.rect.h), self.image)

    def isHover(self, x: float, y: float):
        return self.rect.isHover(x, y)
