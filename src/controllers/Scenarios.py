import logging
import math
import threading
import time
from math import pi, tan
from math import sin
from math import cos

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QColor

from src.UI import UIPrimitives
from src.logic.LinksGeneration import generateLinkMap
from src.utils.LinkableValue import LinkableCoord, LinkableValue
from src.UI.OverlayUI import OverlayUI, KeyboardKeys
from src.controllers.ThaumInteractor import ThaumInteractor, createTI, Aspect
from src.UI.UIPrimitives import Rect, Point, Line, Text, DEFAULT_FONT
from src.utils.constants import MARGIN, THAUM_ASPECTS_INVENTORY_SLOTS_X, THAUM_ASPECTS_INVENTORY_SLOTS_Y, \
    THAUM_HEXAGONS_SLOTS_COUNT, THAUM_ASPECT_RECIPES_CONFIG_PATH, THAUM_VERSION_CONFIG_PATH, \
    THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH
from src.utils.utils import saveThaumControlsConfig, readJSONConfig, saveJSONConfig, eventsDelay, renderDelay, \
    saveThaumVersionConfig, loadThaumVersionConfig

pointTextAnchor = LinkableCoord(MARGIN, MARGIN)
def enroll(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()
    UI.setKeyCallback([KeyboardKeys.enter], configureThaumWindowCoords, UI)

    UI.addObject(Text(
        pointTextAnchor.x, pointTextAnchor.y,
        """Привет. Сначала нужно будет дать знать программе, где на экране находится игра.
Для этого в этом окошке будет показан текст с подсказками.
Вот такие точки можно перемещать:
Закрыть программу всегда можно кликом по крестику в правом верхнем углу.

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
    logging.info("Enrollment successfully showed")

    def onMouseMove(x, y):
        if not movablePoint.isHover(targetPoint.x, targetPoint.y):
            return
        logging.info("Enrollment done")
        UI.clearMouseCallbacks()
        configureThaumWindowCoords(UI)

    UI.setMouseCallback(QEvent.MouseMove, onMouseMove)


def configureThaumWindowCoords(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

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
    logging.info("Configuring Thaum window rect dialogue successfully showed")

    UI.setKeyCallback([KeyboardKeys.enter], confirmThaumWindowSlots,UI, rectThaumWindow.LT.x, rectThaumWindow.LT.y, rectThaumWindow.RB.x, rectThaumWindow.RB.y)
    UI.setKeyCallback([KeyboardKeys.backspace], enroll, UI)

def confirmThaumWindowSlots(UI, LTx, LTy, RBx, RBy):
    thaumWindowWidth = RBx - LTx
    thaumWindowHeight = RBy - LTy
    logging.info(f"Thaum window configured at: ({int(LTx)}, {int(LTy)}) x ({int(RBx)}, {int(RBy)}), width={thaumWindowWidth}, height={thaumWindowHeight}")

    UI.clearAll()
    UI.createExitButton()

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
    Ws = thaumWindowWidth / 15
    Hs = thaumWindowHeight / 10
    topSlotsY = LinkableValue(LTy + Hs * 0.85)
    pointWritingMaterials = UI.addObject(
        Point(LTx + Ws * 1, topSlotsY, movable=True, color=QColor('yellow')))  # writing materials
    pointPapers = UI.addObject(Point(LTx + Ws * 4.5, topSlotsY, movable=True, color=QColor('yellow')))  # scrolls

    rectAspectsLT = LinkableCoord(LTx + Ws * 0.25, LTy + Hs * 2.25)
    rectAspectsRB = LinkableCoord(LTx + Ws * 5.2, LTy + Hs * 7.25)
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
    rectHexagonsTy = LinkableValue(LTy + Hs * 1.05)
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
    logging.info("Configuring Thaum controls coordinates in window dialogue successfully showed")

    def saveControls():
        saveThaumControlsConfig(pointWritingMaterials, pointPapers, rectAspectsListing.LT, rectAspectsListing.RB,
                                pointAspectsScrollLeft, pointAspectsScrollRight,
                                pointAspectsMixLeft, pointAspectsMixCreate, pointAspectsMixRight, rectInventory.LT,
                                rectInventory.RB, rectHexagonsCC, (rectHexagonsCC.y - rectHexagonsTy) / (THAUM_HEXAGONS_SLOTS_COUNT // 2))
        waitForCreatingTI(UI)

    UI.setKeyCallback([KeyboardKeys.enter], saveControls)
    UI.setKeyCallback([KeyboardKeys.backspace], configureThaumWindowCoords, UI)

def chooseThaumVersion(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()
    infoText = UI.addObject(Text(
        pointTextAnchor.x, pointTextAnchor.y,
        f"""Выберите версию Thaumcraft и установленные моды-аддоны.
От этого будут зависеть рецепты получения аспектов.
Если установленный тобой аддон отсутствует в этом списке, то эта программа
помочь тебе не сможет. Напиши нам об этом и мы добавим этот аддон

Когда выберешь, нажми [Enter]
Чтобы вернуться назад, нажми [Backspace]

Выбери версию:      Выбери аддоны:""",
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        padding=MARGIN,
        movable=True,
        UI=UI,
    ))
    recipesConfig = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
    versions = list(recipesConfig.keys())
    versionsObjects = []
    addonsObjects = []
    addonsRecipesConfig = readJSONConfig(THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH)
    addonsSelectingState: dict[str, bool] = {}
    for addonName in addonsRecipesConfig.keys():
        addonsSelectingState[addonName] = False

    selectedVersionObject: list[Text|None] = [None]
    selectedVersion: list[str|None] = [None]

    (oldVersion, oldAddons) = loadThaumVersionConfig()
    logging.info(f"Old selected version is: {oldVersion}. Old selected addons is: {oldAddons}")

    def updateVersionsPosition():
        for i in range(len(versionsObjects)):
            versionObject = versionsObjects[i]
            versionObject.y = pointTextAnchor.y + MARGIN + infoText.h + i * MARGIN * 4
        for i in range(len(addonsObjects)):
            addonObject = addonsObjects[i]
            addonObject.x = pointTextAnchor.x + 250
            addonObject.y = pointTextAnchor.y + MARGIN + infoText.h + i * MARGIN * 4

    infoText.LT.onMoveCallback = updateVersionsPosition
    curX = pointTextAnchor.x
    curY = pointTextAnchor.y + MARGIN + infoText.h
    for i in range(len(versions)):
        version = versions[i]
        def onClickVersion(versionObject, version):
            logging.debug(f"Click on version {version}")
            selectVersion(versionObject, version)
        def selectVersion(versionObject, version):
            if selectedVersionObject[0] is not None:
                selectedVersionObject[0].setColor(QColor('white'))
            logging.debug(f"Version {version} selected in UI. Previous selected version is {selectedVersion[0]}")
            selectedVersion[0] = version
            selectedVersionObject[0] = versionObject
            selectedVersionObject[0].setColor(QColor('purple'))

        versionObject = UI.addObject(Text(
            curX, curY,
            version,
            color=QColor('white'),
            withBackground=True,
            backgroundColor=QColor('black'),
            padding=MARGIN,
            UI=UI,
            onClickCallback=onClickVersion,
            hoverable=True,
        ))
        versionObject.onClickCallbackArgs = [versionObject, version]
        versionsObjects.append(versionObject)
        if oldVersion == version:
            selectVersion(versionObject, version)
        curY += MARGIN * 4

    addonsNames = list(addonsSelectingState.keys())
    curX = pointTextAnchor.x + 250
    curY = pointTextAnchor.y + MARGIN + infoText.h
    startCurY = curY
    for i in range(len(addonsNames)):
        addonName = addonsNames[i]
        def onClickAddon(addonObject, addonName):
            logging.debug(f"Click on addon {addonName}")
            toggleAddonSelecting(addonObject, addonName)
        def toggleAddonSelecting(addonObject, addonName):
            addonsSelectingState[addonName] = not addonsSelectingState[addonName]
            if addonsSelectingState[addonName] is True:
                addonObject.setColor(QColor('green'))
                logging.debug(f"Selected addon {addonName}")
            else:
                addonObject.setColor(QColor('white'))
                logging.debug(f"Deselected addon {addonName}")
        addonObject = UI.addObject(Text(
            curX, curY,
            addonName,
            color=QColor('white'),
            withBackground=True,
            backgroundColor=QColor('black'),
            padding=MARGIN,
            UI=UI,
            onClickCallback=onClickAddon,
            hoverable=True,
        ))
        addonObject.onClickCallbackArgs = [addonObject, addonName]
        addonsObjects.append(addonObject)
        if addonName in (oldAddons or []):
            toggleAddonSelecting(addonObject, addonName)
        curY += MARGIN * 4
        if curY > UI.height() - addonObject.h:
            curX += 500
            curY = startCurY

    def onSumbit():
        if selectedVersion[0] is None:
            logging.warning(f"Enter pressed in dialogue but thaum version is not selected")
            return
        selectedAddons = []
        for addon, state in addonsSelectingState.items():
            if state is True:
                selectedAddons.append(addon)
        logging.info(f"Selected thaum version:{selectedVersion[0]}")
        logging.info(f"Selected addons: {selectedAddons}")
        saveThaumVersionConfig(selectedVersion[0], selectedAddons)
        waitForCreatingTI(UI)

    logging.info(f"Selecting version and addons dialogue showed. Versions: {versions}, Addons: {addonsNames}")

    UI.setKeyCallback([KeyboardKeys.enter], onSumbit)
    UI.setKeyCallback([KeyboardKeys.backspace], configureThaumWindowCoords, UI)

def beReadyForStartSolving(UI: OverlayUI):
    logging.info(f"Be ready for solving scenario started")
    UI.clearAll()
    UI.createExitButton()

    UI.addObject(UIPrimitives.Text(
        MARGIN, MARGIN,
        f"""Сейчас нейросеть будет определять аспекты, находящиеся на поле. 
Необходимо подключение к интернету.
Выложи записку исследования в ячейку стола, а инвентарь заполни записками исследований,
начиная с самого верхнего левого слота. Они будут исследоваться по очереди

Как будет готово, жми [Enter]
Чтобы вернуться назад, нажми [Backspace]""",
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        padding=MARGIN,
        UI=UI,
        movable=True,
    ))

    UI.setKeyCallback([KeyboardKeys.enter], waitForCreatingTI, UI)
    UI.setKeyCallback([KeyboardKeys.backspace], chooseThaumVersion, UI)


def waitForCreatingTI(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

#     UI.addObject(Text(
#         pointTextAnchor.x, pointTextAnchor.y,
#         """Определяем аспекты в твоем столе.
# Перенеси это окно так, чтобы оно не перекрывало окно с игрой
# и нажми [Enter]
# Чтобы вернуться назад, нажми [Backspace]""",
#         color=QColor('white'),
#         withBackground=True,
#         backgroundColor=QColor('black'),
#         padding=MARGIN,
#         movable=True, UI=UI,
#     ))

    def startCreatingTI():
        UI.clearAll()
        UI.createExitButton()
        TI = createTI(UI)
        if TI is None:
            logging.critical(f"ThaumcraftInteractor was not created!")
            return
        runResearching(UI, TI)
    # UI.setKeyCallback(KeyboardKeys.enter, startCreatingTI)
    # UI.setKeyCallback(KeyboardKeys.backspace, chooseThaumVersion, UI)
    startCreatingTI()


def runResearching(UI: OverlayUI, TI: ThaumInteractor):
    logging.info(f"Run researching scenario started")
    UI.clearAll()
    exitButtonObject = UI.createExitButton()

    class Cell:
        x: int = None
        y: int = None
        object: UIPrimitives.Circle = None
        imageObject: UIPrimitives.Image = None
        aspect: Aspect = None
        isNone: bool = False

        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y
        def __repr__(self):
            return f"Cell([{self.x}, {self.y}], aspect={self.aspect}, isNone={self.isNone})"

    cells: list[Cell] = []
    selectedCell: list[Cell | None, QColor | None] = [None, None]  # list to make it mutable
    currentLinkMap: list[dict[(int, int), str]] = [{}]  # list to make it mutable

    cellColorFree = QColor('white')
    cellColorNone = QColor('black')
    cellColorAspect = QColor('antiquewhite')
    cellColorFree.setAlpha(20)
    cellColorNone.setAlpha(150)
    cellColorAspect.setAlpha(200)

    # it all Lists to make them mutable
    existingAspects = [{}]
    freeHexagons = [set()]
    noneHexagons = [set()]
    isUnstoppableModeOn = [False]

    activeStateDialogueObjects = []
    pausedStateDialogueObjects = []
    cellSettingsStateDialogueObjects = []
    cellsObjects = []

    def updateDetectingField():
        logging.debug(f'Run detecting aspects on field')
        UI.setAllObjectsVisibility(False)
        (existingAspects[0], noneHexagons[0], freeHexagons[0]) = TI.getExistingAspectsOnField()
        switchToActiveState()
        logging.debug(f'Aspects on field detected')

    def updateSolving():
        logging.debug(f'Starts updating solve...')
        # Start solving
        currentLinkMap[0] = generateLinkMap(existingAspects[0], noneHexagons[0])
        logging.debug(f'New solving generated {currentLinkMap[0]}')
        # Rerender cells images
        updateCellsImage()

    def updateCellsImage():
        # Fill cells by gotten solve
        aspectsCoords = currentLinkMap[0].keys()
        for cell in cells:
            cell.isNone = True
            cell.aspect = None
            cell.imageObject.clearImage()
            # is aspect:
            for coords in aspectsCoords:
                if (cell.x == coords[0]) and (cell.y == coords[1]):
                    aspectObj = TI.getAspectByName(currentLinkMap[0][coords])
                    cell.aspect = aspectObj
                    cell.isNone = False
                    cell.object.setColor(cellColorAspect)
                    cell.imageObject.setImage(aspectObj.pixMapImage)
                    break
            # is free:
            if (cell.x, cell.y) in freeHexagons[0]:
                if cell.aspect is not None:
                    continue
                cell.isNone = False
                cell.object.setColor(cellColorFree)
            # is none:
            if cell.isNone:
                cell.object.setColor(cellColorNone)
        logging.debug(f'New images placed to all cells')

    def onClickCellIsNone():
        logging.debug(f'Click on "Cell is none". Selected cell: {selectedCell[0]}')
        if selectedCell[0] is None:
            return
        coords = (selectedCell[0].x, selectedCell[0].y)
        if existingAspects[0].get(coords) is not None: del existingAspects[0][coords]
        freeHexagons[0].discard(coords)
        noneHexagons[0].add(coords)
        selectedCell[0] = None
        updateSolving()
        switchToActiveState()

    def onClickCellIsAspect(aspect: Aspect):
        logging.debug(f'Click on "Cell is aspect {aspect}". Selected cell: {selectedCell[0]}')
        if selectedCell[0] is None:
            return
        coords = (selectedCell[0].x, selectedCell[0].y)
        existingAspects[0][coords] = aspect.name
        freeHexagons[0].discard(coords)
        noneHexagons[0].discard(coords)
        selectedCell[0] = None
        updateSolving()
        switchToActiveState()

    def onClickCellIsFree():
        logging.debug(f'Click on "Cell is free". Selected cell: {selectedCell[0]}')
        if selectedCell[0] is None:
            return
        coords = (selectedCell[0].x, selectedCell[0].y)
        if existingAspects[0].get(coords) is not None: del existingAspects[0][coords]
        freeHexagons[0].add(coords)
        noneHexagons[0].discard(coords)
        selectedCell[0] = None
        updateSolving()
        switchToActiveState()

    def startCellDialogue(cell: Cell):
        switchToCellSettingsState()
        if selectedCell[0]:
            newColor = QColor(selectedCell[0].object.color)
            newColor.setAlpha(selectedCell[1])
            selectedCell[0].object.setColor(newColor)
        selectedCell[0] = cell
        newColor = QColor(cell.object.color)
        selectedCell[1] = newColor.alpha()
        newColor.setAlpha(130)
        cell.object.setColor(newColor)
        logging.debug(f'Showed cell state selecting dialogue')

    def exitCellDialogue():
        switchToActiveState()
        if not selectedCell[0]:
            return
        newColor = QColor(selectedCell[0].object.color)
        newColor.setAlpha(selectedCell[1])
        selectedCell[0].object.setColor(newColor)
        selectedCell[0] = None
        logging.debug(f'Exit cell state selecting dialogue. Showed only cells field')


    # draw clickable cells
    for ix in range(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1, THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1):
        for iy in range(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + (abs(ix) + 1) // 2 + 1, THAUM_HEXAGONS_SLOTS_COUNT // 2 - (abs(ix)) // 2 + 1):
            hexagonCenterX = TI.rectHexagonsCC.x + ix * TI.hexagonSlotSizeX
            hexagonCenterY = TI.rectHexagonsCC.y + iy * TI.hexagonSlotSizeY - (ix % 2) * TI.hexagonSlotSizeY / 2
            cell = Cell(ix, iy)
            cellObject = UIPrimitives.Circle(
                hexagonCenterX,
                hexagonCenterY,
                r=TI.hexagonSlotSizeY / 2,
                color=cellColorFree,
                onClickCallback=startCellDialogue,
                onClickCallbackArgs=[cell],
                hoverable=True,
            )
            cell.object = cellObject
            imageSide = TI.hexagonSlotSizeY / math.sqrt(2)
            cellAspectImageObject = UIPrimitives.Image(
                hexagonCenterX,
                hexagonCenterY - imageSide,
                imageSide,
                imageSide,
                None
            )
            cell.imageObject = cellAspectImageObject
            cells.append(cell)
            cellsObjects.append(cellAspectImageObject)
            cellsObjects.append(cellObject)
            UI.addObject(cellObject)
            UI.addObject(cellAspectImageObject)

    # draw cell dialogue
    textYCoord = MARGIN
    textCellIsNone = UI.addObject(UIPrimitives.Text(
        MARGIN, textYCoord,
        'Ячейка недоступна (N)',
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        backgroundOpacity=0.8,
        padding=MARGIN,
        UI=UI,
        onClickCallback=onClickCellIsNone,
        hoverable=True,
    ))
    cellSettingsStateDialogueObjects.append(textCellIsNone)
    textYCoord += textCellIsNone.h + MARGIN
    textCellIsFree = UI.addObject(UIPrimitives.Text(
        MARGIN, textYCoord,
        'Ячейка свободна (F)',
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        backgroundOpacity=0.8,
        padding=MARGIN,
        UI=UI,
        onClickCallback=onClickCellIsFree,
        hoverable=True,
    ))
    cellSettingsStateDialogueObjects.append(textCellIsFree)
    textYCoord += textCellIsFree.h + MARGIN * 2
    startTextYCoord = textYCoord
    textXCoord = MARGIN
    for i in range(len(TI.allAspects)):
        aspect = TI.allAspects[i]
        textAspect = UI.addObject(UIPrimitives.Text(
            textXCoord, textYCoord,
            aspect.name,
            color=QColor('white'),
            withBackground=True,
            backgroundColor=QColor('black'),
            backgroundOpacity=0.8,
            padding=(MARGIN, MARGIN, MARGIN, MARGIN * 4),
            UI=UI,
            onClickCallback=onClickCellIsAspect,
            onClickCallbackArgs=[aspect],
            hoverable=True,
        ))
        aspectImage = UI.addObject(UIPrimitives.Image(
            textXCoord + MARGIN * 2, textYCoord,
            MARGIN * 2, MARGIN * 2,
            None,
            ))
        aspectImage.setImage(aspect.pixMapImage)
        cellSettingsStateDialogueObjects.append(textAspect)
        cellSettingsStateDialogueObjects.append(aspectImage)
        textYCoord += textAspect.h
        if textYCoord > UI.height() - textAspect.h:
            textYCoord = startTextYCoord
            textXCoord += 250
    UI.setObjectsVisibility(cellSettingsStateDialogueObjects, False)

    # draw base dialogue
    activeStateTextObject = UI.addObject(UIPrimitives.Text(
        pointTextAnchor.x, pointTextAnchor.y,
        f"""Нейросеть определила аспекты на поле.
Чтобы перегенерировать полученную цепочку решения, нажми [R]
Если аспекты определены неверно, можно кликнуть на ячейку 
и выбрать, что в ней должно быть на самом деле. 

Чтобы приостановить программу, нажми [Ctrl + Shift + Пробел]
Если все определено правильно, жми [Enter]
Чтобы включить безостановочный режим, жми вместо этого [Ctrl + Enter]
Чтобы вернуться назад, нажми [Backspace]""",
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        padding=MARGIN,
        UI=UI,
        movable=True,
    ))
    activeStateDialogueObjects.append(activeStateTextObject)

    def startPuttingLinkMap():
        UI.setAllObjectsVisibility(False)
        onProcessText = UI.addObject(UIPrimitives.Text(
            MARGIN, MARGIN,
            f"""Подожди, решение выкладывается на поле... 
Не двигай мышью и не нажимай никакие кнопки.

Для экстренного закрытия программы нажми [Ctrl + Shift + Alt]""",
            color=QColor('white'),
            withBackground=True,
            backgroundColor=QColor('black'),
            padding=MARGIN,
        ))
        UI.clearKeyCallbacks()
        UI.setKeyCallback([KeyboardKeys.ctrl, KeyboardKeys.shift, KeyboardKeys.alt], UI.exit)

        finalLinkMap = currentLinkMap[0].copy()
        # Удаляем исходные аспекты из карты заполнения
        for aspectCoords in existingAspects[0].keys():
            del finalLinkMap[aspectCoords]

        def startPuttingAspects():
            logging.info("Putting aspects started...")
            TI.fillByLinkMap(finalLinkMap)
            logging.info("Putting aspects done")
            TI.takeOutPaper()
            eventsDelay()
            TI.increaseWorkingSlot()
            goToNextSlot()
            UI.removeObject(onProcessText)

        puttingAspectsThread = threading.Thread(target=startPuttingAspects)  # run in thread to not blocking keys callbacks
        puttingAspectsThread.start()


    def goToNextSlot():
        logging.info("Going to next slot")
        TI.insertPaper()
        TI.moveMouseInSafePos()
        existingAspects[0].clear()
        freeHexagons[0].clear()
        noneHexagons[0].clear()
        currentLinkMap[0].clear()
        updateCellsImage()
        renderDelay()
        updateDetectingField()
        updateSolving()
        switchToActiveState()
        logging.info("Everything prepared to next detecting")
        if isUnstoppableModeOn[0]:
            startPuttingLinkMap()

    onPausedText = UI.addObject(UIPrimitives.Text(
        MARGIN, MARGIN,
        f"""Программа проистановлена.

Чтобы продолжить работу, нажми [Ctrl + Shift + Пробел]""",
        color=QColor('white'),
        withBackground=True,
        backgroundColor=QColor('black'),
        padding=MARGIN,
        movable=True,
        UI=UI,
    ))
    pausedStateDialogueObjects.append(onPausedText)

    def switchToActiveState():
        logging.info("Switching to active state")
        def setUnstoppableModeOn():
            isUnstoppableModeOn[0] = True
        UI.clearKeyCallbacks()
        UI.setKeyCallback([KeyboardKeys.ctrl, KeyboardKeys.enter], setUnstoppableModeOn)
        UI.setKeyCallback([KeyboardKeys.enter], startPuttingLinkMap)
        UI.setKeyCallback([KeyboardKeys.r], updateSolving)
        UI.setKeyCallback([KeyboardKeys.backspace], beReadyForStartSolving, UI)
        UI.setKeyCallback([KeyboardKeys.ctrl, KeyboardKeys.shift, KeyboardKeys.space], switchToPausedState)
        UI.setAllObjectsVisibility(False)
        UI.setObjectsVisibility(activeStateDialogueObjects, True)
        UI.setObjectsVisibility(cellsObjects, True)
        exitButtonObject.setVisibility(True)

    def switchToPausedState():
        logging.info("Switching to paused state")
        UI.clearKeyCallbacks()
        UI.setKeyCallback([KeyboardKeys.ctrl, KeyboardKeys.shift, KeyboardKeys.space], switchToActiveState)
        UI.setAllObjectsVisibility(False)
        UI.setObjectsVisibility(pausedStateDialogueObjects, True)

    def switchToCellSettingsState():
        logging.info("Switching to cell settings state")
        UI.clearKeyCallbacks()
        UI.setKeyCallback([KeyboardKeys.n], onClickCellIsNone)
        UI.setKeyCallback([KeyboardKeys.f], onClickCellIsFree)
        UI.setKeyCallback([KeyboardKeys.esc], exitCellDialogue)
        UI.setAllObjectsVisibility(False)
        UI.setObjectsVisibility(cellSettingsStateDialogueObjects, True)
        UI.setObjectsVisibility(cellsObjects, True)
        exitButtonObject.setVisibility(True)

    updateDetectingField()
    updateSolving()
    switchToActiveState()
    logging.debug("Hexagon field with configuring initial aspects showed")

