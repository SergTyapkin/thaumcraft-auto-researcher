import logging
import math
import time
from typing import Any, Union

import keyboard
import mouse
import pyscreeze  # for screenshot
from PIL import Image
from PyQt5.QtGui import QColor, QPixmap

from logic.Neurolink import Neurolink
from src.UI import UIPrimitives
from src.controllers import Scenarios
from src.utils.constants import INVENTORY_SLOTS_X, INVENTORY_SLOTS_Y, THAUM_ASPECTS_INVENTORY_SLOTS_X, \
    THAUM_ASPECTS_INVENTORY_SLOTS_Y, ASPECTS_IMAGES_SIZE, \
    THAUM_CONTROLS_CONFIG_PATH, THAUM_ASPECT_RECIPES_CONFIG_PATH, THAUM_ASPECTS_ORDER_CONFIG_PATH, \
    EMPTY_ASPECT_SLOT_IMAGE_PATH, THAUM_HEXAGONS_SLOTS_COUNT, HEXAGON_MASK_IMAGE_PATH, FREE_HEXAGON_SLOT_IMAGES_PATHS, \
    NONE_HEXAGON_SLOT_IMAGE_PATH, MASK_ONLY_NUMBER_IMAGE_PATH, MASK_WITHOUT_NUMBER_IMAGE_PATH, EMPTY_TOLERANCE_PERCENT, \
    getImagePathByNumber, THAUM_VERSION_CONFIG_PATH, DEBUG, \
    HEXAGON_BORDER_MASK_IMAGE_PATH, MARGIN, UNKNOWN_ASPECT_IMAGE_PATH, ROBOFLOW_FREE_HEXAGON_PREDICTION_NAME, \
    ROBOFLOW_SCRIPT_IMAGE_PREDICTION_NAME, DELAY_BETWEEN_RENDER
from src.utils.constants import getAspectImagePath
from src.utils.utils import getImagesDiffPercent, readJSONConfig, eventsDelay, renderDelay, \
    loadRecipesForSelectedVersion


def createTI(UI):
    pointsConfig = readJSONConfig(THAUM_CONTROLS_CONFIG_PATH)
    if pointsConfig is None:
        Scenarios.enroll(UI)
        return None
    selected_thaum_version = readJSONConfig(THAUM_VERSION_CONFIG_PATH)
    if selected_thaum_version is None:
        Scenarios.chooseThaumVersion(UI)
        return None

    recipesConfig = loadRecipesForSelectedVersion()

    aspectsOrderConfig = readJSONConfig(THAUM_ASPECTS_ORDER_CONFIG_PATH)
    aspectsOrderConfig = aspectsOrderConfig['aspects']

    i = 0
    while i < len(aspectsOrderConfig):
        aspect = aspectsOrderConfig[i]
        if aspect not in recipesConfig:
            aspectsOrderConfig.remove(aspect)
        else:
            i += 1

    return ThaumInteractor(UI, pointsConfig, recipesConfig, aspectsOrderConfig)


class P:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def move(self):
        mousePos = mouse.get_position()
        if mousePos[0] != self.x or mousePos[1] != self.y:
            logging.debug(f"Move mouse to point {self}")
            mouse.move(self.x, self.y)
            eventsDelay()
        else:
            logging.debug(f"Move mouse to point {self} - mouse already in this pos")

    def click(self, button=mouse.LEFT, shift=False):
        self.move()
        if not shift:
            logging.debug(f"Click mouse on point {self}")
            mouse.click(button)
            return
        keyboard.press('shift')
        eventsDelay()
        logging.debug(f"Click on point {self} with shift")
        mouse.click(button)
        eventsDelay()
        keyboard.release('shift')

    def hold(self, button=mouse.LEFT):
        self.move()
        logging.debug(f"Hold mouse on point {self}")
        mouse.press(button)

    def release(self, button=mouse.LEFT):
        self.move()
        logging.debug(f"Release mouse on point {self}")
        mouse.release(button)


class Aspect:
    idx: int = None
    name: str = None
    image: Image.Image = None
    pixMapImage: QPixmap = None
    mask: Image.Image = None
    count: int = None

    def __init__(self, name: str, idx: int):
        self.name = name
        self.idx = idx

    def __repr__(self):
        return f"{self.name}({self.count})"


class ThaumInteractor:
    UI = None

    workingInventorySlot = -1  # can be 0..26 (inventory 9x3)
    currentAspectsPageIdx = None
    allAspects: list[Aspect] = []
    availableAspects: list[Aspect] = []
    recipes: dict[str, [str, str]]
    maxPagesCount: int = None
    numbersImages: list[Image.Image] = []

    pointWritingMaterials: P
    pointPapers: P
    pointSafePosition: P
    rectAspectsListingLT: P
    rectAspectsListingRB: P
    pointAspectsScrollLeft: P
    pointAspectsScrollRight: P
    pointAspectsMixLeft: P
    pointAspectsMixCreate: P
    pointAspectsMixRight: P
    rectInventoryLT: P
    rectInventoryRB: P
    rectHexagonsCC: P
    pointWorkingInventorySlot: P
    hexagonSlotSizeY: float
    hexagonSlotSizeX: float

    emptyAspectInventorySlotImage: Image.Image = None
    hexagonMaskImage: Image.Image = None
    hexagonBorderMaskImage: Image.Image = None
    freeHexagonImage: Image.Image = None
    noneHexagonImage: Image.Image = None
    maskOnlyNumbers: Image.Image = None
    maskWithoutNumbers: Image.Image = None

    def __init__(self, UI, controlsConfig: dict[str, dict[str, float]], aspectsRecipes: dict[str, list[str]], orderedAvailableAspects: list[str]):
        self.UI = UI

        c = controlsConfig
        self.pointWritingMaterials = P(c['pointWritingMaterials']['x'], c['pointWritingMaterials']['y'])
        self.pointPapers = P(c['pointPapers']['x'], c['pointPapers']['y'])
        self.pointSafePosition = P((self.pointPapers.x + self.pointWritingMaterials.x) / 2, self.pointPapers.y)
        self.rectAspectsListingLT = P(c['rectAspectsListingLT']['x'], c['rectAspectsListingLT']['y'])
        self.rectAspectsListingRB = P(c['rectAspectsListingRB']['x'], c['rectAspectsListingRB']['y'])
        self.pointAspectsScrollLeft = P(c['pointAspectsScrollLeft']['x'], c['pointAspectsScrollLeft']['y'])
        self.pointAspectsScrollRight = P(c['pointAspectsScrollRight']['x'], c['pointAspectsScrollRight']['y'])
        self.pointAspectsMixLeft = P(c['pointAspectsMixLeft']['x'], c['pointAspectsMixLeft']['y'])
        self.pointAspectsMixCreate = P(c['pointAspectsMixCreate']['x'], c['pointAspectsMixCreate']['y'])
        self.pointAspectsMixRight = P(c['pointAspectsMixRight']['x'], c['pointAspectsMixRight']['y'])
        self.rectInventoryLT = P(c['rectInventoryLT']['x'], c['rectInventoryLT']['y'])
        self.rectInventoryRB = P(c['rectInventoryRB']['x'], c['rectInventoryRB']['y'])
        self.rectHexagonsCC = P(c['rectHexagonsCC']['x'], c['rectHexagonsCC']['y'])
        self.hexagonSlotSizeY = c['hexagonSlotSizeY']
        self.hexagonSlotSizeX = self.hexagonSlotSizeY * math.cos(math.pi / 6)
        self.increaseWorkingSlot()

        self.emptyAspectInventorySlotImage = self.loadImage(EMPTY_ASPECT_SLOT_IMAGE_PATH)
        self.maskWithoutNumbers = self.loadImage(MASK_WITHOUT_NUMBER_IMAGE_PATH)
        self.maskOnlyNumbers = self.loadImage(MASK_ONLY_NUMBER_IMAGE_PATH)
        self.hexagonMaskImage = self.loadImage(HEXAGON_MASK_IMAGE_PATH)
        self.hexagonBorderMaskImage = self.loadImage(HEXAGON_BORDER_MASK_IMAGE_PATH)
        self.freeHexagonImages = [self.loadImage(path) for path in FREE_HEXAGON_SLOT_IMAGES_PATHS]
        self.noneHexagonImage = self.loadImage(NONE_HEXAGON_SLOT_IMAGE_PATH)
        for i in range(0, 10):
            self.numbersImages.append(self.loadImage(getImagePathByNumber(i), noResize=True))

        # TODO: make with available aspects detecting
        self.maxPagesCount = max(((len(orderedAvailableAspects) - 1) // THAUM_ASPECTS_INVENTORY_SLOTS_Y) - 4, 0)
        self.recipes = aspectsRecipes

        self.allAspects = []
        for i in range(len(orderedAvailableAspects)):
            self.allAspects.append(Aspect(orderedAvailableAspects[i], i))
        self.loadAspectsImages()
        logging.info(f"ThaumcraftInteractor successfully initialized")

    def loadImage(self, path: str, backgroundImage: Image.Image = None, noResize: bool = False) -> Image.Image:
        image = Image.open(path)
        if not noResize:
            image = self.imageResize(image)
        image = image.convert("RGBA")
        backgroundImage = backgroundImage or Image.new("RGBA", image.size, "BLACK")  # Create a white rgba background
        newImage = backgroundImage.convert("RGBA")
        newImage.paste(image, mask=image)  # Paste the image on the background. Go to the links given below for details.
        result = newImage.convert('RGB')
        logging.debug(f"Loaded image {path}")
        return result

    def loadAspectsImages(self):
        logging.info(f"Loading thaum aspects images...")
        for aspect in self.allAspects:
            imagePath = getAspectImagePath(aspect.name)
            try:
                aspect.image = self.loadImage(imagePath, self.emptyAspectInventorySlotImage)
                aspect.pixMapImage = QPixmap(imagePath)
            except Exception as e:
                logging.critical(f"Couldn't load image from path {imagePath}. Error: {e}")
                aspect.image = self.loadImage(UNKNOWN_ASPECT_IMAGE_PATH, self.emptyAspectInventorySlotImage)
                aspect.pixMapImage = QPixmap(UNKNOWN_ASPECT_IMAGE_PATH)
            imagePath = getAspectImagePath(aspect.name, colored=False)
            try:
                aspect.mask = Image.open(imagePath).convert("L")
            except Exception as e:
                logging.critical(f"Couldn't load image from path {imagePath} Error: {e}")
                aspect.mask = Image.open(UNKNOWN_ASPECT_IMAGE_PATH).convert("L")

    def scrollLeft(self):
        if self.currentAspectsPageIdx <= 0:
            return
        logging.info(f"Thaum inventory scrolling left")
        self.pointAspectsScrollLeft.click()
        self._showDebugClick(self.pointAspectsScrollLeft)
        self.currentAspectsPageIdx -= 1

    def scrollRight(self):
        if self.currentAspectsPageIdx == self.maxPagesCount:
            return
        logging.info(f"Thaum inventory scrolling right")
        self.pointAspectsScrollRight.click()
        self._showDebugClick(self.pointAspectsScrollRight)
        self.currentAspectsPageIdx += 1

    def scrollToLeftSide(self):
        logging.info(f"Thaum inventory scrolling to left side border...")
        if self.currentAspectsPageIdx is None:
            if self.maxPagesCount is not None:
                self.currentAspectsPageIdx = self.maxPagesCount
            else:
                self.currentAspectsPageIdx = THAUM_ASPECTS_INVENTORY_SLOTS_Y + 10
        for _ in range(self.currentAspectsPageIdx):
            self.scrollLeft()
            eventsDelay()
        self.currentAspectsPageIdx = 0

    def scrollToRightSide(self):
        logging.info(f"Thaum inventory scrolling to right side border...")
        if self.currentAspectsPageIdx is None:
            self.currentAspectsPageIdx = 0
        for _ in range(self.maxPagesCount - self.currentAspectsPageIdx):
            self.scrollRight()
            eventsDelay()
        self.currentAspectsPageIdx = self.maxPagesCount

    def _showDebugClick(self, point, color=QColor('lightgreen')):
        if not DEBUG:
            return
        eventsDelay()
        clickCircle = UIPrimitives.Circle(point.x, point.y, 20, color=color)

        timeToLeave = DELAY_BETWEEN_RENDER / 2 * 1000  # ms
        circleRadius = 20
        def onTimeCallback(timeLeft):
            clickCircle.r = timeLeft / timeToLeave * circleRadius

        self.UI.addObjectAndDeleteAfterTime(clickCircle, timeToLeave, onTimeCallback)

    def moveMouseInSafePos(self):
        self.pointSafePosition.move()

    def takeOutPaper(self):
        logging.info(f"Take out paper from thaum inventory")
        self.pointPapers.click()
        self._showDebugClick(self.pointPapers)
        eventsDelay()
        self.pointWorkingInventorySlot.click()
        self._showDebugClick(self.pointWorkingInventorySlot)

    def insertPaper(self):
        logging.info(f"Insert paper into thaum inventory")
        self.pointWorkingInventorySlot.click()
        self._showDebugClick(self.pointWorkingInventorySlot)
        eventsDelay()
        self.pointPapers.click()
        self._showDebugClick(self.pointPapers)

    def increaseWorkingSlot(self):
        self.workingInventorySlot += 1

        areaWidth = self.rectInventoryRB.x - self.rectInventoryLT.x
        areaHeight = self.rectInventoryRB.y - self.rectInventoryLT.y
        slotWidth = areaWidth / INVENTORY_SLOTS_X
        slotHeight = areaHeight / INVENTORY_SLOTS_Y

        self.pointWorkingInventorySlot = P(
            self.rectInventoryLT.x + (slotWidth * 0.5) + slotWidth * (self.workingInventorySlot % INVENTORY_SLOTS_X),
            self.rectInventoryLT.y + (slotHeight * 0.5) + slotHeight * (self.workingInventorySlot // INVENTORY_SLOTS_X)
        )
        logging.info(f"Current working slot increased to {self.workingInventorySlot}. New slot coordinates: {self.pointWorkingInventorySlot}")

    def takeAspectByCellCoords(self, cellX, cellY):
        areaWidth = self.rectAspectsListingRB.x - self.rectAspectsListingLT.x
        areaHeight = self.rectAspectsListingRB.y - self.rectAspectsListingLT.y
        slotWidth = areaWidth / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = areaHeight / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        aspectPoint = P(
            self.rectAspectsListingLT.x + slotWidth * (cellX + 0.5),
            self.rectAspectsListingLT.y + slotHeight * (cellY + 0.5)
        )
        logging.info(f"Take aspect from cell ({cellX, cellY}), coordinates: {aspectPoint}")
        aspectPoint.hold()
        self._showDebugClick(aspectPoint, QColor('blue'))

    def putAspect(self, cellX, cellY):
        aspectPoint = P(
            self.rectHexagonsCC.x + self.hexagonSlotSizeX * cellX,
            self.rectHexagonsCC.y + self.hexagonSlotSizeY * cellY - (cellX % 2) * (self.hexagonSlotSizeY / 2)
        )
        logging.info(f"Put aspect to hexagon cell ({cellX, cellY}), coordinates: {aspectPoint}")
        aspectPoint.release()
        self._showDebugClick(aspectPoint, QColor('red'))

    def getAspectByName(self, aspectName: str):
        for aspect in self.allAspects:
            if aspect.name == aspectName:
                return aspect
        raise ValueError(f"Aspect {aspectName} not exists in known aspects list")

    def scrollToAspect(self, aspect: Aspect) -> (int, int):
        cellX = aspect.idx // THAUM_ASPECTS_INVENTORY_SLOTS_Y
        cellY = aspect.idx % THAUM_ASPECTS_INVENTORY_SLOTS_Y
        logging.info(f"Scroll to aspect {aspect}, in cell[absolute] ({cellX}, {cellY})")

        cellPageIdxMin = max(cellX - THAUM_ASPECTS_INVENTORY_SLOTS_X + 1, 0)
        cellPageIdxMax = min(cellX, self.maxPagesCount)

        if self.currentAspectsPageIdx < cellPageIdxMin:
            for _ in range(self.currentAspectsPageIdx, cellPageIdxMin):
                self.scrollRight()
                eventsDelay()
        elif self.currentAspectsPageIdx > cellPageIdxMax:
            for _ in range(cellPageIdxMax, self.currentAspectsPageIdx):
                self.scrollLeft()
                eventsDelay()

        return cellX - self.currentAspectsPageIdx, cellY

    def takeAspect(self, aspect: Aspect):
        logging.info(f"Take aspect {aspect}...")
        (cellX, cellY) = self.scrollToAspect(aspect)
        self.takeAspectByCellCoords(cellX, cellY)

    def mixAspect(self, aspect: Aspect, useShift=True):
        logging.info(f"Mixing aspect {aspect}...")
        recipe = self.recipes.get(aspect.name)
        if recipe is None:
            raise ValueError(f"Aspect {aspect.name} not exists in known aspects recipes")
        if len(recipe[1]) < 2:
            raise ValueError(f"Aspect {aspect.name} is a basic and can't be created using mixing")

        if useShift:
            (cellX, cellY) = self.scrollToAspect(aspect)
            eventsDelay()
            P(cellX, cellY).click(shift=True)
            self._showDebugClick(P(cellX, cellY))
            return

        (cellX, cellY) = self.scrollToAspect(recipe[0])
        eventsDelay()
        P(cellX, cellY).click()
        self._showDebugClick(P(cellX, cellY))
        eventsDelay()
        (cellX, cellY) = self.scrollToAspect(recipe[1])
        eventsDelay()
        P(cellX, cellY).click()
        self._showDebugClick(P(cellX, cellY))
        eventsDelay()
        self.pointAspectsMixCreate.click()
        self._showDebugClick(self.pointAspectsMixCreate)

    def fillByLinkMap(self, aspectsMap: dict[(int, int), str]):
        logging.info(f"Filling aspects by link map: {aspectsMap}")
        # Оптимизируем порядок аспектов, чтобы пришлось меньше листать инвентарь
        aspectsListMap = list(aspectsMap.items())
        def sortFunc(pair):
            aspectName = pair[1]
            aspect = self.getAspectByName(aspectName)
            return aspect.idx
        aspectsListMap.sort(key=sortFunc)
        logging.debug(f"Sorted aspects link map: {aspectsListMap}")
        # Заполняем по одному аспекту, пролистывая к каждому следующему
        self.currentAspectsPageIdx = None
        self.scrollToLeftSide()
        for coords, aspectName in aspectsListMap:
            aspect = self.getAspectByName(aspectName)
            self.takeAspect(aspect)
            eventsDelay()
            self.putAspect(*coords)
            eventsDelay()

    def imageResize(self, image: Image.Image) -> Image.Image:
        return image.resize((ASPECTS_IMAGES_SIZE, ASPECTS_IMAGES_SIZE), Image.Resampling.LANCZOS)

    def addDebugHighlightingRect(self, LTx=0, LTy=0, RTx=0, RTy=0):
        if not DEBUG:
            return None
        debugHighlightingRect = UIPrimitives.Rect(LTx, LTy,
                                                  RTx, RTy,
                                                  fill=QColor('blue'), fillOpacity=0.3, lineWidth=1,
                                                  color=QColor('blue'))
        self.UI.addObject(debugHighlightingRect)
        return debugHighlightingRect

    def takeScreenshot(self, LTx, LTy, RBx, RBy, debugHighlightingRect = None) -> Image.Image:
        if DEBUG and debugHighlightingRect is not None:
            debugHighlightingRect.setVisibility(False)
        screenshotImage = pyscreeze.screenshot(region=(
            int(LTx), int(LTy),
            int(RBx - LTx), int(RBy - LTy),
        ))
        logging.info(f"Taken screenshot on ({LTx}, {LTy})x({RBx}, {RBy})...")
        if DEBUG and debugHighlightingRect is not None:
            debugHighlightingRect.setCoords(
                LTx, LTy,
                RBx, RBy,
            )
            debugHighlightingRect.setVisibility(True)
            time.sleep(1)
        return screenshotImage

    def updateAvailableAspectsInInventory(self):
        logging.info("Detecting available aspects...")
        self.availableAspects = []

        debugHighlightingRect = self.addDebugHighlightingRect()
        slotWidth = (self.rectAspectsListingRB.x - self.rectAspectsListingLT.x) / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = (self.rectAspectsListingRB.y - self.rectAspectsListingLT.y) / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        self.scrollToLeftSide()
        isFoundEndOfInventory = False
        newAdditionalOffset = THAUM_ASPECTS_INVENTORY_SLOTS_X
        while newAdditionalOffset > 0:
            logging.info(f"Finding aspects on new page of inventory. Current page: {self.currentAspectsPageIdx}")
            # Calculate screenshot area
            screenshotRBX = self.rectAspectsListingRB.x
            screenshotRBY = self.rectAspectsListingRB.y
            screenshotLTX = self.rectAspectsListingRB.x - slotWidth * newAdditionalOffset
            screenshotLTY = self.rectAspectsListingLT.y
            screenshotImage = self.takeScreenshot(
                screenshotLTX, screenshotLTY,
                screenshotRBX, screenshotRBY,
                debugHighlightingRect
            )

            # FIXME: Neurolink can't detect aspects on dark background
            # Find aspects on screenshot
            logging.info("Wait for prediction")
            predictions = Neurolink.predict(screenshotImage)
            logging.info(f"Predictions: {predictions}")
            self.UI.exit()

            # Approximate aspects coordinates by cells
            aspectsOnScreenshot = []
            for prediction in predictions:
                try:
                    aspect = self.getAspectByName(prediction.predictionName)
                except ValueError:
                    continue
                coords = (
                    self.currentAspectsPageIdx + prediction.x // slotWidth,
                    prediction.y // slotHeight,
                )
                aspectsOnScreenshot.append([coords, aspect])
            def sortFunc(element):
                return element[0][0] * THAUM_ASPECTS_INVENTORY_SLOTS_Y + element[0][1]
            aspectsOnScreenshot.sort(key=sortFunc)
            logging.info(f"Sorted detected aspects: {aspectsOnScreenshot}")

            # add found aspects to available aspects
            self.availableAspects.extend(map(lambda elem: elem[1], aspectsOnScreenshot))
            logging.debug(f"All available aspects: {self.availableAspects}")

            if isFoundEndOfInventory:
                break

            # Check if we really move right or it's end of inventory
            logging.info(f"Checking if we really can move right or it's end of inventory...")
            newAdditionalOffset = 0
            previousScreenshotImage = self.takeScreenshot(
                self.rectAspectsListingRB.x - slotWidth, self.rectAspectsListingLT.y,
                self.rectAspectsListingRB.x, self.rectAspectsListingLT.y + slotHeight,
                debugHighlightingRect
            )
            while newAdditionalOffset < THAUM_ASPECTS_INVENTORY_SLOTS_X:
                self.scrollRight()
                renderDelay()
                newScreenshotImage = self.takeScreenshot(
                    self.rectAspectsListingRB.x - slotWidth, self.rectAspectsListingLT.y,
                    self.rectAspectsListingRB.x, self.rectAspectsListingLT.y + slotHeight,
                    debugHighlightingRect
                )
                # check if we really scrolled right
                diffWithEmpty = getImagesDiffPercent(previousScreenshotImage, newScreenshotImage)
                logging.debug(f"Difference of two images before and after scrolling right: {diffWithEmpty}")
                if diffWithEmpty < EMPTY_TOLERANCE_PERCENT: # nothing changed - it's the end of inventory
                    logging.info(f"Found end of inventory. Detection ends")
                    self.currentAspectsPageIdx -= 1
                    self.maxPagesCount = self.currentAspectsPageIdx
                    isFoundEndOfInventory = True
                    logging.info(f"Total inventory pages: {self.currentAspectsPageIdx}")
                    break
                newAdditionalOffset += 1
                previousScreenshotImage = newScreenshotImage
            logging.info(f"New aspects page total width: {newAdditionalOffset}")

        self.UI.removeObject(debugHighlightingRect)


    def logAvailableAspects(self):
        string = ""
        for i in range(len(self.availableAspects)):
            string += str(self.availableAspects[i]) + " "
            if i % THAUM_ASPECTS_INVENTORY_SLOTS_Y == THAUM_ASPECTS_INVENTORY_SLOTS_Y - 1:
                logging.info(string)
                string = ""
        logging.info(string)

    def getExistingAspectsOnField(self) -> tuple[dict[(int, int), str], set[(int, int)], set[(int, int)]]:
        self.logAvailableAspects()

        hexagonsRectLT = P(
            self.rectHexagonsCC.x - (THAUM_HEXAGONS_SLOTS_COUNT / 2 + 0.5) * self.hexagonSlotSizeX,
            self.rectHexagonsCC.y - (THAUM_HEXAGONS_SLOTS_COUNT / 2 + 0.1) * self.hexagonSlotSizeY,
        )
        hexagonsRectRB = P(
            self.rectHexagonsCC.x + (THAUM_HEXAGONS_SLOTS_COUNT / 2 + 0.5) * self.hexagonSlotSizeX,
            self.rectHexagonsCC.y + (THAUM_HEXAGONS_SLOTS_COUNT / 2 + 0.1) * self.hexagonSlotSizeY,
        )

        # Do a screenshot
        debugHighlightingRect = self.addDebugHighlightingRect()
        allHexagonsImage = self.takeScreenshot(
            hexagonsRectLT.x, hexagonsRectLT.y,
            hexagonsRectRB.x, hexagonsRectRB.y,
            debugHighlightingRect
        )

        # Find aspects, hexagons and scripts on screenshot.
        logging.info("Wait for prediction")
        predictions = Neurolink.predict(allHexagonsImage)
        logging.info(f"Predictions: {predictions}")

        # Approximate cell coords
        class Cell:
            x: int
            y: int
            aspectName: str | None
            isAspect: bool = False
            isFreeHex: bool = False
            def __init__(self, x, y, aspectName, isAspect, isFreeHex):
                self.x = x
                self.y = y
                self.aspectName = aspectName
                self.isAspect = isAspect
                self.isFreeHex = isFreeHex

        xLeft = self.rectHexagonsCC.x - (THAUM_HEXAGONS_SLOTS_COUNT / 2) * self.hexagonSlotSizeX
        yTop = self.rectHexagonsCC.y - (THAUM_HEXAGONS_SLOTS_COUNT / 2) * self.hexagonSlotSizeY
        allCells = set()
        maxDistFromCenter = 0
        for prediction in predictions:
            if prediction.predictionName == ROBOFLOW_FREE_HEXAGON_PREDICTION_NAME:
                isAspect = False
            elif prediction.predictionName == ROBOFLOW_SCRIPT_IMAGE_PREDICTION_NAME:
                continue
            else:
                isAspect = True
                try:  # check if we know detected aspect
                    self.getAspectByName(prediction.predictionName)
                except ValueError:
                    continue
            xCenter = prediction.x + hexagonsRectLT.x
            yCenter = prediction.y + hexagonsRectLT.y
            xCell = int(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1 + (xCenter - xLeft) // self.hexagonSlotSizeX)
            yCell = int(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1 + (yCenter - yTop + ((self.hexagonSlotSizeY / 2) if xCell % 2 != 0 else 0)) // self.hexagonSlotSizeY)
            distFromCenter = abs(xCell) + abs(yCell) - abs(xCell) // 2
            maxDistFromCenter = max(maxDistFromCenter, distFromCenter)
            allCells.add(Cell(
                xCell, yCell,
                prediction.predictionName if isAspect else None,
                isAspect,
                not isAspect,
            ))

        # Split cells by holes set and aspects dict
        hexagonFieldRadius = min(maxDistFromCenter, THAUM_HEXAGONS_SLOTS_COUNT // 2)
        logging.debug(f"Hexagon field radius detected: {hexagonFieldRadius}")

        existingAspects = {}
        noneHexagons = set()
        freeHexagons = set()
        for x in range(-hexagonFieldRadius, hexagonFieldRadius + 1):
            for y in range(-hexagonFieldRadius + (abs(x) + 1) // 2, hexagonFieldRadius - (abs(x)) // 2 + 1):
                noneHexagons.add((x, y))
        for cell in allCells:
            if (cell.x, cell.y) not in noneHexagons: # coordinates out of range
                continue
            if cell.isAspect:
                existingAspects[(cell.x, cell.y)] = cell.aspectName
            elif cell.isFreeHex:
                noneHexagons.remove((cell.x, cell.y))
                freeHexagons.add((cell.x, cell.y))

        logging.debug(f"Found aspects: {existingAspects}")
        logging.debug(f"Found holes: {noneHexagons}")
        logging.debug(f"Free hexagons: {freeHexagons}")
        logging.debug(f"End of detecting hexagons field")

        self.UI.removeObject(debugHighlightingRect)
        return existingAspects, noneHexagons, freeHexagons
