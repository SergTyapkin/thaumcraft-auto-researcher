import itertools
import math
from enum import Enum
from typing import Callable, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont, QPen, QBrush

from src.utils.LinkableValue import LinkableValue, editLinkableValue
from src.utils.utils import distance

DEFAULT_POINT_SIZE = 21
DEFAULT_COLOR = QColor('red')
DEFAULT_LINE_WIDTH = 3
DEFAULT_FONT = QFont('Arial', 14, 500, False)
DEFAULT_PADDING = 20


def mixColors(color1: QColor, color2: QColor, ratio: float = 0.5, mixAlpha: bool = False) -> QColor:
    r = color1.red() * (1 - ratio) + color2.red() * ratio
    g = color1.green() * (1 - ratio) + color2.green() * ratio
    b = color1.blue() * (1 - ratio) + color2.blue() * ratio
    a = color1.alpha()
    if mixAlpha:
        a = color1.alpha() * (1 - ratio) + color2.alpha() * ratio
    return QColor(int(r), int(g), int(b), int(a))

def opacityToAlpha(opacity: float) -> int:
    return int(opacity * 255)


_objectIdValue = itertools.count()
class _Object:
    id = None
    lineWidth = DEFAULT_LINE_WIDTH
    color = DEFAULT_COLOR
    hoverColor = None
    _currentColor = None
    visible = True
    movable = False
    hoverable = False
    onClickCallback = None
    onClickCallbackArgs = []
    _pen: QPen = None
    _brush: QBrush = None

    def __init__(self):
        self.id = next(_objectIdValue)
        self._currentColor = self.color
        self._init()

    def setColor(self, color: QColor):
        self.color = color
        self._currentColor = color
        self._init()

    def _setCurrentColor(self, color: QColor):
        self._currentColor = color
        self._init()

    def _init(self):
        self._pen = QPen(self._currentColor, self.lineWidth, cap=Qt.RoundCap, join=Qt.RoundJoin)
        if self.lineWidth == 0:
            self._pen.setColor(QColor('transparent'))
        self._brush = QBrush(self._currentColor)

    def render(self, painter: QPainter) -> bool:
        if not self.visible:
            return False
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        return True

    def isHover(self, x: float, y: float) -> bool:
        return False

    def setVisibility(self, state: bool) -> None:
        self.visible = state

    def _updateHoverState(self, x: float, y: float, isMouseRelease: bool, targetFieldName: str = "color"):
        if not self.hoverable:
            return
        if not isMouseRelease and self.isHover(x, y):
            newColor = self.hoverColor
            if newColor is None:
                oldColor = getattr(self, targetFieldName)
                if oldColor.lightness() > 230:
                    additionalColor = QColor('black')
                else:
                    additionalColor = QColor('white')
                newColor = mixColors(oldColor, additionalColor, 0.2)
            self._setCurrentColor(newColor)
        else:
            self._setCurrentColor(getattr(self, targetFieldName))

    def updateHoverState(self, x: float, y: float, isMouseRelease: bool = False):
        self._updateHoverState(x, y, isMouseRelease)


class Circle(_Object):
    def __init__(self, x: float, y: float, r: float, color=DEFAULT_COLOR, lineWidth=DEFAULT_LINE_WIDTH,
                 movable: bool = False, hoverable: bool = False, hoverColor: QColor = None, onMoveCallback: Callable = None, onClickCallback: Callable = None, onClickCallbackArgs: list = []): #, fill=None, fillOpacity=1):
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
        # self.fill = fill
        # if fill is not None: self.fill.setAlpha(opacityToAlpha(fillOpacity))

        super().__init__()

    def render(self, painter: QPainter):
        if not super().render(painter): return
        painter.drawEllipse(int(self.x - self.r), int(self.y - self.r), int(self.r * 2), int(self.r * 2))

    def isHover(self, x: float, y: float):
        return distance(x, y, self.x, self.y) <= self.r



class Point(_Object):
    def __init__(self, x: float, y: float, size=DEFAULT_POINT_SIZE, color=DEFAULT_COLOR, lineWidth=DEFAULT_LINE_WIDTH,
                 movable=False, hoverable: bool = False, hoverColor: QColor = None, onMoveCallback: Callable = None, onClickCallback: Callable = None, onClickCallbackArgs: list = []):
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


class Line(_Object):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color=DEFAULT_COLOR, width=DEFAULT_LINE_WIDTH,
                 dashed=False, movable: bool = False, hoverable: bool = False, hoverColor: QColor = None, onMoveCallback: Callable = None, onClickCallback: Callable = None, onClickCallbackArgs: list = []):
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

class Rect(_Object):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color=DEFAULT_COLOR, lineWidth=DEFAULT_LINE_WIDTH,
                 dashed=False, fill=None, fillOpacity=1, movable: bool = False, hoverable: bool = False, hoverColor: QColor = None, onMoveCallback: Callable = None, onClickCallback: Callable = None, onClickCallbackArgs: list = []):
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


class Align(Enum):
    left = Qt.AlignLeft
    right = Qt.AlignRight
    top = Qt.AlignTop
    bottom = Qt.AlignBottom
    center = Qt.AlignCenter


class Text(_Object):
    def __init__(self, x: float, y: float, text: str, font=DEFAULT_FONT, color=DEFAULT_COLOR, align: Align = Align.left,
                 withBackground=False, backgroundColor=QColor('black'), backgroundOpacity=0.5, padding=DEFAULT_PADDING,
                 movable: bool = False, hoverable: bool = False, hoverColor: QColor = None, onMoveCallback: Callable = None, UI=None, onClickCallback: Callable = None, onClickCallbackArgs: list = []):
        lines = text.split('\n')
        self.w = max(map(len, lines)) * font.pointSize() / 1.05
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
        self.onMoveCallback = onMoveCallback
        self.onClickCallback = onClickCallback
        self.onClickCallbackArgs = onClickCallbackArgs
        if self.withBackground:
            self.backgroundColor = backgroundColor
            self.backgroundColor.setAlpha(opacityToAlpha(backgroundOpacity))
            self.padding = padding
            self.w += padding * 2
            self.h += padding * 2

        self.UI = UI
        self.movable = False
        self.hoverable = hoverable
        self.hoverColor = hoverColor
        # self.movable = movable
        if movable:
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
        self._currentColor = self.backgroundColor

    def render(self, painter: QPainter):
        if not super().render(painter): return
        painter.setFont(self.font)
        if self.withBackground:
            painter.fillRect(int(self.x), int(self.y), int(self.w), int(self.h), self._currentColor)
            painter.drawText(
                int(self.x + self.padding), int(self.y + self.padding),
                int(self.w - self.padding * 2), int(self.h - self.padding * 2),
                self.align.value, self.text
            )
        else:
            painter.drawText(int(self.x), int(self.y), int(self.w), int(self.h), self.align.value, self.text)

        if self.movable:
            self.LT.render(painter)

    def isHover(self, x: float, y: float):
        if not self.visible:
            return False
        return (
            self.x <= x <= self.x + self.w and
            self.y <= y <= self.y + self.h
        )

    def updateHoverState(self, x: float, y: float, isMouseRelease: bool = False):
        self._updateHoverState(x, y, isMouseRelease, "backgroundColor" if self.withBackground else "color")
    def _setCurrentColor(self, color: QColor):
        self._currentColor = color


class Image(_Object):
    def __init__(self, x: float, y: float, w: float, h: float, path: str | None, movable: bool = False, hoverable: bool = False, hoverColor: QColor = None, onMoveCallback: Callable = None, onClickCallback: Callable = None, onClickCallbackArgs: list = []):
        self.rect = Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
        self.w = w
        self.h = h
        self.path = path
        self.image = None
        if path is not None:
            self.image = QPixmap(path)
        self.movable = movable
        self.hoverable = hoverable
        self.hoverColor = hoverColor
        self.onMoveCallback = onMoveCallback
        self.onClickCallback = onClickCallback
        self.onClickCallbackArgs = onClickCallbackArgs

        # self.image = self.image.scaledToWidth(int(w))
        # self.image = self.image.scaledToHeight(int(h))
        # self._label = QLabel()
        # self._label.setPixmap(self.image)
        # self._layout = QHBoxLayout()
        # self._layout.setContentsMargins(0, 0, 0, 0)
        # self._layout.addWidget(self._label)

        super().__init__()

    def render(self, painter: QPainter):
        if not super().render(painter): return
        if not self.image: return
        painter.drawPixmap(int(self.rect.LT.x), int(self.rect.LB.y), int(self.rect.w), int(self.rect.h), self.image)

    def isHover(self, x: float, y: float):
        if not self.visible:
            return False
        return self.rect.isHover(x, y)

    def setPath(self, path: str):
        self.path = path
        self.image = QPixmap(path)

    def setImage(self, image: QPixmap):
        self.path = None
        self.image = image

    def clearImage(self):
        self.path = None
        self.image = None


UIPrimitive = Union[Point, Line, Circle, Rect, Text, Image]
