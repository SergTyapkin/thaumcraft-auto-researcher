import logging

from PyQt5.QtGui import QColor

from UI.OverlayUI import OverlayUI
from UI.primitives import Text, Point, Line, Rect
from controllers.scenarios.scenario1_Enroll import enroll
from controllers.scenarios.scenario3_ConfirmThaumWindowSlots import confirmThaumWindowSlots
from controllers.scenarios.shared import createNextBackButtonsAndText
from utils.LinkableValue import LinkableCoord


def configureThaumWindowCoords(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    (cx, cy) = UI.getCenter()
    rectLT = LinkableCoord(cx - 200, cy - 200)
    rectRB = LinkableCoord(cx + 200, cy + 200)
    UI.addObject(Line(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('brown')))
    UI.addObject(Line(rectRB.x, rectLT.y, rectLT.x, rectRB.y, dashed=True, color=QColor('brown')))
    rectThaumWindow = UI.addObject(
        Rect(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('yellow')))
    UI.addObject(Point(rectLT.x, rectLT.y, movable=True))
    UI.addObject(Point(rectRB.x, rectRB.y, movable=True))
    logging.info("Configuring Thaum window rect dialogue successfully showed")

    createNextBackButtonsAndText(
        UI,
        """Отлично! Сперва обозначим окно стола исследований.
Откройте интерфейс стола исследований, а потом передвиньте две точки так, 
чтобы прямоугольник обозначал границу этого окна.""",
        confirmThaumWindowSlots, [UI, rectThaumWindow.LT.x, rectThaumWindow.LT.y,
                                  rectThaumWindow.RB.x, rectThaumWindow.RB.y],
        enroll, [UI],
    )
