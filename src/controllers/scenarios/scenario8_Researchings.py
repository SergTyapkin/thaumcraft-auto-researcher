import logging
import math
import threading

from PyQt5.QtGui import QColor

from UI.OverlayUI import KeyboardKeys, OverlayUI
from UI.primitives import Image, Circle
from UI.primitives.Text import Text
from controllers.Aspect import Aspect
from controllers.ThaumInteractor import ThaumInteractor
from controllers.scenarios.scenario4_ChooseThaumVersion import chooseThaumVersion
from controllers.scenarios.shared import createButtonsAndText
from logic.LinksGeneration import generateLinkMap
from utils.constants import MARGIN, LINK_GENERATION_MAX_TIME_MS, MAX_SOLVE_RETRIES, THAUM_HEXAGONS_SLOTS_COUNT
from utils.utils import renderDelay, eventsDelay


def runResearching(UI: OverlayUI, TI: ThaumInteractor):
    logging.info(f"Run researching scenario started")
    UI.clearAll()
    exitButtonObject = UI.createExitButton()

    class Cell:
        x: int | None = None
        y: int | None = None
        object: Circle | None = None
        imageObject: Image | None = None
        aspect: Aspect | None = None
        isNone: bool = False

        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Cell([{self.x}, {self.y}], aspect={self.aspect}, isNone={self.isNone})"

    cells: list[Cell] = []
    selectedCell: list[Cell | None, QColor | None] = [None, None]  # list to make it mutable
    currentLinkMap: list[dict[tuple[int, int], str]] = [{}]  # list to make it mutable

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
        UI.safeSetAllVisibility(False)
        UI.safeSetObjectsVisibility([exitButtonObject], True)
        UI.safeRepaint()
        renderDelay()
        (existingAspects[0], noneHexagons[0], freeHexagons[0]) = TI.getExistingAspectsOnField()
        logging.debug(f'Aspects on field detected')

    def updateSolving(interruptingFlag: list[bool] = [False]):
        logging.debug(f'Starts updating solve...')

        # Start solving
        solving = None
        solveRetries = 0
        logging.debug(f'Trying to generate solving, try number: {solveRetries + 1}')
        while solveRetries < MAX_SOLVE_RETRIES and solving is None:
            solving = generateLinkMap(
                existingAspects[0],
                noneHexagons[0],
                TI.getAvailableAspectsNames(),
                interruptingFlag
            )
            solveRetries += 1

        if solving is None:
            currentLinkMap[0] = existingAspects[0]
            logging.debug(f'None solving gotten from "generateLinkMap"')
        else:
            currentLinkMap[0] = solving
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
            UI.safeSetAllVisibility(False)
            UI.safeRepaint()
            renderDelay()
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
        UI.safeSetAllObjectsVisibility(False)

        onProcessText = Text(
            MARGIN, MARGIN,
            f"""Подождите, решение выкладывается на поле... 
Не двигайте мышью и не нажимайте никакие кнопки!

Для экстренного закрытия программы нажмите [Ctrl + Shift + Alt]""",
            color=QColor('white'),
            withBackground=True,
            padding=MARGIN,
            UI=UI,  # Передаем UI для корректной инициализации объекта
        )
        UI.safeAddObject(onProcessText)
        UI.safeClearKeyCallbacks()
        UI.safeSetKeyCallback([KeyboardKeys.ctrl, KeyboardKeys.shift, KeyboardKeys.alt], UI.safeExit)

        finalLinkMap = currentLinkMap[0].copy()
        # Remove initial aspects from linkMap
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
            UI.safeRemoveObject(onProcessText)

        # Create thread for long operations
        puttingAspectsThread = threading.Thread(
            target=startPuttingAspects)  # run in thread to not blocking keys callbacks
        puttingAspectsThread.start()

    # vars for changing between render functions
    isInUpdatingAspects = [False]
    curUpdatingUid = [0]
    def regenerateLinkMap():
        if isInUpdatingAspects[0]:
            return
        isInUpdatingAspects[0] = True
        UI.safeSetAllObjectsVisibility(False)
        UI.safeRepaint()
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

    # base dialogue
    def onClickSwitchToMultyResearches():
        switchToMultyResearchesState()

    activeStateDialogueObjects = createButtonsAndText(
        UI,
        f"""Нейросеть определила аспекты на поле.
Если аспекты определены неверно, можно кликнуть на ячейку 
и выбрать, что в ней должно быть на самом деле. 

Чтобы приостановить программу, нажми [Ctrl + Shift + Пробел]""",
        [
            ("Назад в настройки", chooseThaumVersion, [UI]),
            ("Перегенерировать решение ", regenerateLinkMap, []),
            ("Выложить решение ", startPuttingLinkMap, []),
            ("Безостановочный режим ", onClickSwitchToMultyResearches, []),
        ]
    )

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

Чтобы продолжить работу, нажмите [Ctrl + Shift + Пробел]""",
        color=QColor('white'),
        withBackground=True,
        padding=MARGIN,
        movable=True,
        UI=UI,
    ))
    pausedStateDialogueObjects = [onPausedText]

    # --- Switch between states functions
    def switchToActiveState():
        logging.info("Switching to active state")
        UI.clearKeyCallbacks()
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
