from enum import Enum
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter

from src.UI.primitives.Object import _Object
from src.UI.primitives.Point import Point
from src.UI.primitives.Rect import opacityToAlpha
from src.UI.primitives.values import DEFAULT_FONT, DEFAULT_COLOR, DEFAULT_PADDING
from src.utils.LinkableValue import editLinkableValue, LinkableValue


class Align(int):
    left = Qt.AlignLeft
    right = Qt.AlignRight
    top = Qt.AlignTop
    bottom = Qt.AlignBottom
    center = Qt.AlignCenter


class Text(_Object):
    def __init__(
            self,
            x: float,
            y: float,
            text: str,
            font=DEFAULT_FONT,
            color=DEFAULT_COLOR,
            align: Align = Align.left,
            withBackground=False,
            backgroundColor=QColor('black'),
            backgroundOpacity=0.5,
            padding: int | tuple[int, int, int, int] = DEFAULT_PADDING,
            movable: bool = False,
            hoverable: bool = False,
            hoverColor: QColor = None,
            onMoveCallback: Callable = None,
            UI=None,
            onClickCallback: Callable = None,
            onClickCallbackArgs: list = [],
            clickable: bool = None):
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
        self.clickable = clickable if clickable is not None else (onClickCallback is not None)
        if self.withBackground:
            self.backgroundColor = backgroundColor
            self.backgroundColor.setAlpha(opacityToAlpha(backgroundOpacity))
            if isinstance(padding, int):
                padding = (padding, padding, padding, padding)
            self.padding = padding
            self.w += padding[1] + padding[3]
            self.h += padding[0] + padding[2]

        self.UI = UI
        self.hoverable = hoverable
        self.hoverColor = hoverColor
        self.movable = movable
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
                int(self.x + self.padding[3]), int(self.y + self.padding[0]),
                int(self.w - self.padding[1] - self.padding[3]), int(self.h - self.padding[0] - self.padding[2]),
                self.align, self.text
            )
        else:
            painter.drawText(int(self.x), int(self.y), int(self.w), int(self.h), self.align, self.text)
        if self.movable:
            self.LT.render(painter)

    def isHover(self, x: float, y: float):
        if not self.visible:
            return False
        return (
                self.x <= x <= self.x + self.w and
                self.y <= y <= self.y + self.h
        )

    def setColor(self, color: QColor):
        super().setColor(color)
        self._currentColor = self.backgroundColor

    def setText(self, text: str):
        self.text = text
        lines = text.split('\n')
        self.w = max(map(len, lines)) * self.font.pointSize() / 1.05
        self.h = self.font.pointSize() * 2 * len(lines)
        if self.withBackground:
            self.w += self.padding[1] + self.padding[3]
            self.h += self.padding[0] + self.padding[2]

    def updateHoverState(self, x: float, y: float, isMouseRelease: bool = False):
        self._updateHoverState(x, y, isMouseRelease, "backgroundColor" if self.withBackground else "color")

    def _setCurrentColor(self, color: QColor):
        self._currentColor = color
