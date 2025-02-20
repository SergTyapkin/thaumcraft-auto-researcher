from typing import Callable

from PyQt5.QtGui import QColor, QPixmap, QPainter

from src.UI.primitives.Object import _Object
from src.UI.primitives.Rect import Rect


class Image(_Object):
    def __init__(
            self,
            x: float,
            y: float,
            w: float,
            h: float,
            path: str | None,
            movable: bool = False,
            hoverable: bool = False,
            hoverColor: QColor = None,
            onMoveCallback: Callable = None,
            onClickCallback: Callable = None,
            onClickCallbackArgs: list = [],
            clickable: bool = None):
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
        self.clickable = clickable if clickable is not None else (onClickCallback is not None)

        # self.image = self.image.scaledToWidth(int(w))
        # self.image = self.image.scaledToHeight(int(h))
        # self._label = QLabel()
        # self._label.setPixmap(self.image)
        # self._layout = QHBoxLayout()
        # self._layout.setContentsMargins(0, 0, 0, 0)
        # self._layout.addWidget(self._label)

        super().__init__()

    def setX(self, x: float):
        self.rect.setLx(x)
        self.rect.setRx(x + self.w)

    def setY(self, y: float):
        self.rect.setLy(y)
        self.rect.setRy(y + self.h)

    def setW(self, w: float):
        self.w = w
        self.rect.setRx(self.rect.LT.x + self.w)

    def setH(self, h: float):
        self.h = h
        self.rect.setRy(self.rect.LT.y + self.h)

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
