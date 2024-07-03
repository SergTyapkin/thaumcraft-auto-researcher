import sys
from enum import Enum
from typing import Union, Callable, Any

import keyboard
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, QObject, QEvent
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow

from src.utils.LinkableValue import editLinkableValue
from src.UI.UIPrimitives import Point, Line, Rect, Text, Image, UIPrimitive

FPS = 60
FRAME_TIME = int(1000 / FPS)


class KeyboardKeys(Enum):
    esc = 1
    ctrl = 29
    shift = 42
    alt = 56
    tab = 15
    enter = 28
    space = 57
    backspace = 14
    a = 30
    b = 48
    c = 46
    d = 32
    e = 18
    f = 33
    g = 34
    h = 35
    i = 23
    j = 36
    k = 37
    l = 38
    m = 50
    n = 49
    o = 24
    p = 25
    q = 16
    r = 19
    s = 31
    t = 20
    u = 22
    v = 47
    w = 17
    x = 45
    y = 21
    z = 44


class TimedEvent:
    callback: Callable[[], None]
    timeLeftMs: int
    args: list[any]
    kwargs: dict[any]
    onChangeCallback: Callable[[int], None]
    def __init__(self, timeLeftMs: int, callback: Callable[[], None], args=[], kwargs={}, onChangeCallback: Callable[[int], None] = lambda timeLeft: None):
        self.callback = callback
        self.timeLeftMs = timeLeftMs
        self.args = args
        self.kwargs = kwargs
        self.onChangeCallback = onChangeCallback
    def decreaseTime(self, timeMs):
        self.timeLeftMs -= timeMs
    def execCallbackIfTime0(self) -> bool:
        if self.timeLeftMs <= 0:
            self.callback(*self.args, **self.kwargs)
            return True
        return False
    def execOnChangeCallback(self):
        self.onChangeCallback(self.timeLeftMs)

class _Window(QMainWindow):
    objects: list[UIPrimitive] = []
    keysCallbacks: dict[KeyboardKeys, (Callable, list[Any])] = {}
    mousePressCallbacks: list[(Callable, list[Any])] = []
    mouseReleaseCallbacks: list[(Callable, list[Any])] = []
    mouseMoveCallbacks: list[(Callable, list[Any])] = []
    anchorMouseMovePoint: tuple[int, int] | None = None
    lastMouseMovePoint: tuple[int, int] | None = None
    currentMovingObject: UIPrimitive | None = None
    currentPressedObject: UIPrimitive | None = None
    timedEvents: set[TimedEvent] = set()


    def __init__(self, opacity=1.0, w=None, h=None):
        QMainWindow.__init__(
            self, None,
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

        def onKeyboardEvent(event: keyboard.KeyboardEvent):
            if event.event_type != keyboard.KEY_DOWN:
                return

            for key in self.keysCallbacks.keys():
                # print(event.name, event.scan_code)
                if event.scan_code == key:
                    self.keysCallbacks[key][0](*self.keysCallbacks[key][1])
        keyboard._listener.add_handler(onKeyboardEvent)

        self.startTimer(FRAME_TIME)

    def getCenter(self):
        return self.w / 2, self.h / 2

    def timerEvent(self, t):
        try:
            eventsToDelete = set()
            for event in self.timedEvents:
                event.decreaseTime(FRAME_TIME)
                event.execOnChangeCallback()
                if event.execCallbackIfTime0():
                    eventsToDelete.add(event)
            for event in eventsToDelete:
                self.timedEvents.remove(event)
            self.update()
        except KeyboardInterrupt:
            print("##############\nShutdown all...")
            exit()

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            objects = self.objects.copy()
            for obj in objects:
                obj.render(painter)
        except KeyboardInterrupt:
            print("##############\nShutdown all...")
            exit()

    def _updateObjectsHoverState(self, event: QMouseEvent, isMouseRelease: bool = False):
        for obj in self.objects:
            obj.updateHoverState(event.x(), event.y(), isMouseRelease)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.anchorMouseMovePoint = (event.x(), event.y())
        self.lastMouseMovePoint = (event.x(), event.y())
        for obj in self.objects:
            if obj.isHover(event.x(), event.y()):
                self.currentPressedObject = obj
                if obj.movable:
                    self.currentMovingObject = obj

        for callback in self.mousePressCallbacks:
            callback[0](event.x(), event.y(), *callback[1])

        self._updateObjectsHoverState(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.currentMovingObject is not None:
            if isinstance(self.currentMovingObject, Point):
                self.currentMovingObject.x = editLinkableValue(self.currentMovingObject.x, event.x())
                self.currentMovingObject.y = editLinkableValue(self.currentMovingObject.y, event.y())
            else:
                self.currentMovingObject.x = editLinkableValue(self.currentMovingObject.x, self.currentMovingObject.x + (event.x() - self.lastMouseMovePoint[0]))
                self.currentMovingObject.y = editLinkableValue(self.currentMovingObject.y, self.currentMovingObject.y + (event.y() - self.lastMouseMovePoint[1]))

            self.lastMouseMovePoint = (event.x(), event.y())

            onMoveCallback = getattr(self.currentMovingObject, 'onMoveCallback')
            if onMoveCallback is not None:
                onMoveCallback()

        for callback in self.mouseMoveCallbacks:
            callback[0](event.x(), event.y(), *callback[1])

        self._updateObjectsHoverState(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.currentPressedObject is not None and (
                (self.anchorMouseMovePoint[0] == event.x()) and (self.anchorMouseMovePoint[1] == event.y())
                or (not self.currentPressedObject.movable)
        ):
            objToClick = None
            for obj in self.objects:
                if obj.isHover(event.x(), event.y()) \
                        and (getattr(obj, 'onClickCallback') is not None):
                        # and (self.currentPressedObject is obj):
                    objToClick = obj
            if objToClick is not None:
                objToClick.onClickCallback(*objToClick.onClickCallbackArgs)
        self.lastMouseMovePoint = None
        self.anchorMouseMovePoint = None
        self.currentPressedObject = None

        self.currentMovingObject = None
        for callback in self.mouseReleaseCallbacks:
            callback[0](event.x(), event.y(), *callback[1])

        self._updateObjectsHoverState(event, True)


    def setTimeout(self, timeoutMs: int, callback: Callable, args=[], kwargs={}, onChangeCallback=lambda timeLeft: None):
        self.timedEvents.add(TimedEvent(timeoutMs, callback, args, kwargs, onChangeCallback))
        # or simpler but not works: QtCore.QTimer.singleShot(timeoutMs, callback)

    def addObjectAndDeleteAfterTime(self, obj: UIPrimitive, timeoutMS: int, onChangeCallback=lambda timeLeft: None):
        self.setTimeout(timeoutMS, lambda: self.removeObject(obj), [], {}, onChangeCallback)
        return self.addObject(obj)

    def addObject(self, obj: UIPrimitive):
        if not isinstance(obj, UIPrimitive):
            raise TypeError(f"Trying to add object that is not one of UIPrimitives. Object type: {type(obj)}")
        self.objects.append(obj)
        return obj

    def removeObject(self, obj: UIPrimitive):
        try:
            self.objects.remove(obj)
        except ValueError: # list.remove(x): x not in list
            pass
        return obj

    def clear(self):
        self.objects.clear()

    def getObjectsByType(self, objectType: UIPrimitive):
        res = []
        for obj in self.objects:
            if isinstance(obj, objectType):
                res.append(obj)
        return res

    def setKeyCallback(self, key: KeyboardKeys, callback: Callable, *args: list[Any]):
        self.keysCallbacks[key.value] = (callback, args)

    def setMouseCallback(self, eventType: QEvent.Type, callback: Callable, *args: list[Any]):
        if eventType == QEvent.MouseButtonPress:
            self.mousePressCallbacks.append((callback, args))
        elif eventType == QEvent.MouseButtonRelease:
            self.mouseReleaseCallbacks.append((callback, args))
        elif eventType == QEvent.MouseMove:
            self.mouseMoveCallbacks.append((callback, args))

    def clearKeyCallbacks(self):
        self.keysCallbacks = {}

    def clearMouseCallbacks(self):
        self.mousePressCallbacks = []
        self.mouseReleaseCallbacks = []
        self.mouseMoveCallbacks = []

    def clearAll(self):
        self.clearKeyCallbacks()
        self.clearMouseCallbacks()
        self.clear()


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

