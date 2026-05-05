import logging

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QColor

from UI.OverlayUI import OverlayUI
from UI.primitives import Text, Point
from UI.primitives.values import DEFAULT_FONT
from configs.translations import TEXTS
from controllers import Scenarios
from controllers.Scenarios.shared import PointTextAnchor, createNextBackButtonsAndText
from configs.constants import MARGIN
from utils import AppState


def enroll(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    createNextBackButtonsAndText(
        UI,
        AppState.translatedTexts[TEXTS.enroll],
        None, [],
        Scenarios.chooseLanguage, [UI],
    )

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
        Scenarios.configureThaumWindowCoords(UI)

    UI.setMouseCallback(QEvent.MouseMove, onMouseMove)
