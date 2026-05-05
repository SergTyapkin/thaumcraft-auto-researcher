import logging

from PyQt5.QtGui import QColor

from UI.OverlayUI import KeyboardKeys
from UI.primitives import UIPrimitive, Image, Rect
from UI.primitives.Text import Align, Text
from configs.translations import TEXTS
from controllers.Aspect import Aspect
from controllers import Scenarios
from controllers.Scenarios.shared import createNextBackButtonsAndText, createButtonsAndText
from configs.constants import MARGIN, THAUM_ASPECTS_INVENTORY_SLOTS_X, THAUM_ASPECTS_INVENTORY_SLOTS_Y
from utils import AppState
from utils.utils import renderDelay


def detectionAspectsDialogue(UI, TI):
    TI.scrollToLeftSide()
    logging.info(f"TI successfully detected all aspects")

    UI.clearAll()
    exitButton = UI.createExitButton()
    (mainText, nextButton, backButton) = createNextBackButtonsAndText(
        UI,
        AppState.translatedTexts[TEXTS.aspectsDetected],
        Scenarios.runResearching, [UI, TI],
        Scenarios.chooseThaumVersion, [UI],
    )

    # --- Inventory aspects and counts dialogue elements
    cellColorFree = QColor('black')
    cellColorFree.setAlpha(50)
    # draw clickable cells
    cellsObjects = []

    def updateCurrentAspectData():
        logging.info(f"Current aspect data updated on screen. Aspect: {currentAspect[0]}")
        currentAspectMainText.setText(f'{currentAspect[0].name if currentAspect[0] else AppState.translatedTexts[TEXTS.Buttons.notSelected]}, x{currentAspectCount[0] or "?"}.')
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
        renderDelay()
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
        if newAspect is None:
            logging.info("Aspect not chosen but trying to confirm")
            return
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
        AppState.translatedTexts[TEXTS.aspectChanging],
        [
            (AppState.translatedTexts[TEXTS.Buttons.cancel], cancelAspectChanges, []),
            (AppState.translatedTexts[TEXTS.Buttons.confirm], confirmAspectChanges, []),
            (AppState.translatedTexts[TEXTS.Buttons.cellIsEmpty], confirmAspectIsNone, []),
        ]
    )

    textYCoord = cellBackButton.y + cellBackButton.h + MARGIN
    textXCoord = MARGIN
    currentAspectInfoText = Text(
        textXCoord, textYCoord,
        AppState.translatedTexts[TEXTS.Buttons.aspectData],
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
