import logging

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QColor

from UI.OverlayUI import OverlayUI
from UI.primitives import Text, Point
from UI.primitives.values import DEFAULT_FONT
from controllers.scenarios.scenario2_ConfigureThaumWindow import configureThaumWindowCoords
from controllers.scenarios.shared import pointTextAnchor
from utils.constants import MARGIN


def enroll(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    UI.addObject(Text(
        pointTextAnchor.x, pointTextAnchor.y,
        """Привет. Сначала нужно будет дать знать программе, где на экране находится игра.
Для этого в этом окошке будет показан текст с подсказками.
Вот такие точки можно перемещать:
Закрыть программу всегда можно кликом по крестику в правом верхнем углу.

Чтобы двинуться дальше, переместите эту точку на жёлтую точку посередине экрана.
(Кстати, это окошко тоже можно перемещать).""",
        color=QColor('white'),
        withBackground=True,
        padding=MARGIN,
        movable=True, UI=UI,
    ))

    (cx, cy) = UI.getCenter()
    targetPoint = Point(cx, cy, color=QColor('yellow'))
    UI.addObject(targetPoint)
    movablePoint = Point(MARGIN + MARGIN + DEFAULT_FONT.pointSize() * 2 * 16,
                         MARGIN + 3.4 * (DEFAULT_FONT.pointSize() * 2), movable=True)
    UI.addObject(movablePoint)
    logging.info("Enrollment successfully showed")

    def onMouseMove(x, y):
        if not movablePoint.isHover(targetPoint.x, targetPoint.y):
            return
        logging.info("Enrollment done")
        UI.clearMouseCallbacks()
        configureThaumWindowCoords(UI)

    UI.setMouseCallback(QEvent.MouseMove, onMouseMove)
