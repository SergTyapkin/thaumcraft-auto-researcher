import itertools

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush, QPainter

from src.UI.primitives.values import DEFAULT_COLOR, DEFAULT_LINE_WIDTH


def mixColors(color1: QColor, color2: QColor, ratio: float = 0.5, mixAlpha: bool = False) -> QColor:
    r = color1.red() * (1 - ratio) + color2.red() * ratio
    g = color1.green() * (1 - ratio) + color2.green() * ratio
    b = color1.blue() * (1 - ratio) + color2.blue() * ratio
    a = color1.alpha()
    if mixAlpha:
        a = color1.alpha() * (1 - ratio) + color2.alpha() * ratio
    return QColor(int(r), int(g), int(b), int(a))


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
    clickable = False
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
