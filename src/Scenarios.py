import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from src.OverlayUI import OverlayUI, LinkableCoord
from src.UIPrimitives import Rect, Point, Line, Text
from src.constants import MARGIN


def configureThaumWindow(UI):
    def getThaumWindowCoords():
        UI.setKeyCallback(Qt.Key_Return, confirmThaumWindowSlots)

        UI.clear()
        (cx, cy) = UI.getCenter()
        rectLT = LinkableCoord(cx - 200, cy - 200)
        rectRB = LinkableCoord(cx + 200, cy + 200)
        UI.addObject(Line(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('brown')))
        UI.addObject(Line(rectRB.x, rectLT.y, rectLT.x, rectRB.y, dashed=True, color=QColor('brown')))
        UI.addObject(Rect(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('yellow')))
        UI.addObject(Point(rectLT.x, rectLT.y, movable=True))
        UI.addObject(Point(rectRB.x, rectRB.y, movable=True))
        text = Text(
            MARGIN * 2, MARGIN * 2,
            """Сперва обозначим окно стола исследований.
    Открой интерфейс стола исследований, а потом передвинь две точки так, 
    чтобы прямоугольник обозначал границу этого окна.""",
            color=QColor('white')
        )
        UI.addObject(Rect(text.x - MARGIN, text.y - MARGIN, text.x + text.w + MARGIN * 2, text.y + text.h + MARGIN * 2,
                          lineWidth=2, color=QColor('black'), fill=QColor('black'), fillOpacity=0.5))
        UI.addObject(text)

    def confirmThaumWindowSlots():
        # UI.setKeyCallback(Qt.Key_Return, UNKNOWN_FOO)

        [windowLT, windowRB] = UI.getObjectsByFilter(Point)
        print("Thaum window at:", int(windowLT.x), int(windowLT.y), int(windowRB.x), int(windowRB.y))

        UI.clear()


    getThaumWindowCoords()
