import logging
import math
from typing import Any, Union

import keyboard
import mouse
import pyautogui  # for screenshot
from PIL import Image
from PyQt5.QtGui import QColor, QPixmap

from src.UI import UIPrimitives
from src.controllers import Scenarios
from src.utils.constants import INVENTORY_SLOTS_X, INVENTORY_SLOTS_Y, THAUM_ASPECTS_INVENTORY_SLOTS_X, \
    THAUM_ASPECTS_INVENTORY_SLOTS_Y, ASPECTS_IMAGES_SIZE, \
    THAUM_CONTROLS_CONFIG_PATH, THAUM_ASPECT_RECIPES_CONFIG_PATH, THAUM_ASPECTS_ORDER_CONFIG_PATH, \
    EMPTY_ASPECT_SLOT_IMAGE_PATH, THAUM_HEXAGONS_SLOTS_COUNT, HEXAGON_MASK_IMAGE_PATH, FREE_HEXAGON_SLOT_IMAGES_PATHS, \
    NONE_HEXAGON_SLOT_IMAGE_PATH, MASK_ONLY_NUMBER_IMAGE_PATH, MASK_WITHOUT_NUMBER_IMAGE_PATH, EMPTY_TOLERANCE_PERCENT, \
    getImagePathByNumber, THAUM_VERSION_CONFIG_PATH, DEBUG, \
    HEXAGON_BORDER_MASK_IMAGE_PATH, MARGIN, UNKNOWN_ASPECT_IMAGE_PATH
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
    currentAspectsPageIdx = 0
    allAspects: list[Aspect] = []
    availableAspects: list[Aspect] = []
    recipes: dict[str, [str, str]]
    maxPagesCount: int = 1
    numbersImages: list[Image.Image] = []

    pointWritingMaterials: P
    pointPapers: P
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

        self.maxPagesCount = max(((len(orderedAvailableAspects) - 1) // THAUM_ASPECTS_INVENTORY_SLOTS_Y) - 4, 0)
        self.recipes = aspectsRecipes

        self.allAspects = []
        for i in range(len(orderedAvailableAspects)):
            self.allAspects.append(Aspect(orderedAvailableAspects[i], i))
        self.loadAspectsImages()
        logging.info(f"ThaumcraftInteractor successfully initialized")
        # self.availableAspects = self.getAvailableAspects()

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
            self.currentAspectsPageIdx = self.maxPagesCount
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
        clickCircle = UIPrimitives.Circle(point.x, point.y, 20, color=color)

        def onTimeCallback(timeLeft):
            clickCircle.r = timeLeft / 1000 * 20

        self.UI.addObjectAndDeleteAfterTime(clickCircle, 1000, onTimeCallback)

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
            for i in range(len(self.allAspects)):
                if self.allAspects[i].name == aspectName:
                    return i
            return 999999
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

    def findClosestAspectImage(self, image: Image.Image, mask: Image.Image = None,
                               specialReturns: list[(Union[Image.Image, list[Image.Image]], Any)] = []):
        minDiff = 100
        minDiffAspect = None
        for aspect in self.allAspects:
            if mask is not None:
                curDiff = getImagesDiffPercent(image, aspect.image, [mask])
            else:
                curDiff = getImagesDiffPercent(image, aspect.image)

            if curDiff < minDiff:
                minDiff = curDiff
                minDiffAspect = aspect
            image.save('image_compare1.png')
            aspect.image.save('image_compare2.png')
            # logging.debug(f"Cur: {aspect.name}, {curDiff} | Min: {minDiffAspect.name}, {minDiff}")

        for specialPair in specialReturns:
            imagesToCompare = specialPair[0]
            if type(imagesToCompare) != list:
                imagesToCompare = [imagesToCompare]
            for imageToCompare in imagesToCompare:
                if mask is not None:
                    diffWithSpecialImage = getImagesDiffPercent(image, imageToCompare, [mask])
                else:
                    diffWithSpecialImage = getImagesDiffPercent(image, imageToCompare)
                if diffWithSpecialImage < minDiff:
                    minDiff = diffWithSpecialImage
                    minDiffAspect = specialPair[1]
                image.save('image_compare1.png')
                imageToCompare.save('image_compare2.png')
                logging.debug(f"{imageToCompare.size}, {diffWithSpecialImage} | Min: {minDiffAspect}, {minDiff}")
        return minDiffAspect

    # def getAvailableAspects(self):
    #     logging.info("Detecting available aspects...")
    #     availableAspects = []
    #     debugHighlightingRect = None
    #     if DEBUG:
    #         debugHighlightingRect = UIPrimitives.Rect(self.rectAspectsListingLT.x, self.rectAspectsListingLT.y, self.rectAspectsListingRB.x, self.rectAspectsListingRB.y, fill=QColor('blue'), fillOpacity=0.3, lineWidth=1, color=QColor('blue'))
    #         self.UI.addObject(debugHighlightingRect)
    #     slotWidth = (self.rectAspectsListingRB.x - self.rectAspectsListingLT.x) / THAUM_ASPECTS_INVENTORY_SLOTS_X
    #     slotHeight = (self.rectAspectsListingRB.y - self.rectAspectsListingLT.y) / THAUM_ASPECTS_INVENTORY_SLOTS_Y
    #     self.scrollToLeftSide()
    #     x = 0
    #     while True:
    #         for y in range(THAUM_ASPECTS_INVENTORY_SLOTS_Y):
    #             regionLX = self.rectAspectsListingLT.x + x * slotWidth
    #             regionLY = self.rectAspectsListingLT.y + y * slotHeight
    #             if DEBUG:
    #                 debugHighlightingRect.setCoords(
    #                     regionLX, regionLY,
    #                     regionLX + slotWidth, regionLY + slotHeight
    #                 )
    #                 debugHighlightingRect.setVisibility(False)
    #                 renderDelay()
    #             imageInSlot = self.imageResize(pyautogui.screenshot(region=(
    #                 regionLX, regionLY,
    #                 slotWidth, slotHeight
    #             )))
    #             if DEBUG:
    #                 debugHighlightingRect.setVisibility(True)
    #             diffWithEmpty = getImagesDiffPercent(imageInSlot, self.emptyAspectInventorySlotImage, [self.maskOnlyNumbers])
    #             if diffWithEmpty < EMPTY_TOLERANCE_PERCENT:
    #                 logging.debug("Found empty place. Detection ends")
    #                 self.maxPagesCount = self.currentAspectsPageIdx
    #                 if DEBUG: self.UI.removeObject(debugHighlightingRect)
    #                 return availableAspects
    #             minDiffAspect = self.findClosestAspectImage(imageInSlot, self.maskWithoutNumbers)
    #
    #             aspectCount = 0
    #             for i in range(2, -1, -1):
    #                 numberImage = imageInSlot.crop((
    #                     ASPECTS_IMAGES_SIZE - ASPECT_COUNT_NUMBER_SIZE[0] * (i + 1), ASPECTS_IMAGES_SIZE - ASPECT_COUNT_NUMBER_SIZE[1],
    #                     ASPECTS_IMAGES_SIZE - ASPECT_COUNT_NUMBER_SIZE[0] * i, ASPECTS_IMAGES_SIZE
    #                 ))
    #                 minDiffCount = 100
    #                 minNum = None
    #                 for idx in range(len(self.numbersImages)):
    #                     curDiff = getImagesDiffPercent(numberImage, self.numbersImages[idx])
    #                     if curDiff < minDiffCount:
    #                         minDiffCount = curDiff
    #                         minNum = idx
    #                 aspectCount = int(aspectCount) * 10 + int(minNum)
    #             minDiffAspect.count = aspectCount
    #             logging.debug(f"Min diff with: {minDiffAspect}")
    #
    #             availableAspects.append(minDiffAspect)
    #         if x == THAUM_ASPECTS_INVENTORY_SLOTS_X - 1:
    #             self.scrollRight()
    #             eventsDelay()
    #         else:
    #             x += 1
    #     logging.info("Detected aspects: {self.availableAspects}")
    def getAvailableAspects(self):
        logging.info("Detecting available aspects...")
        debugHighlightingRect = None
        if DEBUG:
            debugHighlightingRect = UIPrimitives.Rect(self.rectAspectsListingLT.x, self.rectAspectsListingLT.y,
                                                      self.rectAspectsListingRB.x, self.rectAspectsListingRB.y,
                                                      fill=QColor('blue'), fillOpacity=0.3, lineWidth=1,
                                                      color=QColor('blue'))
            self.UI.addObject(debugHighlightingRect)
        slotWidth = (self.rectAspectsListingRB.x - self.rectAspectsListingLT.x) / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = (self.rectAspectsListingRB.y - self.rectAspectsListingLT.y) / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        self.scrollToLeftSide()
        xCell = THAUM_ASPECTS_INVENTORY_SLOTS_X - 1
        yCell = 0
        regionLX = self.rectAspectsListingLT.x + xCell * slotWidth
        regionLY = self.rectAspectsListingLT.y + yCell * slotHeight
        previousImageInSlot = None
        while True:
            if DEBUG:
                debugHighlightingRect.setCoords(
                    regionLX, regionLY,
                    regionLX + slotWidth, regionLY + slotHeight
                )
                debugHighlightingRect.setVisibility(False)
                renderDelay()
            imageInSlot = self.imageResize(pyautogui.screenshot(region=(
                regionLX, regionLY,
                slotWidth, slotHeight
            )))
            if DEBUG:
                debugHighlightingRect.setVisibility(True)
            if previousImageInSlot:
                diffWithEmpty = getImagesDiffPercent(previousImageInSlot, imageInSlot)
                if diffWithEmpty < EMPTY_TOLERANCE_PERCENT:
                    logging.info(f"Found end of inventory. Detection ends. Total pages: {self.currentAspectsPageIdx}")
                    self.maxPagesCount = self.currentAspectsPageIdx
                    if DEBUG: self.UI.removeObject(debugHighlightingRect)
                    break
            previousImageInSlot = imageInSlot
            self.scrollRight()
            eventsDelay()

        availableAspects = []
        return availableAspects

    def logAvailableAspects(self):
        string = ""
        for i in range(len(self.availableAspects)):
            string += str(self.availableAspects[i]) + " "
            if i % THAUM_ASPECTS_INVENTORY_SLOTS_Y == THAUM_ASPECTS_INVENTORY_SLOTS_Y - 1:
                logging.info(string)
                string = ""
        logging.info(string)

    # def getExistingAspectsOnField(self):
    # self.logAvailableAspects()
    # debugHighlightingRect = None
    # if DEBUG:
    #     debugHighlightingRect = UIPrimitives.Rect(
    #         self.rectHexagonsCC.x + (-THAUM_HEXAGONS_SLOTS_COUNT / 2) * self.hexagonSlotSizeX,
    #         self.rectHexagonsCC.y + (-THAUM_HEXAGONS_SLOTS_COUNT / 2) * self.hexagonSlotSizeY,
    #         self.rectHexagonsCC.x + (THAUM_HEXAGONS_SLOTS_COUNT / 2) * self.hexagonSlotSizeX,
    #         self.rectHexagonsCC.y + THAUM_HEXAGONS_SLOTS_COUNT / 2 * self.hexagonSlotSizeY,
    #         fill=QColor('blue'), fillOpacity=0.3, lineWidth=1, color=QColor('blue'))
    #     self.UI.addObject(debugHighlightingRect)
    #     renderDelay()
    # realHexagonSlotHeight = self.hexagonSlotSizeY * 0.85
    # existingAspects = []
    # freeHexagons = []
    # noneHexagons = []
    # for x in range(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1, THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1):
    #     for y in range(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + abs(x) // 2 + 1, THAUM_HEXAGONS_SLOTS_COUNT // 2 - (abs(x) + 1) // 2 + 1):
    #         logging.debug(f"{x}, {y}")
    #         # find pos of hexagons
    #         slotLTx = self.rectHexagonsCC.x + x * self.hexagonSlotSizeX - self.hexagonSlotSizeX / 2
    #         slotLTy = self.rectHexagonsCC.y + y * self.hexagonSlotSizeY - self.hexagonSlotSizeX / 2
    #         if x % 2 == 1:
    #             slotLTy += self.hexagonSlotSizeY / 2
    #
    #         screenshotLTy = slotLTy - (self.hexagonSlotSizeX - realHexagonSlotHeight) / 2
    #         if DEBUG:
    #             debugHighlightingRect.setCoords(slotLTx, screenshotLTy, slotLTx + self.hexagonSlotSizeX, slotLTy + self.hexagonSlotSizeX)
    #             if x >= -2:
    #                 renderDelay()
    #             debugHighlightingRect.setVisibility(False)
    #             time.sleep(0.1)
    #         imageInSlot = self.imageResize(pyautogui.screenshot(region=(
    #             slotLTx, screenshotLTy,
    #             self.hexagonSlotSizeX, self.hexagonSlotSizeX
    #         )))
    #
    #         if DEBUG:
    #             debugHighlightingRect.setVisibility(True)
    #         minDiffAspect = self.findClosestAspectImage(imageInSlot, mask=self.hexagonBorderMaskImage, specialReturns=[(self.freeHexagonImages, -1), (self.noneHexagonImage, -2)])
    #         if minDiffAspect == -1:    # free slot
    #             logging.debug("FREE")
    #             freeHexagons.append((x, y))
    #         elif minDiffAspect == -2:  # none slot
    #             logging.debug("NONE (NO CELL)")
    #             noneHexagons.append((x, y))
    #         else:                      # aspect in slot
    #             logging.debug(minDiffAspect.name)
    #             existingAspects.append((minDiffAspect, (x, y)))
    # logging.debug("END!!!")
    # logging.debug(f"{existingAspects}, {noneHexagons}")
    # exit()
    # return existingAspects, freeHexagons
