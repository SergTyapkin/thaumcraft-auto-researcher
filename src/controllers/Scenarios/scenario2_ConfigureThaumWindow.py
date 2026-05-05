import logging

from PyQt5.QtGui import QColor

from UI.OverlayUI import OverlayUI
from UI.primitives import Point, Line, Rect
from configs.translations import TEXTS
from controllers import Scenarios
from controllers.Scenarios.shared import createNextBackButtonsAndText
from utils import AppState
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
        AppState.translatedTexts[TEXTS.configureThaumWindow],
        Scenarios.confirmThaumWindowSlots, [UI, rectThaumWindow.LT.x, rectThaumWindow.LT.y,
                                  rectThaumWindow.RB.x, rectThaumWindow.RB.y],
        Scenarios.chooseLanguage, [UI],
    )
