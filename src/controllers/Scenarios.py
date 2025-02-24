import logging
import math
import threading
from math import cos
from math import pi
from math import sin
from typing import Callable

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QColor, QFont

from UI.primitives.Text import Align
from src.UI.OverlayUI import OverlayUI, KeyboardKeys
from src.UI.primitives import Circle, Image, Line, Point, Rect, Text, UIPrimitive
from src.UI.primitives.values import DEFAULT_FONT
from src.controllers.Aspect import Aspect
from src.controllers.ThaumInteractor import ThaumInteractor, createTI
from src.logic.LinksGeneration import generateLinkMap
from src.utils.LinkableValue import LinkableCoord, LinkableValue
from src.utils.constants import MARGIN, THAUM_ASPECTS_INVENTORY_SLOTS_X, THAUM_ASPECTS_INVENTORY_SLOTS_Y, \
    THAUM_HEXAGONS_SLOTS_COUNT, THAUM_ASPECT_RECIPES_CONFIG_PATH, DELAY_BETWEEN_RENDER, DELAY_BETWEEN_EVENTS, \
    LINK_GENERATION_MAX_TIME_MS
from src.utils.utils import saveThaumControlsConfig, readJSONConfig, eventsDelay, renderDelay, \
    saveThaumVersionConfig, loadThaumVersionConfig

pointTextAnchor = LinkableCoord(MARGIN, MARGIN)


def createButtonsAndText(
        UI: OverlayUI, text: str,
        buttons: list[tuple[str, Callable, list[any]]],
        x: int = pointTextAnchor.x, y: int = pointTextAnchor.y,
        movable = True,
) -> list[Text]:
    mainText = Text(
        x, y,
        text,
        color=QColor('white'),
        withBackground=True,
        padding=MARGIN,
        movable=movable,
        UI=UI,
    )
    buttonsElements: list[Text] = []
    def onTextMoving():
        xCoord = mainText.x
        yCoord = mainText.y + mainText.h + MARGIN
        startXCoord = xCoord
        for buttonElement in buttonsElements:
            buttonElement.x = xCoord
            buttonElement.y = yCoord
            xCoord += buttonElement.w + MARGIN
            if xCoord > UI.width() - buttonElement.w:
                yCoord += buttonElement.h + MARGIN
                xCoord = startXCoord
    mainText.onMoveCallback = onTextMoving
    if movable:
        mainText.LT.onMoveCallback = onTextMoving
    UI.addObject(mainText)

    xCoord = mainText.x
    yCoord = mainText.y + mainText.h + MARGIN
    startXCoord = xCoord
    for (buttonText, buttonCallback, buttonArgs) in buttons:
        buttonElement = Text(
            xCoord,
            yCoord,
            buttonText,
            color=QColor('white'),
            withBackground=True,
            padding=MARGIN,
            UI=UI,
            hoverable=True,
            clickable=True,
            onClickCallback=buttonCallback,
            onClickCallbackArgs=buttonArgs,
        )
        UI.addObject(buttonElement)
        buttonsElements.append(buttonElement)
        xCoord += buttonElement.w + MARGIN
        if xCoord > UI.width() - buttonElement.w:
            yCoord += buttonElement.h + MARGIN
            xCoord = startXCoord

    return [mainText, *buttonsElements]


def createNextBackButtonsAndText(
        UI: OverlayUI, text: str,
        nextCallback: Callable | None, nextCallbackArgs: list[any],
        backCallback: Callable | None, backCallbackArgs: list[any],
        overrideNextText: str = None, overrideBackText: str = None,
) -> tuple[Text, Text | None, Text | None]:
    buttonsConfig = []
    if backCallback is not None:
        buttonsConfig.append((
            overrideBackText or "<  Назад",
            backCallback,
            backCallbackArgs,
        ))
    if nextCallback is not None:
        buttonsConfig.append((
            overrideNextText or "Далее  >",
            nextCallback,
            nextCallbackArgs,
        ))
    elements = createButtonsAndText(UI, text, buttonsConfig)
    return elements[0], elements[1] if len(elements) > 1 else None, elements[2] if len(elements) > 2 else None


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
Открой интерфейс стола исследований, а потом передвинь две точки так, 
чтобы прямоугольник обозначал границу этого окна.""",
        confirmThaumWindowSlots, [UI, rectThaumWindow.LT.x, rectThaumWindow.LT.y,
                                  rectThaumWindow.RB.x, rectThaumWindow.RB.y],
        enroll, [UI],
    )


def confirmThaumWindowSlots(UI, LTx, LTy, RBx, RBy):
    thaumWindowWidth = RBx - LTx
    thaumWindowHeight = RBy - LTy
    logging.info(
        f"Thaum window configured at: ({int(LTx)}, {int(LTy)}) x ({int(RBx)}, {int(RBy)}), width={thaumWindowWidth}, height={thaumWindowHeight}")

    UI.clearAll()
    UI.createExitButton()

    def saveControls():
        saveThaumControlsConfig(pointWritingMaterials, pointPapers, rectAspectsListing.LT, rectAspectsListing.RB,
                                pointAspectsScrollLeft, pointAspectsScrollRight,
                                pointAspectsMixLeft, pointAspectsMixCreate, pointAspectsMixRight, rectInventory.LT,
                                rectInventory.RB, rectHexagonsCC,
                                (rectHexagonsCC.y - rectHexagonsTy) / (THAUM_HEXAGONS_SLOTS_COUNT // 2))
        beReadyForCreatingTI(UI)

    createNextBackButtonsAndText(
        UI,
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

(!!! После завершения этой конфигурации, если окно с игрой открыто не во весь экран, 
не передвигайте его по экрану !!)""",
        saveControls, [],
        configureThaumWindowCoords, [UI],
    )

    # Slots
    Ws = thaumWindowWidth / 15
    Hs = thaumWindowHeight / 10
    topSlotsY = LinkableValue(LTy + Hs * 0.85)
    pointWritingMaterials = UI.addObject(
        Point(LTx + Ws * 1, topSlotsY, movable=True, color=QColor('yellow')))  # writing materials
    pointPapers = UI.addObject(Point(LTx + Ws * 4.5, topSlotsY, movable=True, color=QColor('yellow')))  # scrolls

    rectAspectsLT = LinkableCoord(LTx + Ws * 0.25, LTy + Hs * 2.25)
    rectAspectsRB = LinkableCoord(LTx + Ws * 5.2, LTy + Hs * 7.25)
    UI.addObject(
        Line(rectAspectsLT.x, rectAspectsLT.y, rectAspectsRB.x, rectAspectsRB.y, dashed=True, color=QColor('brown')))
    UI.addObject(
        Line(rectAspectsRB.x, rectAspectsLT.y, rectAspectsLT.x, rectAspectsRB.y, dashed=True, color=QColor('brown')))
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

    UI.addObject(Point(rectAspectsLT.x, rectAspectsLT.y, movable=True, onMoveCallback=updateListingRectCoords))
    UI.addObject(Point(rectAspectsRB.x, rectAspectsRB.y, movable=True,
                       onMoveCallback=updateListingRectCoords))  # aspects listing rectangle

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
            deg30HexagonsLines[idx].S.y = rectHexagonsCC.y + sin(pi / 6) * rad - (i < 0) * i * slotSizeY / 2 - (
                        i > 0) * i * slotSizeY
            deg30HexagonsLines[idx].E.y = rectHexagonsCC.y - sin(pi / 6) * rad - (i > 0) * i * slotSizeY / 2 - (
                        i < 0) * i * slotSizeY

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


def chooseThaumVersion(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    def onSubmit():
        if selectedVersion[0] is None:
            logging.warning(f"Enter pressed in dialogue but thaum version is not selected")
            return
        logging.info(f"Selected thaum version:{selectedVersion[0]}")
        saveThaumVersionConfig(selectedVersion[0])
        beReadyForCreatingTI(UI)

    (infoText, _, backButton) = createNextBackButtonsAndText(
        UI,
        f"""Выберите версию Thaumcraft.
От этого будут зависеть рецепты получения аспектов.

Выбери версию:""",
        onSubmit, [],
        configureThaumWindowCoords, [UI],
    )
    recipesConfig = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
    versions = list(recipesConfig.keys())
    versionsObjects = []

    selectedVersionObject: list[Text | None] = [None]
    selectedVersion: list[str | None] = [None]

    oldVersion = loadThaumVersionConfig()
    logging.info(f"Selected in config version is: {oldVersion}")

    oldInfoTextCallback = infoText.onMoveCallback
    def updateVersionsPosition():
        oldInfoTextCallback()
        startCurY = backButton.y + backButton.h + MARGIN
        curY = startCurY
        curX = pointTextAnchor.x
        for i in range(len(versionsObjects)):
            versionObject = versionsObjects[i]
            if curY > UI.height() - versionObject.h:
                curX += 300
                curY = startCurY
            versionObject.y = curY
            versionObject.x = curX
            curY += versionObject.h + MARGIN

    infoText.LT.onMoveCallback = updateVersionsPosition
    infoText.onMoveCallback = updateVersionsPosition
    startCurY = backButton.y + backButton.h + MARGIN
    curY = startCurY
    curX = pointTextAnchor.x
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
            0, 0,
            version,
            color=QColor('white'),
            withBackground=True,
            padding=MARGIN,
            UI=UI,
            onClickCallback=onClickVersion,
            hoverable=True,
        ))
        if curY > UI.height() - versionObject.h:
            curX += 300
            curY = startCurY
        versionObject.x = curX
        versionObject.y = curY
        curY += versionObject.h + MARGIN
        versionObject.onClickCallbackArgs = [versionObject, version]
        versionsObjects.append(versionObject)
        if oldVersion == version:
            selectVersion(versionObject, version)

    logging.info(f"Selecting version dialogue showed. Versions: {versions}")


def beReadyForStartSolving(UI: OverlayUI, TI: ThaumInteractor):
    logging.info(f"Be ready for solving scenario started")
    UI.clearAll()
    UI.createExitButton()

    createNextBackButtonsAndText(
        UI,
        f"""Сейчас нейросеть будет определять аспекты, находящиеся на поле.
Выложи записку исследования в ячейку стола, а инвентарь заполни записками исследований,
начиная с самого верхнего левого слота. Они будут исследоваться по очереди""",
        runResearching, [UI, TI],
        chooseThaumVersion, [UI],
    )


def beReadyForCreatingTI(UI: OverlayUI):
    UI.clearAll()
    UI.createExitButton()

    def startCreatingTI():
        UI.clearAll()
        UI.createExitButton()
        createButtonsAndText(
            UI,
            f"""Жди и не двигай курсором мыши""",
            [],
            MARGIN, MARGIN,
            False,
        )
        UI.repaint()
        renderDelay()
        directlyCreateTI(UI)

    createNextBackButtonsAndText(
        UI,
        f"""Сейчас нейросеть определит имеющиеся аспекты в твоем столе.
Не двигай курсором мыши в процессе""",
        startCreatingTI, [],
        chooseThaumVersion, [UI],
    )

def directlyCreateTI(UI):
    logging.info(f"Create TI")
    TI = createTI(UI)
    if TI is None:
        logging.critical(f"Unknown error when creating ThaumcraftInteractor. It cannot be created")
        return
    logging.info(f"TI successfully created")
    UI.repaint()
    renderDelay()
    TI.updateAvailableAspectsInInventory(detectionAspectsDialogue, [UI, TI])

def detectionAspectsDialogue(UI, TI):
    TI.scrollToLeftSide()
    logging.info(f"TI successfully detected all aspects")

    UI.clearAll()
    exitButton = UI.createExitButton()
    (mainText, nextButton, backButton) = createNextBackButtonsAndText(
        UI,
        f"""Нейросеть определила аспекты в инвентаре и их количество.
Проверь правильность определения. В случае ошибки кликай на ячейку и исправляй.

Перелистывать страницы следует исключительно кнопками, нарисованными поверх игры""",
        runResearching, [UI, TI],
        chooseThaumVersion, [UI],
    )

    # --- Inventory aspects and counts dialogue elements
    cellColorFree = QColor('black')
    cellColorFree.setAlpha(50)
    # draw clickable cells
    cellsObjects = []

    def updateCurrentAspectData():
        logging.info(f"Current aspect data updated on screen. Aspect: {currentAspect[0]}")
        currentAspectMainText.setText(f'{currentAspect[0].name if currentAspect[0] else "не выбрано"}, {currentAspectCount[0] or "?"} шт.')
        if currentAspect[0]:
            currentAspectImage.setImage(currentAspect[0].pixMapImage)
        else:
            currentAspectImage.clearImage()

    def drawCurrentPageAspects():
        UI.removeObjects(cellsObjects)
        cellsObjects.clear()

        def onClickCell(aspect: Aspect, cellX: int, cellY: int):
            logging.info(f"Click on aspect to change: {aspect}, cellX: {cellX}, cellY {cellY}")
            currentAspectCellCoords[0] = cellX
            currentAspectCellCoords[1] = cellY
            currentAspectCount[0] = str(aspect.count if aspect else "")
            currentAspect[0] = aspect
            updateCurrentAspectData()
            switchToCellDialogue()

        # for i in range(len(TI.availableAspects)):
        for cellX in range(THAUM_ASPECTS_INVENTORY_SLOTS_X):
            for cellY in range(THAUM_ASPECTS_INVENTORY_SLOTS_Y):
                aspect = TI.getAspectByCellCoords(TI.currentAspectsPageIdx + cellX, cellY)
                cellRectCoords = list(TI.inventoryCellCoordsToPixelBoundingBox(cellX, cellY))
                cellWidth = cellRectCoords[2] - cellRectCoords[0]
                cellHeight = cellRectCoords[3] - cellRectCoords[1]
                cellRect = Rect(
                    *cellRectCoords,
                    color=cellColorFree,
                    fill=QColor(cellColorFree),
                    fillOpacity=0.1,
                    onClickCallback=onClickCell,
                    onClickCallbackArgs=[aspect, TI.currentAspectsPageIdx + cellX, cellY],
                    hoverable=True,
                    clickable=True,
                )
                imageSize = cellHeight / 3 * 2
                imageRect = Rect(
                    cellRectCoords[0], cellRectCoords[1],
                    cellRectCoords[2], cellRectCoords[1] + imageSize,
                    color=QColor('transparent'),
                    fill=QColor(cellColorFree),
                    fillOpacity=0.7,
                    hoverable=True,
                    clickable=True,
                )
                cellAspectImageObject = Image(
                    cellRectCoords[0] + imageSize / 2,
                    cellRectCoords[1] - imageSize / 2,
                    imageSize,
                    imageSize,
                    None,
                )
                cellsObjects.append(cellRect)
                cellsObjects.append(imageRect)
                cellsObjects.append(cellAspectImageObject)
                UI.addObject(cellRect)
                UI.addObject(imageRect)
                UI.addObject(cellAspectImageObject)

                if aspect:
                    cellAspectImageObject.setImage(aspect.pixMapImage)
                    cellAspectImageCountText = Text(
                        cellRectCoords[0] + cellWidth * 0.4,
                        cellRectCoords[1] + cellHeight * 0.2,
                        str(aspect.count),
                        color=QColor('#ff4444'),
                        withBackground=True,
                        padding=0,
                    )
                    cellsObjects.append(cellAspectImageCountText)
                    UI.addObject(cellAspectImageCountText)

        logging.info(f"Inventory page with aspects successfully drawn. Current page idx {TI.currentAspectsPageIdx}")
    drawCurrentPageAspects()

    LPoint = TI.pointAspectsScrollLeft
    RPoint = TI.pointAspectsScrollRight
    # buttonsLRWidth = (RPoint.x - LPoint.x)
    # buttonsLRHeight = buttonsLRWidth * 0.3
    def onClickScrollButton(isLeft=False):
        logging.info(f"Inventory aspects page scrolling to {'LEFT' if isLeft else 'RIGHT'}")
        UI.setAllObjectsVisibility(False)
        exitButton.setVisibility(True)
        UI.repaint()
        eventsDelay()
        if isLeft:
            TI.scrollLeft()
        else:
            TI.scrollRight()
        switchToMainDialogue()
        logging.info(f"New current aspects inventory page idx: {TI.currentAspectsPageIdx}")
    buttonScrollL = Text(
        LPoint.x, LPoint.y,
        '<=',
        color=QColor('white'),
        withBackground=True,
        padding=(MARGIN * 0.1, MARGIN, MARGIN * 0.1, MARGIN),
        align=Align.center,
        UI=UI,
        hoverable=True,
        clickable=True,
        onClickCallback=onClickScrollButton,
        onClickCallbackArgs=[True],
    )
    buttonScrollR = Text(
        RPoint.x, RPoint.y,
        '=>',
        color=QColor('white'),
        withBackground=True,
        padding=(MARGIN * 0.1, MARGIN, MARGIN * 0.1, MARGIN),
        align=Align.center,
        UI=UI,
        hoverable=True,
        clickable=True,
        onClickCallback=onClickScrollButton,
        onClickCallbackArgs=[False],
    )
    buttonScrollL.setVisibility(False)
    UI.addObject(buttonScrollL)
    UI.addObject(buttonScrollR)

    mainDialogueObjects = [mainText, nextButton, backButton, buttonScrollL, buttonScrollR]

    # --- Cell dialogue elements
    currentAspectCellCoords: list[int | None] = [None, None]
    currentAspectCount = [""]
    currentAspect: list[Aspect | None] = [None]
    cellDialogueObjects: list[UIPrimitive] = []

    def cancelAspectChanges():
        logging.info(f"Aspect changing canceled")
        switchToMainDialogue()
    def confirmAspectChanges():
        logging.info(f"Aspect changing confirmed")
        prevAspect = TI.getAspectByCellCoords(*currentAspectCellCoords)
        newAspect = currentAspect[0]
        newAspect.count = int(currentAspectCount[0] or 0)
        logging.info(f"Previous aspect: {prevAspect}, change to: {newAspect}")
        TI.setAspectIntoAvailables(
            newAspect,
            currentAspectCellCoords[0], currentAspectCellCoords[1]
        )
        logging.info(f"All new available aspects: {TI.availableAspects}")
        switchToMainDialogue()
    def confirmAspectIsNone():
        logging.info(f"Aspect is none changing confirmed")
        prevAspect = TI.getAspectByCellCoords(*currentAspectCellCoords)
        logging.info(f"Previous aspect: {prevAspect}, change to None")
        if prevAspect is not None:
            TI.availableAspects.remove(prevAspect)
        logging.info(f"All new available aspects: {TI.availableAspects}")
        switchToMainDialogue()

    [cellMainText, cellBackButton, cellNextButton, cellIsNoneButton] = createButtonsAndText(
        UI,
        f"""Чтобы изменить аспект в ячейке, выбери его из списка ниже
Чтобы изменить его количество, испоьзуй клавиши цифр [0-9] и [Backspace]""",
        [
            ("Отмена ", cancelAspectChanges, []),
            ("Подтвердить ", confirmAspectChanges, []),
            ("Ячейка пуста или неизвестный аспект ", confirmAspectIsNone, []),
        ]
    )

    textYCoord = cellBackButton.y + cellBackButton.h + MARGIN
    textXCoord = MARGIN
    currentAspectInfoText = Text(
        textXCoord, textYCoord,
        'Данные аспекта:',
        color=QColor('white'),
        withBackground=True,
        backgroundOpacity=0.8,
        padding=(MARGIN, MARGIN, 0, MARGIN),
        UI=UI,
    )
    UI.addObject(currentAspectInfoText)
    textYCoord += currentAspectInfoText.h
    currentAspectMainText = Text(
        textXCoord, textYCoord,
        f'{currentAspect[0].name if currentAspect[0] else "не выбрано"}, {currentAspectCount[0] or "?"} шт.',
        color=QColor('white'),
        withBackground=True,
        backgroundOpacity=0.8,
        padding=(MARGIN, MARGIN, MARGIN, MARGIN * 4),
        UI=UI,
    )
    UI.addObject(currentAspectMainText)
    currentAspectImage = Image(
        textXCoord + MARGIN * 2, textYCoord - MARGIN * 0.9,
        MARGIN * 2, MARGIN * 2,
        None
    )
    UI.addObject(currentAspectImage)
    if currentAspect[0]:
        currentAspectImage.setImage(currentAspect[0].pixMapImage)

    def onSelectAspect(aspect: Aspect):
        logging.info(f"Selected new aspect to selected cell {aspect}")
        currentAspect[0] = aspect
        updateCurrentAspectData()

    textYCoord += currentAspectMainText.h + MARGIN
    startTextYCoord = textYCoord
    cellsDialogueAspectsTexts = []
    cellsDialogueAspectsImages = []
    for i in range(len(TI.allAspects)):
        aspect = TI.allAspects[i]
        textAspect = UI.addObject(Text(
            textXCoord, textYCoord,
            aspect.name,
            color=QColor('white'),
            withBackground=True,
            backgroundOpacity=0.8,
            padding=(MARGIN, MARGIN, MARGIN, MARGIN * 4),
            UI=UI,
            onClickCallback=onSelectAspect,
            onClickCallbackArgs=[aspect],
            hoverable=True,
        ))
        aspectImage = UI.addObject(Image(
            textXCoord + MARGIN * 2, textYCoord,
            MARGIN * 2, MARGIN * 2,
            None,
        ))
        aspectImage.setImage(aspect.pixMapImage)
        cellDialogueObjects.append(textAspect)
        cellDialogueObjects.append(aspectImage)
        cellsDialogueAspectsTexts.append(textAspect)
        cellsDialogueAspectsImages.append(aspectImage)
        textYCoord += textAspect.h
        if textYCoord > UI.height() - textAspect.h:
            textYCoord = startTextYCoord
            textXCoord += 250

    oldCellMainTextCallback = cellMainText.onMoveCallback
    def onCellDialogueMainTextMoving():
        oldCellMainTextCallback()

        textYCoord = cellBackButton.y + cellBackButton.h + MARGIN
        textXCoord = int(cellBackButton.x)
        currentAspectInfoText.x = textXCoord
        currentAspectInfoText.y = textYCoord

        textYCoord += currentAspectInfoText.h
        currentAspectMainText.x = textXCoord
        currentAspectMainText.y = textYCoord
        currentAspectImage.setX(textXCoord + MARGIN)
        currentAspectImage.setY(textYCoord + MARGIN * 0.1)

        textYCoord += currentAspectMainText.h + MARGIN
        startTextYCoord = textYCoord
        for i in range(len(cellsDialogueAspectsTexts)):
            cellsDialogueAspectText = cellsDialogueAspectsTexts[i]
            cellsDialogueAspectText.x = textXCoord
            cellsDialogueAspectText.y = textYCoord
            cellsDialogueAspectImage = cellsDialogueAspectsImages[i]
            cellsDialogueAspectImage.setX(textXCoord + MARGIN)
            cellsDialogueAspectImage.setY(textYCoord + MARGIN)
            textYCoord += cellsDialogueAspectText.h
            if textYCoord > UI.height() - cellsDialogueAspectText.h:
                textYCoord = startTextYCoord
                textXCoord += 250
    cellMainText.onMoveCallback = onCellDialogueMainTextMoving
    cellMainText.LT.onMoveCallback = onCellDialogueMainTextMoving
    cellDialogueObjects += [cellMainText, cellNextButton, cellBackButton, cellIsNoneButton, currentAspectInfoText, currentAspectMainText, currentAspectImage]
    UI.setObjectsVisibility(cellDialogueObjects, False)

    # --- Switch states functions
    def switchToMainDialogue():
        logging.info(f"Switching to a main change inventory apsects dialogue...")
        UI.setObjectsVisibility(cellDialogueObjects, False)
        UI.setObjectsVisibility(mainDialogueObjects, True)
        buttonScrollL.setVisibility(True)
        buttonScrollR.setVisibility(True)
        if TI.currentAspectsPageIdx <= 0:
            buttonScrollL.setVisibility(False)
        if TI.currentAspectsPageIdx >= TI.maxAspectsPagesCount - 1:
            buttonScrollR.setVisibility(False)
        drawCurrentPageAspects()
    def switchToCellDialogue():
        logging.info(f"Switching to a directly change aspect dialogue...")
        UI.removeObjects(cellsObjects)
        UI.setObjectsVisibility(mainDialogueObjects, False)
        UI.setObjectsVisibility(cellDialogueObjects, True)
        UI.clearKeyCallbacks()

        def onInputNumber(number: int):
            currentAspectCount[0] += str(number)
            logging.debug(f"Pressed key: {number}. New value of aspect count: {currentAspectCount[0]}")
            updateCurrentAspectData()
        def onBackspace():
            if len(currentAspectCount[0]) > 0:
                currentAspectCount[0] = currentAspectCount[0][:-1]
                logging.debug(f"Pressed key Backspace. New value of aspect count: {currentAspectCount[0]}")
                updateCurrentAspectData()
        UI.setKeyCallback([KeyboardKeys.num0], onInputNumber, 0)
        UI.setKeyCallback([KeyboardKeys.num1], onInputNumber, 1)
        UI.setKeyCallback([KeyboardKeys.num2], onInputNumber, 2)
        UI.setKeyCallback([KeyboardKeys.num3], onInputNumber, 3)
        UI.setKeyCallback([KeyboardKeys.num4], onInputNumber, 4)
        UI.setKeyCallback([KeyboardKeys.num5], onInputNumber, 5)
        UI.setKeyCallback([KeyboardKeys.num6], onInputNumber, 6)
        UI.setKeyCallback([KeyboardKeys.num7], onInputNumber, 7)
        UI.setKeyCallback([KeyboardKeys.num8], onInputNumber, 8)
        UI.setKeyCallback([KeyboardKeys.num9], onInputNumber, 9)
        UI.setKeyCallback([KeyboardKeys.backspace], onBackspace)
        UI.setKeyCallback([KeyboardKeys.esc], cancelAspectChanges)
        UI.setKeyCallback([KeyboardKeys.enter], confirmAspectChanges)
    logging.info(f"UI to change detected aspects in inventory shown")

def runResearching(UI: OverlayUI, TI: ThaumInteractor):
    logging.info(f"Run researching scenario started")
    UI.clearAll()
    exitButtonObject = UI.createExitButton()

    class Cell:
        x: int = None
        y: int = None
        object: Circle = None
        imageObject: Image = None
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
    multyResearchesCountLeft = [0]

    cellsObjects = []

    # --- Cells dialogue elements
    cellSettingsStateDialogueObjects = []

    def updateDetectingField():
        logging.debug(f'Run detecting aspects on field')
        UI.setAllObjectsVisibility(False)
        exitButtonObject.setVisibility(True)
        UI.repaint()
        renderDelay()
        (existingAspects[0], noneHexagons[0], freeHexagons[0]) = TI.getExistingAspectsOnField()
        logging.debug(f'Aspects on field detected')

    def updateSolving(interruptingFlag: list[bool] = [False]):
        logging.debug(f'Starts updating solve...')
        # Start solving
        availableAspects = TI.getAvailableAspectsNames()
        currentLinkMap[0] = generateLinkMap(existingAspects[0], noneHexagons[0], availableAspects, interruptingFlag)
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
        for iy in range(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + (abs(ix) + 1) // 2 + 1,
                        THAUM_HEXAGONS_SLOTS_COUNT // 2 - (abs(ix)) // 2 + 1):
            hexagonCenterX = TI.rectHexagonsCC.x + ix * TI.hexagonSlotSizeX
            hexagonCenterY = TI.rectHexagonsCC.y + iy * TI.hexagonSlotSizeY - (ix % 2) * TI.hexagonSlotSizeY / 2
            cell = Cell(ix, iy)
            cellObject = Circle(
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
            cellAspectImageObject = Image(
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
    textCellIsNone = UI.addObject(Text(
        MARGIN, textYCoord,
        'Ячейка недоступна (N)',
        color=QColor('white'),
        withBackground=True,
        backgroundOpacity=0.8,
        padding=MARGIN,
        UI=UI,
        onClickCallback=onClickCellIsNone,
        hoverable=True,
    ))
    cellSettingsStateDialogueObjects.append(textCellIsNone)
    textYCoord += textCellIsNone.h + MARGIN
    textCellIsFree = UI.addObject(Text(
        MARGIN, textYCoord,
        'Ячейка свободна (F)',
        color=QColor('white'),
        withBackground=True,
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
    for i in range(len(TI.availableAspects)):
        aspect = TI.availableAspects[i]
        textAspect = UI.addObject(Text(
            textXCoord, textYCoord,
            aspect.name,
            color=QColor('white'),
            withBackground=True,
            backgroundOpacity=0.8,
            padding=(MARGIN, MARGIN, MARGIN, MARGIN * 4),
            UI=UI,
            onClickCallback=onClickCellIsAspect,
            onClickCallbackArgs=[aspect],
            hoverable=True,
        ))
        aspectImage = UI.addObject(Image(
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

    # --- Active state elements
    def insertAndPrepareNextIteration():
        logging.info("Inserting and preparing for next iteration")
        if multyResearchesCountLeft[0] > 0:
            TI.insertPaper()
        TI.moveMouseInSafePos()
        existingAspects[0].clear()
        freeHexagons[0].clear()
        noneHexagons[0].clear()
        currentLinkMap[0].clear()
        updateDetectingField()
        updateSolving()
        logging.info("Everything prepared to next detecting")
        if multyResearchesCountLeft[0] > 0:
            multyResearchesCountLeft[0] -= 1
            startPuttingLinkMap()
            return
        updateCellsImage()
        switchToActiveState()

    def startPuttingLinkMap():
        UI.setAllObjectsVisibility(False)
        onProcessText = UI.addObject(Text(
            MARGIN, MARGIN,
            f"""Подожди, решение выкладывается на поле... 
Не двигай мышью и не нажимай никакие кнопки.

Для экстренного закрытия программы нажми [Ctrl + Shift + Alt]""",
            color=QColor('white'),
            withBackground=True,
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
            insertAndPrepareNextIteration()
            UI.removeObject(onProcessText)

        puttingAspectsThread = threading.Thread(
            target=startPuttingAspects)  # run in thread to not blocking keys callbacks
        puttingAspectsThread.start()


    # base dialogue
    def onClickSwitchToMultyResearches():
        switchToMultyResearchesState()

    [activeStateText, activeStateNextButton, activeStateBackButton, backButton] = createButtonsAndText(
        UI,
        f"""Нейросеть определила аспекты на поле.
Чтобы перегенерировать полученную цепочку решения, нажми [R]
Если аспекты определены неверно, можно кликнуть на ячейку 
и выбрать, что в ней должно быть на самом деле. 

Чтобы приостановить программу, нажми [Ctrl + Shift + Пробел]""",
        [
            ("Назад в настройки", chooseThaumVersion, [UI]),
            ("Выложить решение ", startPuttingLinkMap, []),
            ("Безостановочный режим ", onClickSwitchToMultyResearches, []),
        ]
    )
    activeStateDialogueObjects = [activeStateText, activeStateNextButton, activeStateBackButton, backButton]


    # --- Multy researches state elements
    def onClickBack():
        switchToActiveState()

    def onClickNumber(researchesCount: int):
        multyResearchesCountLeft[0] = researchesCount
        TI.resetWorkingSlot()
        renderDelay()
        renderDelay()
        insertAndPrepareNextIteration()

    multyResearchesObjects = createButtonsAndText(
        UI,
        f"""Начать безостановочное исследование нескольких записок.
Записки должны быть разложены в инвентаре подряд, начиная с левого верхнего слота в инвентаре.
В столе исследований записки быть не должно""",
        [
            ("Назад", onClickBack, []),
            ("1", onClickNumber, [1]), ("2", onClickNumber, [2]), ("3", onClickNumber, [3]),
            ("4", onClickNumber, [4]), ("5", onClickNumber, [5]), ("6", onClickNumber, [6]),
            ("7", onClickNumber, [7]), ("8", onClickNumber, [8]), ("9", onClickNumber, [9]),
            ("10", onClickNumber, [10]), ("11", onClickNumber, [11]), ("12", onClickNumber, [12]),
            ("13", onClickNumber, [13]), ("14", onClickNumber, [14]), ("15", onClickNumber, [15]),
            ("16", onClickNumber, [16]), ("17", onClickNumber, [17]), ("18", onClickNumber, [18]),
            ("19", onClickNumber, [19]), ("20", onClickNumber, [20]), ("21", onClickNumber, [21]),
            ("22", onClickNumber, [22]), ("23", onClickNumber, [23]), ("24", onClickNumber, [24]),
            ("25", onClickNumber, [25]), ("26", onClickNumber, [26]), ("27", onClickNumber, [27]),
        ]
    )

    # --- Paused state elements
    onPausedText = UI.addObject(Text(
        MARGIN, MARGIN,
        f"""Программа проистановлена.

Чтобы продолжить работу, нажми [Ctrl + Shift + Пробел]""",
        color=QColor('white'),
        withBackground=True,
        padding=MARGIN,
        movable=True,
        UI=UI,
    ))
    pausedStateDialogueObjects = [onPausedText]

    # --- Switch between states functions
    isInUpdatingAspects = [False]
    curUpdatingUid = [0]
    def switchToActiveState():
        logging.info("Switching to active state")

        def onPressR():
            if isInUpdatingAspects[0]:
                return
            isInUpdatingAspects[0] = True
            UI.setAllObjectsVisibility(False)
            UI.repaint()
            renderDelay()

            curUpdatingUid[0] += 1
            interruptingFlag = [False]
            def interruptSolving(curUid):  # interrupt solving after LINK_GENERATION_MAX_TIME_MS
                if isInUpdatingAspects[0] and curUid == curUpdatingUid[0]:
                    interruptingFlag[0] = True
            UI.setTimeout(LINK_GENERATION_MAX_TIME_MS, interruptSolving, [curUpdatingUid[0]])

            updateDetectingField()
            updateSolving(interruptingFlag)
            switchToActiveState()
            isInUpdatingAspects[0] = False

        UI.clearKeyCallbacks()
        UI.setKeyCallback([KeyboardKeys.r], onPressR)
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

    def switchToMultyResearchesState():
        logging.info("Switching to multy researches state")
        UI.clearKeyCallbacks()
        UI.setKeyCallback([KeyboardKeys.esc], exitCellDialogue)
        UI.setAllObjectsVisibility(False)
        UI.setObjectsVisibility(multyResearchesObjects, True)
        exitButtonObject.setVisibility(True)

    updateDetectingField()
    updateSolving()
    switchToActiveState()
    logging.debug("Hexagon field with configuring initial aspects showed")
