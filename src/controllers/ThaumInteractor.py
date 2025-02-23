import logging
import math
import time
from threading import Thread
from typing import Callable

import pyscreeze  # for screenshot
from PIL import Image
from PyQt5.QtGui import QColor, QPixmap

from src.UI.primitives import Circle, Rect
from src.controllers import Scenarios
from src.controllers.Aspect import Aspect
from src.controllers.Point import P
from src.logic.Neurolink import Neurolink
from src.utils.constants import INVENTORY_SLOTS_X, INVENTORY_SLOTS_Y, THAUM_ASPECTS_INVENTORY_SLOTS_X, \
    THAUM_ASPECTS_INVENTORY_SLOTS_Y, ASPECTS_IMAGES_SIZE, \
    THAUM_CONTROLS_CONFIG_PATH, THAUM_ASPECTS_ORDER_CONFIG_PATH, \
    THAUM_HEXAGONS_SLOTS_COUNT, \
    IMAGES_TOLERANCE_PERCENT, \
    THAUM_VERSION_CONFIG_PATH, DEBUG, \
    UNKNOWN_ASPECT_IMAGE_PATH, NEUROLINK_FREE_HEXAGON_PREDICTION_NAME, \
    NEUROLINK_SCRIPT_IMAGE_PREDICTION_NAME, DELAY_BETWEEN_RENDER, DELAY_BETWEEN_EVENTS
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


class ThaumInteractor:
    UI = None

    workingInventorySlot = -1  # can be 0..26 (inventory 9x3)
    currentAspectsPageIdx = None  # Current aspects inventory page idx
    allAspects: list[Aspect] = []  # All aspects that for selected version and all known addons
    availableAspects: list[Aspect] = []  # Only available in inventory aspects
    recipes: dict[str, list[str, str]]  # All aspects recipes
    maxAspectsPagesCount: int = None  # Total aspects inventory pages count

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

    unknownAspectImage: Image.Image = None

    def __init__(self, UI, controlsConfig: dict[str, dict[str, float]], aspectsRecipes: dict[str, list[str, str]],
                 orderedAvailableAspects: list[str]):
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

        self.unknownAspectImage = self.loadImage(UNKNOWN_ASPECT_IMAGE_PATH)

        self.maxAspectsPagesCount = max(((len(orderedAvailableAspects) - 1) // THAUM_ASPECTS_INVENTORY_SLOTS_Y) - 4, 0)
        self.recipes = aspectsRecipes

        self.allAspects = [Aspect(orderedAvailableAspects[i], i) for i in range(len(orderedAvailableAspects))]
        self.loadAspectsImages()

        logging.info(f"ThaumcraftInteractor successfully initialized")
        logging.info(f"All known aspects:     {self.allAspects}")
        logging.info(f"All available aspects: {self.availableAspects}")

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
            if aspect.image:
                continue
            imagePath = getAspectImagePath(aspect.name)
            try:
                aspect.image = self.loadImage(imagePath, self.unknownAspectImage)
                aspect.pixMapImage = QPixmap(imagePath)
            except Exception as e:
                logging.critical(f"Couldn't load image from path {imagePath}. Error: {e}")
                aspect.image = self.unknownAspectImage
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
        if self.currentAspectsPageIdx >= self.maxAspectsPagesCount - 1:
            return
        logging.info(f"Thaum inventory scrolling right")
        self.pointAspectsScrollRight.click()
        self._showDebugClick(self.pointAspectsScrollRight)
        self.currentAspectsPageIdx += 1

    def scrollToLeftSide(self):
        logging.info(f"Thaum inventory scrolling to left side border...")
        if self.currentAspectsPageIdx is None:
            if self.maxAspectsPagesCount is not None:
                self.currentAspectsPageIdx = self.maxAspectsPagesCount
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
        for _ in range(self.maxAspectsPagesCount - self.currentAspectsPageIdx):
            self.scrollRight()
            eventsDelay()
        self.currentAspectsPageIdx = self.maxAspectsPagesCount

    def _showDebugClick(self, point, color=QColor('lightgreen')):
        if not DEBUG:
            return
        eventsDelay()
        clickCircle = Circle(point.x, point.y, 20, color=color)

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
        logging.info(
            f"Current working slot increased to {self.workingInventorySlot}. New slot coordinates: {self.pointWorkingInventorySlot}")

    def inventoryCellCoordsToPixelCoords(self, cellX: int, cellY: int) -> P:
        areaWidth = self.rectAspectsListingRB.x - self.rectAspectsListingLT.x
        areaHeight = self.rectAspectsListingRB.y - self.rectAspectsListingLT.y
        slotWidth = areaWidth / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = areaHeight / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        return P(
            self.rectAspectsListingLT.x + slotWidth * (cellX + 0.5),
            self.rectAspectsListingLT.y + slotHeight * (cellY + 0.5)
        )

    def inventoryCellCoordsToPixelBoundingBox(self, cellX: int, cellY: int) -> tuple[int, int, int, int]:
        areaWidth = self.rectAspectsListingRB.x - self.rectAspectsListingLT.x
        areaHeight = self.rectAspectsListingRB.y - self.rectAspectsListingLT.y
        slotWidth = areaWidth / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = areaHeight / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        x = self.rectAspectsListingLT.x + slotWidth * cellX
        y = self.rectAspectsListingLT.y + slotHeight * cellY
        return x, y, x + slotWidth, y + slotHeight

    def takeAspectByCellCoords(self, cellX, cellY):
        aspectPoint = self.inventoryCellCoordsToPixelCoords(cellX, cellY)
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

    def getAspectByName(self, aspectName: str) -> Aspect:
        for aspect in self.allAspects:
            if aspect.name == aspectName:
                return aspect
        raise ValueError(f"Aspect {aspectName} not exists in known aspects list")

    def getCellIdxByCellCoords(self, cellX: int, cellY: int) -> int:
        return cellX * THAUM_ASPECTS_INVENTORY_SLOTS_Y + cellY

    def getAspectByCellCoords(self, cellX: int, cellY: int) -> Aspect | None:
        for i in range(len(self.availableAspects)):
            aspect = self.availableAspects[i]
            if aspect.cellX == cellX and aspect.cellY == cellY:
                return aspect
        return None

    def setAspectIntoAvailables(self, aspect: Aspect, cellX: int, cellY: int):
        prevAspect = self.getAspectByCellCoords(cellX, cellY)
        aspect.cellX = cellX
        aspect.cellY = cellY
        logging.info(f"Adding new aspect to availables: {aspect}. Previous aspect in this cell: {prevAspect}")

        if prevAspect is not None:
            if prevAspect == aspect:
                logging.info(f"Aspects is equal. Nothing to change")
                return
            aspectIdx = self.getAvailableAspectIdx(prevAspect)
            prevAspect.count = None
            prevAspect.cellX = None
            prevAspect.cellY = None
            self.availableAspects[aspectIdx] = aspect
            logging.info(f"Aspect {prevAspect} successfully changed to {aspect} on idx {aspectIdx}")
        else:
            cellIdx = self.getCellIdxByCellCoords(cellX, cellY)
            cellsBeforeCount = 0
            for a in self.availableAspects:
                if self.getCellIdxByCellCoords(a.cellX, a.cellY) < cellIdx:
                    cellsBeforeCount += 1
            self.availableAspects.insert(cellsBeforeCount, aspect)
            logging.info(f"Aspect {aspect} successfully inserted on idx {cellsBeforeCount}")

        # log
        logStr = "All available aspects: "
        for a in self.availableAspects:
            logStr += f"{a}[{a.uid}] "
        logging.info(logStr)
        # remove aspect duplicate
        def removeAspectDuplicates():
            for a in self.availableAspects:
                if a.uid == aspect.uid and a.cellX != cellX and a.cellY != cellY:
                    self.availableAspects.remove(a)
                    removeAspectDuplicates()
                    break
        removeAspectDuplicates()


    def scrollToAspect(self, aspect: Aspect) -> (int, int):
        logging.info(f"Scroll to aspect {aspect}, in cell[absolute] ({aspect.cellX}, {aspect.cellY})")

        cellPageIdxMin = max(aspect.cellX - THAUM_ASPECTS_INVENTORY_SLOTS_X + 1, 0)
        cellPageIdxMax = min(aspect.cellX, self.maxAspectsPagesCount)

        if self.currentAspectsPageIdx < cellPageIdxMin:
            for _ in range(self.currentAspectsPageIdx, cellPageIdxMin):
                self.scrollRight()
                eventsDelay()
        elif self.currentAspectsPageIdx > cellPageIdxMax:
            for _ in range(cellPageIdxMax, self.currentAspectsPageIdx):
                self.scrollLeft()
                eventsDelay()

        return aspect.cellX - self.currentAspectsPageIdx, aspect.cellY

    def takeAspect(self, aspect: Aspect):
        if aspect.count == 0:
            self.mixAspect(aspect)
        logging.info(f"Take aspect {aspect}...")
        (cellX, cellY) = self.scrollToAspect(aspect)
        self.takeAspectByCellCoords(cellX, cellY)
        aspect.count -= 1

    def mixAspect(self, aspect: Aspect, useShift=True, times=1) -> None:
        """
        Creates aspect by mixing aspects from its recipe

        Args:
            aspect: Aspect that we need to create
            useShift: If True, then mixing is performed by Shift+LMB
            times: How many aspects do we need to craft
        """
        logging.info(f"Mixing aspect {aspect} {times} times...")
        recipe = self.recipes.get(aspect.name)
        if recipe is None:
            raise ValueError(f"Aspect {aspect.name} not exists in known aspects recipes")
        if len(recipe) < 2:  # Aspect is basic (Aqua, Terra, Aer, Ordo, Perditio)
            if aspect.count < times:
                raise ValueError(f"Ran out of basic aspect {aspect.name}")
            return
        aspect1 = self.getAspectByName(recipe[0])
        aspect2 = self.getAspectByName(recipe[1])
        # Creating aspects used in recipe so that they don't run out
        self.mixAspect(aspect1, useShift=useShift, times=times)
        self.mixAspect(aspect2, useShift=useShift, times=times)

        if useShift:
            (cellX, cellY) = self.scrollToAspect(aspect)
            aspect_point = self.inventoryCellCoordsToPixelCoords(cellX, cellY)
            eventsDelay()
            for _ in range(times):
                aspect_point.click(shift=True)
                self._showDebugClick(aspect_point)
                eventsDelay()
        else:
            (cellX, cellY) = self.scrollToAspect(aspect1)
            aspect1_point = self.inventoryCellCoordsToPixelCoords(cellX, cellY)
            eventsDelay()
            aspect1_point.click()
            self._showDebugClick(aspect1_point)
            eventsDelay()
            (cellX, cellY) = self.scrollToAspect(aspect2)
            aspect2_point = self.inventoryCellCoordsToPixelCoords(cellX, cellY)
            eventsDelay()
            aspect2_point.click()
            self._showDebugClick(aspect2_point)
            eventsDelay()
            for _ in range(times):
                self.pointAspectsMixCreate.click()
                self._showDebugClick(self.pointAspectsMixCreate)
                eventsDelay()

        # Updating counts of aspects
        aspect.count += times
        aspect1.count -= times
        aspect2.count -= times


    def fillByLinkMap(self, aspectsMap: dict[(int, int), str]):
        logging.info(f"Filling aspects by link map: {aspectsMap}")

        # Оптимизируем порядок аспектов, чтобы пришлось меньше листать инвентарь
        aspectsListMap = list(aspectsMap.items())
        aspectsListMap.sort(key=lambda pair: self.getAspectByName(pair[1]).uid)
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
        debugHighlightingRect = Rect(LTx, LTy,
                                     RTx, RTy,
                                     fill=QColor('blue'), fillOpacity=0.3, lineWidth=1,
                                     color=QColor('blue'))
        self.UI.addObject(debugHighlightingRect)
        return debugHighlightingRect

    def takeScreenshot(self, LTx, LTy, RBx, RBy, debugHighlightingRect=None) -> Image.Image:
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

    def updateAvailableAspectsInInventory(self, onFinishCallback: Callable, callbackArgs = []):
        logging.info("Detecting available aspects in inventory...")
        self.availableAspects = []

        debugHighlightingRect = self.addDebugHighlightingRect()
        slotWidth = (self.rectAspectsListingRB.x - self.rectAspectsListingLT.x) / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = (self.rectAspectsListingRB.y - self.rectAspectsListingLT.y) / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        self.scrollToLeftSide()

        def detectAspects():
            def exitWithSort():
                self.UI.removeObject(debugHighlightingRect)

                # Sort found aspects
                self.availableAspects.sort(key=lambda a: a.uid)
                logging.info(f"All detected available aspects was sorted")
                self.logAvailableAspects()

                onFinishCallback(*callbackArgs)

            def detectionIteration(isFoundEndOfInventory = False, newAdditionalOffset = THAUM_ASPECTS_INVENTORY_SLOTS_X):
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

                # Find aspects on screenshot
                logging.info("Wait for prediction aspects")
                predictions = Neurolink.predict_inventory_aspects(screenshotImage)
                logging.info(f"Aspects predictions: {predictions}")

                logging.info("Wait for prediction counts")
                count_predictions = Neurolink.predict_inventory_aspects_count(screenshotImage)
                logging.info(f"Counts predictions:  {count_predictions}")

                # Approximate aspects coordinates by cells
                for prediction in predictions:
                    try:
                        aspect = self.getAspectByName(prediction.predictionName)
                        aspect_count = count_predictions[prediction.predictionName]
                        if aspect.count is None:  # count initialization
                            aspect.count = aspect_count or 0
                        else:
                            # If predictions differ we take minimal
                            # because it's better to underestimate than to overestimate aspects count
                            aspect.count = min(aspect.count, aspect_count)
                    except ValueError:
                        continue
                    coords = (
                        self.currentAspectsPageIdx + (THAUM_ASPECTS_INVENTORY_SLOTS_X - newAdditionalOffset) + prediction.x // slotWidth,
                        prediction.y // slotHeight,
                    )
                    aspect.cellX = coords[0]
                    aspect.cellY = coords[1]
                    logging.debug(f"Cur Page: {self.currentAspectsPageIdx}, offset: {newAdditionalOffset}, {aspect}, {aspect.cellX}, {aspect.cellY} ({prediction.x, prediction.y}), {slotWidth}, {slotHeight}")

                    self.availableAspects.append(aspect)

                logging.info(f"All found aspects: {self.availableAspects}")

                if isFoundEndOfInventory:
                    exitWithSort()
                    return

                # Try to scroll right on maximum of
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
                    eventsDelay()
                    renderDelay()
                    newScreenshotImage = self.takeScreenshot(
                        self.rectAspectsListingRB.x - slotWidth, self.rectAspectsListingLT.y,
                        self.rectAspectsListingRB.x, self.rectAspectsListingLT.y + slotHeight,
                        debugHighlightingRect
                    )
                    # check if we really scrolled right
                    screenshotsDiff = getImagesDiffPercent(previousScreenshotImage, newScreenshotImage)
                    logging.debug(f"Difference of two images before and after scrolling right: {screenshotsDiff}")
                    if screenshotsDiff < IMAGES_TOLERANCE_PERCENT:  # nothing changed - it's the end of inventory
                        logging.info(f"Found end of inventory. Detection ends")
                        self.maxAspectsPagesCount = self.currentAspectsPageIdx
                        isFoundEndOfInventory = True
                        self.currentAspectsPageIdx -= 1
                        logging.info(f"Total inventory pages: {self.maxAspectsPagesCount}")
                        break
                    newAdditionalOffset += 1
                    previousScreenshotImage = newScreenshotImage
                logging.info(f"New aspects page total width: {newAdditionalOffset}")

                if newAdditionalOffset > 0:
                    self.UI.setTimeout(DELAY_BETWEEN_EVENTS, detectionIteration, [isFoundEndOfInventory, newAdditionalOffset])
                else:
                    exitWithSort()

            self.UI.setTimeout(DELAY_BETWEEN_EVENTS, detectionIteration)
        self.UI.setTimeout(DELAY_BETWEEN_EVENTS, detectAspects)

    def logAvailableAspects(self):
        string = "All available aspects by columns:"
        for i in range(len(self.availableAspects)):
            if i % THAUM_ASPECTS_INVENTORY_SLOTS_Y == 0:
                string += f"\nCol {i // THAUM_ASPECTS_INVENTORY_SLOTS_Y + 1}: "
            string += str(self.availableAspects[i]) + " "
        logging.info(string)

    def getAvailableAspectsNames(self) -> set[str]:
        return set(map(lambda a: a.name, self.availableAspects))

    def getAvailableAspectIdx(self, aspect: Aspect) -> int | None:
        for i in range(len(self.availableAspects)):
            if self.availableAspects[i] == aspect:
                return i
        return None

    def getExistingAspectsOnField(self) -> tuple[dict[(int, int), str], set[(int, int)], set[(int, int)]]:
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
        predictions = Neurolink.predict_field_aspects(allHexagonsImage)
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
            if prediction.predictionName == NEUROLINK_FREE_HEXAGON_PREDICTION_NAME:
                isAspect = False
            elif prediction.predictionName == NEUROLINK_SCRIPT_IMAGE_PREDICTION_NAME:
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
            yCell = int(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1 + (yCenter - yTop + (
                (self.hexagonSlotSizeY / 2) if xCell % 2 != 0 else 0)) // self.hexagonSlotSizeY)
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
            if (cell.x, cell.y) not in noneHexagons:  # coordinates out of range
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
