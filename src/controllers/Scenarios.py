from math import pi, tan
from math import sin
from math import cos

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QColor

from src.utils.LinkableValue import LinkableCoord, LinkableValue
from src.logic.LinksGeneration import generateLinkMap
from src.UI.OverlayUI import OverlayUI, KeyboardKeys
from src.controllers.ThaumInteractor import ThaumInteractor, createTI
from src.UI.UIPrimitives import Rect, Point, Line, Text, DEFAULT_FONT
from src.utils.constants import MARGIN, THAUM_ASPECTS_INVENTORY_SLOTS_X, THAUM_ASPECTS_INVENTORY_SLOTS_Y, \
    THAUM_HEXAGONS_SLOTS_COUNT, THAUM_ASPECT_RECIPES_CONFIG_PATH, THAUM_VERSION_CONFIG_PATH
from src.utils.utils import saveThaumControlsConfig, readJSONConfig, saveJSONConfig

pointTextAnchor = LinkableCoord(MARGIN, MARGIN)
def enroll(UI: OverlayUI):
    UI.clearAll()
    UI.setKeyCallback(KeyboardKeys.enter, configureThaumWindow, UI)

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

    (cx, cy) = UI.getCenter()
    targetPoint = Point(cx, cy, color=QColor('yellow'))
    UI.addObject(targetPoint)
    movablePoint = Point(MARGIN + MARGIN + DEFAULT_FONT.pointSize() * 2 * 16, MARGIN + 3.4 * (DEFAULT_FONT.pointSize() * 2), movable=True)
    UI.addObject(movablePoint)

    def onMouseMove(x, y):
        if not movablePoint.isHover(targetPoint.x, targetPoint.y):
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

Как будет готово, жми [Enter].
Чтобы вернуться назад, нажми [Backspace]""",
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

        UI.setKeyCallback(KeyboardKeys.enter, confirmThaumWindowSlots,
                          rectThaumWindow.LT.x, rectThaumWindow.LT.y,
                          rectThaumWindow.RB.x, rectThaumWindow.RB.y)
        UI.setKeyCallback(KeyboardKeys.backspace, enroll, UI)

    def confirmThaumWindowSlots(LTx, LTy, RBx, RBy):
        W = RBx - LTx
        H = RBy - LTy
        print(f"Thaum window configured at: ({int(LTx)}, {int(LTy)}) x ({int(RBx)}, {int(RBy)})")

        UI.clearAll()

        UI.addObject(Text(
            pointTextAnchor.x, pointTextAnchor.y,
            """Программа автоматически определила положения кнопок взаимодействия 
так, как ты видишь. Скорее всего сделала она это не точно, так что внимательно посмотри на точки,
и, если нужно, передвинь их точно на нужные слоты / кнопки. Вот список, где какие точки:

Желтые - слот для \"бумаги и пера\", слот для \"изучений\";
Зеленая область - выбор аспектов из стола 5х5. Важно, чтобы все
 линии с точностью до пары пикселей разделяли аспекты;
Голубые - переход по страницам аспектов влево / вправо;
Розовые - удаление аспектов из смешивателя, смешение аспектов;
Шестиугольная область - место выкладывания аспектов в ячейки 
 (очень важно совпадение всех центров ячеек на пересечениях линий);
Фиолетовая область - 9х3 внутренних слотов инвентаря.

Как будет готово - жми [Enter]
Чтобы вернуться назад, нажми [Backspace]
(!!! После завершения этой конфигурации, если окно с игрой не во весь экран, 
не передвигайте его по экрану !!)""",
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

        rectAspectsLT = LinkableCoord(LTx + Ws * 0.25, LTy + Hs * 2.25)
        rectAspectsRB = LinkableCoord(LTx + Ws * 5.25, LTy + Hs * 7.25)
        UI.addObject(Line(rectAspectsLT.x, rectAspectsLT.y, rectAspectsRB.x, rectAspectsRB.y, dashed=True, color=QColor('brown')))
        UI.addObject(Line(rectAspectsRB.x, rectAspectsLT.y, rectAspectsLT.x, rectAspectsRB.y, dashed=True, color=QColor('brown')))
        rectAspectsListing = UI.addObject(
            Rect(rectAspectsLT.x, rectAspectsLT.y, rectAspectsRB.x, rectAspectsRB.y, dashed=True, color=QColor('lime')))

        verticalListingLines = []
        for x in range(1, THAUM_ASPECTS_INVENTORY_SLOTS_X):
            xVal = rectAspectsLT.x + x * rectAspectsListing.w / THAUM_ASPECTS_INVENTORY_SLOTS_X
            line = Line(xVal, rectAspectsLT.y, xVal, rectAspectsRB.y, dashed=True, color=QColor('lime'), width=1)
            verticalListingLines.append(line)
            UI.addObject(line)
        horizontalListingLines = []
        for y in range(1, THAUM_ASPECTS_INVENTORY_SLOTS_Y):
            yVal = rectAspectsLT.y + y * rectAspectsListing.h / THAUM_ASPECTS_INVENTORY_SLOTS_Y
            line = Line(rectAspectsLT.x, yVal, rectAspectsRB.x, yVal, dashed=True, color=QColor('lime'), width=1)
            horizontalListingLines.append(line)
            UI.addObject(line)

        def updateListingRectCoords():
            rectW = rectAspectsRB.x - rectAspectsLT.x
            rectH = rectAspectsRB.y - rectAspectsLT.y
            for x in range(1, THAUM_ASPECTS_INVENTORY_SLOTS_X):
                xVal = rectAspectsLT.x + x * rectW / THAUM_ASPECTS_INVENTORY_SLOTS_X
                verticalListingLines[x - 1].S.x = xVal
                verticalListingLines[x - 1].E.x = xVal
            for y in range(1, THAUM_ASPECTS_INVENTORY_SLOTS_Y):
                yVal = rectAspectsLT.y + y * rectH / THAUM_ASPECTS_INVENTORY_SLOTS_Y
                horizontalListingLines[y - 1].S.y = yVal
                horizontalListingLines[y - 1].E.y = yVal
        UI.addObject(Point(rectAspectsLT.x, rectAspectsLT.y, movable=True,onMoveCallback=updateListingRectCoords))
        UI.addObject(Point(rectAspectsRB.x, rectAspectsRB.y, movable=True,onMoveCallback=updateListingRectCoords))  # aspects listing rectangle

        aspectsScrollY = LinkableValue(LTy + Hs * 7.65)
        pointAspectsScrollLeft = UI.addObject(Point(LTx + Ws * 2, aspectsScrollY, movable=True, color=QColor('lightblue')))  # aspects scroll left
        pointAspectsScrollRight = UI.addObject(Point(LTx + Ws * 3.5, aspectsScrollY, movable=True, color=QColor('lightblue')))  # aspects scroll right

        aspectsMixY = LinkableValue(LTy + Hs * 9)
        pointAspectsMixLeft = UI.addObject(Point(LTx + Ws * 1, aspectsMixY, movable=True, color=QColor('pink')))  # aspects mix left
        pointAspectsMixCreate = UI.addObject(Point(LTx + Ws * 2.75, aspectsMixY, movable=True, color=QColor('pink')))  # aspects mix create
        pointAspectsMixRight = UI.addObject(Point(LTx + Ws * 4.5, aspectsMixY, movable=True, color=QColor('pink')))  # aspects mix right

        rectLT = LinkableCoord(LTx + Ws * 2.55, LTy + Hs * 10.8)
        rectRB = LinkableCoord(LTx + Ws * 12.4, LTy + Hs * 14)
        UI.addObject(Line(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('brown')))
        UI.addObject(Line(rectRB.x, rectLT.y, rectLT.x, rectRB.y, dashed=True, color=QColor('brown')))
        rectInventory = UI.addObject(Rect(rectLT.x, rectLT.y, rectRB.x, rectRB.y, dashed=True, color=QColor('purple')))
        UI.addObject(Point(rectLT.x, rectLT.y, movable=True))
        UI.addObject(Point(rectRB.x, rectRB.y, movable=True))  # inventory rectangle

        rectHexagonsCC = LinkableCoord(LTx + Ws * 10, LTy + Hs * 5)
        rectHexagonsTy = LinkableValue(LTy + Hs * 0.25)
        verticalHexagonsLines = []
        deg30HexagonsLines = []
        deg60HexagonsLines = []
        for i in range(THAUM_HEXAGONS_SLOTS_COUNT):
            line = Line(0, 0, 0, 0, dashed=True, color=QColor('lightblue'), width=1)
            verticalHexagonsLines.append(line)
            UI.addObject(line)

            line = Line(0, 0, 0, 0, dashed=True, color=QColor('lightblue'), width=1)
            deg30HexagonsLines.append(line)
            UI.addObject(line)

            line = Line(0, 0, 0, 0, dashed=True, color=QColor('lightblue'), width=1)
            deg60HexagonsLines.append(line)
            UI.addObject(line)

        def updateHexagonsCoords():
            rad = rectHexagonsCC.y - rectHexagonsTy
            slotSizeY = rad / (THAUM_HEXAGONS_SLOTS_COUNT // 2)
            slotSizeX = slotSizeY * cos(pi / 6)
            for i in range(-THAUM_HEXAGONS_SLOTS_COUNT // 2, THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1):
                idx = i + THAUM_HEXAGONS_SLOTS_COUNT // 2
                verticalHexagonsLines[idx].S.x = rectHexagonsCC.x + i * slotSizeX
                verticalHexagonsLines[idx].E.x = rectHexagonsCC.x + i * slotSizeX
                verticalHexagonsLines[idx].S.y = rectHexagonsCC.y - rad + abs(i) * slotSizeY / 2
                verticalHexagonsLines[idx].E.y = rectHexagonsCC.y + rad - abs(i) * slotSizeY / 2

                deg30HexagonsLines[idx].S.x = rectHexagonsCC.x + cos(pi / 6) * rad + (i < 0) * i * slotSizeX
                deg30HexagonsLines[idx].E.x = rectHexagonsCC.x - cos(pi / 6) * rad + (i > 0) * i * slotSizeX
                deg30HexagonsLines[idx].S.y = rectHexagonsCC.y + sin(pi / 6) * rad - (i < 0) * i * slotSizeY / 2 - (i > 0) * i * slotSizeY
                deg30HexagonsLines[idx].E.y = rectHexagonsCC.y - sin(pi / 6) * rad - (i > 0) * i * slotSizeY / 2 - (i < 0) * i * slotSizeY

                deg60HexagonsLines[idx].S.x = -deg30HexagonsLines[idx].S.x + rectHexagonsCC.x * 2
                deg60HexagonsLines[idx].E.x = -deg30HexagonsLines[idx].E.x + rectHexagonsCC.x * 2
                deg60HexagonsLines[idx].S.y = deg30HexagonsLines[idx].S.y
                deg60HexagonsLines[idx].E.y = deg30HexagonsLines[idx].E.y
        updateHexagonsCoords()

        UI.addObject(Point(rectHexagonsCC.x, rectHexagonsCC.y, movable=True,
                           onMoveCallback=updateHexagonsCoords))
        UI.addObject(Point(rectHexagonsCC.x, rectHexagonsTy, movable=True,
                           onMoveCallback=updateHexagonsCoords))  # hexagons rectangle

        def saveControls():
            saveThaumControlsConfig(pointWritingMaterials, pointPapers, rectAspectsListing.LT, rectAspectsListing.RB,
                                    pointAspectsScrollLeft, pointAspectsScrollRight,
                                    pointAspectsMixLeft, pointAspectsMixCreate, pointAspectsMixRight, rectInventory.LT,
                                    rectInventory.RB, rectHexagonsCC, (rectHexagonsCC.y - rectHexagonsTy) / (THAUM_HEXAGONS_SLOTS_COUNT // 2))
            waitForCreatingTI(UI)

        UI.setKeyCallback(KeyboardKeys.enter, saveControls)
        UI.setKeyCallback(KeyboardKeys.backspace, configureThaumWindow, UI)

    getThaumWindowCoords()

def chooseThaumVersion(UI: OverlayUI):
    UI.clearAll()
    infoText = UI.addObject(Text(
        pointTextAnchor.x, pointTextAnchor.y,
        f"""Выберите версию Thaumcraft.
От этого будут зависеть рецепты получения аспектов.

Чтобы вернуться назад, нажми [Backspace]""",
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        padding=MARGIN,
        movable=True, UI=UI,
    ))
    recipesConfig = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
    versions = list(recipesConfig.keys())
    versionsObjects = []
    def updateVersionsY():
        for i in range(len(versionsObjects)):
            versionObject = versionsObjects[i]
            versionObject.y = pointTextAnchor.y + MARGIN + infoText.h + i * MARGIN * 4

    infoText.LT.onMoveCallback = updateVersionsY
    for i in range(len(versions)):
        version = versions[i]
        def onClickVersion():
            print("Selected thaum version:", version)
            saveJSONConfig(THAUM_VERSION_CONFIG_PATH, {'version': version})
            waitForCreatingTI(UI)
        versionObject = UI.addObject(Text(
            pointTextAnchor.x, pointTextAnchor.y + MARGIN + infoText.h + i * MARGIN * 4,
            version,
            color=QColor('white'),
            withBackground=True,
            backgroundColor=QColor('black'),
            padding=MARGIN,
            UI=UI,
            onClickCallback=onClickVersion,
        ))
        versionsObjects.append(versionObject)
    UI.setKeyCallback(KeyboardKeys.backspace, configureThaumWindow, UI)

def waitForCreatingTI(UI: OverlayUI):
    UI.clearAll()

    UI.addObject(Text(
        pointTextAnchor.x, pointTextAnchor.y,
        """Определяем аспекты в твоем столе.
Перенеси это окно так, чтобы оно не перекрывало окно с игрой
и нажми [Enter]
Чтобы вернуться назад, нажми [Backspace]""",
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        padding=MARGIN,
        movable=True, UI=UI,
    ))

    def startCreatingTI():
        UI.clearAll()
        TI = createTI(UI)
        if TI is not None:
            runResearching(UI, TI)
    UI.setKeyCallback(KeyboardKeys.enter, startCreatingTI)
    UI.setKeyCallback(KeyboardKeys.backspace, chooseThaumVersion, UI)


def runResearching(UI: OverlayUI, TI: ThaumInteractor):
    UI.clearAll()

    # TI.getAvailableAspects()
    # TI.printAvailableAspects()
    # breakpoint()

    def fillMapAndStartAgain(existingAspects, noneHexagons):
        print("Existing aspects:", existingAspects)
        print("Free hexagons:", noneHexagons)
        linkMap = generateLinkMap(existingAspects, noneHexagons)
        print("Solved:", linkMap)
        # breakpoint()
        print("Starting to put aspects on field...")
        TI.fillByLinkMap(linkMap)
        print("Putting aspects is done")
        TI.takeOutPaper()
        TI.eventsDelay()
        runResearching(UI, TI)

    TI.insertPaper()
    TI.renderDelay()
    TI.getExistingAspectsOnField(fillMapAndStartAgain)
