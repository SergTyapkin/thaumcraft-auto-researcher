import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QColor

from src.LinkableValue import LinkableCoord, LinkableValue
from src.OverlayUI import OverlayUI
from src.ThaumInteractor import ThaumInteractor
from src.UIPrimitives import Rect, Point, Line, Text, DEFAULT_FONT
from src.constants import MARGIN
from src.utils import distance, saveThaumControlsConfig, readThaumControlsConfig


pointTextAnchor = LinkableCoord(MARGIN, MARGIN)
def enroll(UI: OverlayUI):
    UI.setKeyCallback(Qt.Key_Return, configureThaumWindow, UI)

    UI.clearAll()

    (cx, cy) = UI.getCenter()
    UI.addObject(Text(
        pointTextAnchor.x, pointTextAnchor.y,
        """Привет. Сначала нужно будет дать знать программе, где на экране находится игра.
Для этого в этом окошке будет показан текст с подсказками.
Вот такие точки можно перемещать:

Чтобы двинуться дальше, перемести эту точку на жёлтую точку посередине экрана.
(Кстати, это окошко тоже можно переместить, передвинув черную точку в левом верхнем углу).""",
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        padding=MARGIN,
        movable=True, UI=UI,
    ))

    targetPointCoords = (cx, cy)
    UI.addObject(Point(targetPointCoords[0], targetPointCoords[1], color=QColor('yellow')))
    movablePoint = Point(MARGIN + MARGIN * 5, MARGIN + 4.25 * (DEFAULT_FONT.pointSize() * 2), movable=True)
    UI.addObject(movablePoint)

    def onMouseMove(x, y):
        if not movablePoint.isOnPoint(targetPointCoords[0], targetPointCoords[1]):
            return
        UI.clearMouseCallbacks()
        configureThaumWindow(UI)

    UI.setMouseCallback(QEvent.MouseMove, onMouseMove)


def configureThaumWindow(UI: OverlayUI):
    def getThaumWindowCoords():
        UI.clearAll()

        UI.addObject(Text(
            pointTextAnchor.x, pointTextAnchor.y,
            """Отлично! Сперва обозначим окно стола исследований.
Открой интерфейс стола исследований, а потом передвинь две точки так, 
чтобы прямоугольник обозначал границу этого окна.

Как будет готово, жми [Enter].""",
            color=QColor('white'),
            padding=MARGIN,
            withBackground=True,
            movable=True, UI=UI,
        ))

        (cx, cy) = UI.getCenter()
        rectLT = LinkableCoord(cx - 200, cy - 200)
        rectRB = LinkableCoord(cx + 200, cy + 200)
        UI.addObject(Line(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('brown')))
        UI.addObject(Line(rectRB.x, rectLT.y, rectLT.x, rectRB.y, dashed=True, color=QColor('brown')))
        rectThaumWindow = UI.addObject(
            Rect(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('yellow')))
        UI.addObject(Point(rectLT.x, rectLT.y, movable=True))
        UI.addObject(Point(rectRB.x, rectRB.y, movable=True))

        UI.setKeyCallback(Qt.Key_Return, confirmThaumWindowSlots,
                          rectThaumWindow.LT.x, rectThaumWindow.LT.y,
                          rectThaumWindow.RB.x, rectThaumWindow.RB.y)

    def confirmThaumWindowSlots(LTx, LTy, RBx, RBy):
        W = RBx - LTx
        H = RBy - LTy
        print(f"Thaum window configured at: ({int(LTx)}, {int(LTy)}) x ({int(RBx)}, {int(RBy)})")

        UI.clearAll()

        UI.addObject(Text(
            pointTextAnchor.x, pointTextAnchor.y,
            """Программа автоматически определила положения кнопок взаимодействия 
так, как ты видишь. Не факт, что это правильно, так что внимательно посмотри на точки,
и, если нужно, передвинь их точно на нужные слоты / кнопки. Вот список, где какие точки:

Желтые - слот для \"бумаги и пера\", слот для \"изучений\";
Зеленая область - страница выбора из 5х5 аспектов;
Голубые - переход по страницам аспектов влево / вправо;
Розовые - удаление аспектов из смешивателя, смешение аспектов;
Оранжевая область - место выкладывания аспектов в шестиугольники (очень важен центр);
Фиолетовая область - 9х3 внутренних слотов инвентаря.

Как будет готово - жми [Enter]
(!!! После завершения окно с игрой нельзя передвигать по экрану !!!)""",
            color=QColor('white'),
            padding=MARGIN,
            withBackground=True,
            movable=True, UI=UI,
        ))

        # Slots
        Ws = W / 15
        Hs = H / 10
        topSlotsY = LinkableValue(LTy + Hs * 0.85)
        pointWritingMaterials = UI.addObject(
            Point(LTx + Ws * 1, topSlotsY, movable=True, color=QColor('yellow')))  # writing materials
        pointPapers = UI.addObject(Point(LTx + Ws * 4.5, topSlotsY, movable=True, color=QColor('yellow')))  # scrolls

        rectLT = LinkableCoord(LTx + Ws * 0.25, LTy + Hs * 2.25)
        rectRB = LinkableCoord(LTx + Ws * 5.25, LTy + Hs * 7.25)
        UI.addObject(Line(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('brown')))
        UI.addObject(Line(rectRB.x, rectLT.y, rectLT.x, rectRB.y, dashed=True, color=QColor('brown')))
        rectAspectsListing = UI.addObject(
            Rect(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('lime')))
        UI.addObject(Point(rectLT.x, rectLT.y, movable=True))
        UI.addObject(Point(rectRB.x, rectRB.y, movable=True))  # aspects listing rectangle

        aspectsScrollY = LinkableValue(LTy + Hs * 7.65)
        pointAspectsScrollLeft = UI.addObject(
            Point(LTx + Ws * 2, aspectsScrollY, movable=True, color=QColor('lightblue')))  # aspects scroll left
        pointAspectsScrollRight = UI.addObject(
            Point(LTx + Ws * 3.5, aspectsScrollY, movable=True, color=QColor('lightblue')))  # aspects scroll right

        aspectsMixY = LinkableValue(LTy + Hs * 9)
        pointAspectsMixLeft = UI.addObject(
            Point(LTx + Ws * 1, aspectsMixY, movable=True, color=QColor('pink')))  # aspects mix left
        pointAspectsMixCreate = UI.addObject(
            Point(LTx + Ws * 2.75, aspectsMixY, movable=True, color=QColor('pink')))  # aspects mix create
        pointAspectsMixRight = UI.addObject(
            Point(LTx + Ws * 4.5, aspectsMixY, movable=True, color=QColor('pink')))  # aspects mix right

        rectLT = LinkableCoord(LTx + Ws * 2.55, LTy + Hs * 10.8)
        rectRB = LinkableCoord(LTx + Ws * 12.4, LTy + Hs * 14)
        UI.addObject(Line(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('brown')))
        UI.addObject(Line(rectRB.x, rectLT.y, rectLT.x, rectRB.y, dashed=True, color=QColor('brown')))
        rectInventory = UI.addObject(Rect(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('purple')))
        UI.addObject(Point(rectLT.x, rectLT.y, movable=True))
        UI.addObject(Point(rectRB.x, rectRB.y, movable=True))  # inventory rectangle

        rectLT = LinkableCoord(LTx + Ws * 5.7, LTy + Hs * 0.4)
        rectRB = LinkableCoord(LTx + Ws * 14.4, LTy + Hs * 9.6)
        UI.addObject(Line(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('brown')))
        UI.addObject(Line(rectRB.x, rectLT.y, rectLT.x, rectRB.y, dashed=True, color=QColor('brown')))
        rectHexagons = UI.addObject(Rect(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('orange')))
        UI.addObject(Point(rectLT.x, rectLT.y, movable=True))
        UI.addObject(Point(rectRB.x, rectRB.y, movable=True))  # hexagons rectangle

        def saveControls():
            UI.clearKeyCallbacks()
            saveThaumControlsConfig(pointWritingMaterials, pointPapers, rectAspectsListing.LT, rectAspectsListing.RB,
                                    pointAspectsScrollLeft, pointAspectsScrollRight,
                                    pointAspectsMixLeft, pointAspectsMixCreate, pointAspectsMixRight, rectInventory.LT,
                                    rectInventory.RB, rectHexagons.LT, rectHexagons.RB)
            TI = ThaumInteractor(readThaumControlsConfig())
            runResearching(UI, TI)

        UI.setKeyCallback(Qt.Key_Return, saveControls)

    getThaumWindowCoords()


def runResearching(UI: OverlayUI, TI: ThaumInteractor):
    UI.clearAll()
    
    
