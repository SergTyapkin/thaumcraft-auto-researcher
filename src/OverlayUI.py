import sys
from typing import Union, Callable

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, QObject
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow

from src.utils import distance
from src.UIPrimitives import Point, Line, Rect, Text, Image

UIPrimitive = Union[Point, Line, Rect, Text, Image]

FPS = 60
FRAME_TIME = int(1000 / FPS)


class LinkableValue:
    def __init__(self, val: float):
        self.val = val

    def __float__(self):
        return float(self.val)

    def __int__(self):
        return int(self.val)

    def __add__(self, other):
        if isinstance(other, LinkableValue):
            return self.val + other.val
        return self.val + other

    def __sub__(self, other):
        if isinstance(other, LinkableValue):
            return self.val - other.val
        return self.val - other

    def __mul__(self, other):
        if isinstance(other, LinkableValue):
            return self.val * other.val
        return self.val * other

    def __divmod__(self, other):
        if isinstance(other, LinkableValue):
            return self.val / other.val
        return self.val / other
    # def __str__(self):
    #     return str(self.val)


class LinkableCoord:
    def __init__(self, x: float, y: float):
        self.x = LinkableValue(x)
        self.y = LinkableValue(y)
    # def __str__(self):
    #     return f'({self.x}, {self.y})'


def editLinkableValue(oldVal: Union[float, LinkableValue], newVal: float) -> Union[float, LinkableValue]:
    if isinstance(oldVal, LinkableValue):
        oldVal.val = newVal
        return oldVal
    return newVal


class _Window(QMainWindow):
    objects: list[UIPrimitive] = []
    keysCallbacks: dict[Qt.Key, Callable] = {}
    currentMovingObject = None

    def __init__(self, opacity=1.0, w=None, h=None):
        QMainWindow.__init__(self, None,
                             Qt.FramelessWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowStaysOnTopHint
                             # | Qt.Popup | Qt.WindowDoesNotAcceptFocus | Qt.WindowTransparentForInput
                             )
        fillScreenGeometry = QDesktopWidget().availableGeometry()
        self.w = w or fillScreenGeometry.width()
        self.h = h or fillScreenGeometry.height()

        self.resize(self.w, self.h)
        self.setFixedSize(self.w, self.h)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(opacity)

        # widget = QWidget()
        # self.setCentralWidget(widget)
        # pixmap1 = QPixmap('image.png')
        # pixmap1 = pixmap1.scaledToWidth(self.w)
        # pixmap1 = pixmap1.scaledToHeight(self.h)
        # imageOnLabel = QLabel()
        # imageOnLabel.setPixmap(pixmap1)
        #
        # layout_box = QHBoxLayout(widget)
        # layout_box.setContentsMargins(0, 0, 0, 0)
        # layout_box.addWidget(imageOnLabel)
        #
        # p = self.geometry().bottomRight() - image.geometry().bottomRight() - QPoint(100, 100)
        # image.move(p)

        # self._path = QPainterPath()
        # self.DC = QDesktopWidget()

        timerId = self.startTimer(FRAME_TIME)

    def getCenter(self):
        return self.w / 2, self.h / 2

    def timerEvent(self, t):
        # if len(self.objects) > 0:
        #     self.objects[0].RB.x = editLinkableValue(self.objects[0].RB.x, self.objects[0].RB.x + 1)
        #     self.objects[0].RB.y = editLinkableValue(self.objects[0].RB.y, self.objects[0].RB.y + 1)

        # if GetKeyState(0x01) < -1:
        #     sys.exit()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        for obj in self.objects:
            obj.render(painter)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        for obj in self.objects:
            if isinstance(obj, Point) and obj.movable and (
                    distance(obj.x, obj.y, event.x(), event.y()) <= (obj.size / 2)):
                self.currentMovingObject = obj
                break

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.currentMovingObject is None:
            return

        self.currentMovingObject.x = editLinkableValue(self.currentMovingObject.x, event.x())
        self.currentMovingObject.y = editLinkableValue(self.currentMovingObject.y, event.y())

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.currentMovingObject = None

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        for key in self.keysCallbacks.keys():
            if event.key() == key:
                self.keysCallbacks[key]()

    def addObject(self, obj: UIPrimitive):
        self.objects.append(obj)

    def clear(self):
        self.objects = []

    def getObjectsByFilter(self, objectType: UIPrimitive):
        res = []
        for obj in self.objects:
            if isinstance(obj, objectType):
                res.append(obj)
        return res

    def setKeyCallback(self, key: Qt.Key, callback: Callable):
        self.keysCallbacks[key] = callback


class _Worker(QObject):
    def __init__(self, foo):
        super().__init__()
        self.foo = foo

    def work(self):
        self.foo()


class OverlayUI(_Window):
    def __init__(self, opacity=1.0):
        print("UI INIT!")
        self.app = QApplication(sys.argv)
        _Window.__init__(self, opacity=opacity)

    def start(self, otherProcessFoo):
        self.otherProcessThread = QThread()
        otherProcessWorker = _Worker(otherProcessFoo)
        otherProcessWorker.moveToThread(self.otherProcessThread)

        self.otherProcessThread.started.connect(otherProcessWorker.work)
        self.otherProcessThread.start()

        self.show()

        sys.exit(self.app.exec_())
