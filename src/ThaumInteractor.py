import math
import time
from typing import Any, Union

import keyboard
import mouse
import pyautogui  # for screenshot
import imgcompare  # for aspects images compare
from PIL import Image
from PyQt5.QtGui import QColor

from src import Scenarios, UIPrimitives
from src.constants import INVENTORY_SLOTS_X, INVENTORY_SLOTS_Y, THAUM_ASPECTS_INVENTORY_SLOTS_X, \
    THAUM_ASPECTS_INVENTORY_SLOTS_Y, DELAY_BETWEEN_EVENTS, ASPECTS_IMAGES_SIZE, THAUM_TRANSLATION_CONFIG_PATH, \
    THAUM_CONTROLS_CONFIG_PATH, THAUM_ASPECT_RECIPES_CONFIG_PATH, EMPTY_ASPECT_SLOT_IMAGE_PATH, \
    THAUM_HEXAGONS_SLOTS_COUNT, THAUM_HEXAGONS_SLOTS_COUNT, HEXAGON_MASK_IMAGE_PATH, FREE_HEXAGON_SLOT_IMAGES_PATHS, \
    NONE_HEXAGON_SLOT_IMAGE_PATH, MASK_ONLY_NUMBER_IMAGE_PATH, MASK_WITHOUT_NUMBER_IMAGE_PATH, EMPTY_TOLERANCE_PERCENT, \
    getImagePathByNumber, ASPECT_COUNT_NUMBER_SIZE, DELAY_BETWEEN_RENDER, THAUM_VERSION_CONFIG_PATH, DEBUG, \
    HEXAGON_BORDER_MASK_IMAGE_PATH
from src.constants import getAspectImagePath
from src.utils import getImagesDiffPercent, readJSONConfig


def createTI(UI):
    pointsConfig = readJSONConfig(THAUM_CONTROLS_CONFIG_PATH)
    if pointsConfig is None:
        Scenarios.enroll(UI)
        return None
    thaum_version = readJSONConfig(THAUM_VERSION_CONFIG_PATH)
    if thaum_version is None:
        Scenarios.chooseThaumVersion(UI)
        return None

    recipesConfig = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
    if recipesConfig is None:
        raise ValueError("Can't open recipes config")
    recipesConfig = recipesConfig[thaum_version['version']]

    translationsConfig = readJSONConfig(THAUM_TRANSLATION_CONFIG_PATH)
    if translationsConfig is None:
        raise ValueError("Can't open translations config")

    recipesConfigTranslated = {}
    for aspectNameEng in recipesConfig.keys():
        aspectNameLat = translationsConfig[aspectNameEng]
        recipesConfigTranslated[aspectNameLat] = recipesConfig[aspectNameEng]
    return ThaumInteractor(UI, pointsConfig, recipesConfigTranslated, list(recipesConfigTranslated.keys()))


class P:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def move(self):
        mouse.move(self.x, self.y)

    def click(self, button=mouse.LEFT, shift=False):
        self.move()
        if not shift:
            mouse.click(button)
            return
        keyboard.press('shift')
        mouse.click(button)
        keyboard.release('shift')

    def hold(self, button=mouse.LEFT):
        self.move()
        mouse.press(button)

    def release(self, button=mouse.LEFT):
        self.move()
        mouse.release(button)



class Aspect:
    idx: int = None
    name: str = None
    image: Image.Image = None
    mask: Image.Image = None
    count: int = None

    def __init__(self, name: str, idx: int):
        self.name = name
        self.idx = idx

    def __str__(self):
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


    def __init__(self, UI, controlsConfig: dict[str, dict[str, float]], aspectsRecipes: dict[str, list[str]], availableAspects: list[str]):
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

        self.maxPagesCount = max(((len(availableAspects) - 1) // THAUM_ASPECTS_INVENTORY_SLOTS_Y) - 4, 0)
        self.recipes = aspectsRecipes

        self.allAspects = []
        for i in range(len(availableAspects)):
            self.allAspects.append(Aspect(availableAspects[i], i))
        self.loadAspectsImages()
        # self.availableAspects = self.getAvailableAspects()

    def loadImage(self, path: str, backgroundImage: Image.Image = None, noResize: bool = False) -> Image.Image:
        image = Image.open(path)
        if not noResize:
            image = self.imageResize(image)
        image = image.convert("RGBA")
        backgroundImage = backgroundImage or Image.new("RGBA", image.size, "BLACK")  # Create a white rgba background
        newImage = backgroundImage.convert("RGBA")
        newImage.paste(image, mask=image)  # Paste the image on the background. Go to the links given below for details.
        return newImage.convert('RGB')

    def loadAspectsImages(self):
        for aspect in self.allAspects:
            aspect.image = self.loadImage(getAspectImagePath(aspect.name), self.emptyAspectInventorySlotImage)
            aspect.mask = Image.open(getAspectImagePath(aspect.name, color=False)).convert("L")

    def scrollLeft(self):
        if self.currentAspectsPageIdx <= 0:
            return
        self.pointAspectsScrollLeft.click()
        self._showDebugClick(self.pointAspectsScrollLeft)
        self.currentAspectsPageIdx -= 1
    def scrollRight(self):
        if self.currentAspectsPageIdx == self.maxPagesCount:
            return
        self.pointAspectsScrollRight.click()
        self._showDebugClick(self.pointAspectsScrollRight)
        self.currentAspectsPageIdx += 1
    def scrollToLeftSide(self):
        if self.currentAspectsPageIdx is None:
            self.currentAspectsPageIdx = self.maxPagesCount
        for _ in range(self.currentAspectsPageIdx):
            self.scrollLeft()
            self.eventsDelay()
        self.currentAspectsPageIdx = 0
    def _showDebugClick(self, point, color=QColor('lightgreen')):
        if not DEBUG:
            return
        clickCircle = UIPrimitives.Circle(point.x, point.y, 20, color=color)
        def onTimeCallback(timeLeft):
            clickCircle.r = timeLeft / 1000 * 20
        self.UI.addObjectAndDeleteAfterTime(clickCircle, 1000, onTimeCallback)

    def scrollToRightSide(self):
        if self.currentAspectsPageIdx is None:
            self.currentAspectsPageIdx = 0
        for _ in range(self.maxPagesCount - self.currentAspectsPageIdx):
            self.scrollRight()
            self.eventsDelay()
        self.currentAspectsPageIdx = self.maxPagesCount
    def takeOutPaper(self):
        self.pointPapers.click()
        self._showDebugClick(self.pointPapers)
        self.eventsDelay()
        self.pointWorkingInventorySlot.click()
        self._showDebugClick(self.pointWorkingInventorySlot)
    def insertPaper(self):
        self.pointWorkingInventorySlot.click()
        self._showDebugClick(self.pointWorkingInventorySlot)
        self.eventsDelay()
        self.pointPapers.click()
        self._showDebugClick(self.pointPapers)
        # self.pointWorkingInventorySlot.move()
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

    def takeAspectByCellCoords(self, cellX, cellY):
        areaWidth = self.rectAspectsListingRB.x - self.rectAspectsListingLT.x
        areaHeight = self.rectAspectsListingRB.y - self.rectAspectsListingLT.y
        slotWidth = areaWidth / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = areaHeight / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        aspectPoint = P(
            self.rectAspectsListingLT.x + (slotWidth * 0.5) + slotWidth * cellX,
            self.rectAspectsListingLT.y + (slotHeight * 0.5) + slotHeight * cellY
        )
        aspectPoint.hold()
        self._showDebugClick(aspectPoint, QColor('blue'))

    def putAspect(self, cellX, cellY):
        areaWidth = self.rectHexagonsRB.x - self.rectHexagonsLT.x
        areaHeight = self.rectHexagonsRB.y - self.rectHexagonsLT.y

        slotWidth = areaWidth / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = areaHeight / THAUM_ASPECTS_INVENTORY_SLOTS_Y

        aspectPoint = P(
            self.rectHexagonsLT.x + (slotWidth * 0.5) + slotWidth * cellX,
            self.rectHexagonsLT.y + (slotHeight * 0.5) + slotHeight * cellY
        )
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

        cellPageIdxMin = max(cellX - 4, 0)
        cellPageIdxMax = min(cellX, self.maxPagesCount)

        if self.currentAspectsPageIdx < cellPageIdxMin:
            for _ in range(self.currentAspectsPageIdx, cellPageIdxMin):
                self.scrollRight()
                self.eventsDelay()
        elif self.currentAspectsPageIdx > cellPageIdxMax:
            for _ in range(cellPageIdxMax, self.currentAspectsPageIdx):
                self.scrollRight()
                self.eventsDelay()

        return cellX, cellY - self.currentAspectsPageIdx

    def takeAspect(self, aspect: Aspect):
        (cellX, cellY) = self.scrollToAspect(aspect)
        self.takeAspectByCellCoords(cellX, cellY)

    def eventsDelay(self):
        time.sleep(DELAY_BETWEEN_EVENTS)
    def renderDelay(self):
        time.sleep(DELAY_BETWEEN_RENDER)

    def mixAspect(self, aspect: Aspect, useShift=True):
        recipe = self.recipes.get(aspect.name)
        if recipe is None:
            raise ValueError(f"Aspect {aspect.name} not exists in known aspects recipes")
        if len(recipe[1]) < 2:
            raise ValueError(f"Aspect {aspect.name} is a basic and can't be created using mixing")

        if useShift:
            (cellX, cellY) = self.scrollToAspect(aspect)
            self.eventsDelay()
            P(cellX, cellY).click(shift=True)
            self._showDebugClick(P(cellX, cellY))
            return

        (cellX, cellY) = self.scrollToAspect(recipe[0])
        self.eventsDelay()
        P(cellX, cellY).click()
        self._showDebugClick(P(cellX, cellY))
        self.eventsDelay()
        (cellX, cellY) = self.scrollToAspect(recipe[1])
        self.eventsDelay()
        P(cellX, cellY).click()
        self._showDebugClick(P(cellX, cellY))
        self.eventsDelay()
        self.pointAspectsMixCreate.click()
        self._showDebugClick(self.pointAspectsMixCreate)

    def fillByLinkMap(self, aspectsMap: dict[str, (int, int)]):
        for aspectName in aspectsMap.keys():
            aspect = self.getAspectByName(aspectName)
            self.takeAspect(aspect)
            self.eventsDelay()
            self.putAspect(*aspectsMap[aspectName])
            self.eventsDelay()

    def imageResize(self, image: Image.Image):
        return image.resize((ASPECTS_IMAGES_SIZE, ASPECTS_IMAGES_SIZE), Image.Resampling.LANCZOS)

    def findClosestAspectImage(self, image: Image.Image, mask: Image.Image = None, specialReturns: list[(Union[Image.Image, list[Image.Image]], Any)] = []):
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
            # print("Cur:", aspect.name, curDiff, "| Min:", minDiffAspect.name, minDiff)

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
                print(imageToCompare.size, diffWithSpecialImage, "| Min: ", minDiffAspect, minDiff)
        return minDiffAspect

    def getAvailableAspects(self):
        print("Detecting available aspects...")
        availableAspects = []
        debugHighlightingRect = None
        if DEBUG:
            debugHighlightingRect = UIPrimitives.Rect(self.rectAspectsListingLT.x, self.rectAspectsListingLT.y, self.rectAspectsListingRB.x, self.rectAspectsListingRB.y, fill=QColor('blue'), fillOpacity=0.3, lineWidth=1, color=QColor('blue'))
            self.UI.addObject(debugHighlightingRect)
        slotWidth = (self.rectAspectsListingRB.x - self.rectAspectsListingLT.x) / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = (self.rectAspectsListingRB.y - self.rectAspectsListingLT.y) / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        self.scrollToLeftSide()
        x = 0
        while True:
            for y in range(THAUM_ASPECTS_INVENTORY_SLOTS_Y):
                regionLX = self.rectAspectsListingLT.x + x * slotWidth
                regionLY = self.rectAspectsListingLT.y + y * slotHeight
                if DEBUG:
                    debugHighlightingRect.setCoords(regionLX, regionLY, regionLX + slotWidth, regionLY + slotHeight)
                    debugHighlightingRect.setVisibility(False)
                    self.renderDelay()
                imageInSlot = self.imageResize(pyautogui.screenshot(region=(
                    regionLX, regionLY,
                    slotWidth, slotHeight
                )))
                if DEBUG:
                    debugHighlightingRect.setVisibility(True)
                diffWithEmpty = getImagesDiffPercent(imageInSlot, self.emptyAspectInventorySlotImage, [self.maskOnlyNumbers])
                if diffWithEmpty < EMPTY_TOLERANCE_PERCENT:
                    print("Found empty place. Detection ends")
                    self.maxPagesCount = self.currentAspectsPageIdx
                    if DEBUG: self.UI.removeObject(debugHighlightingRect)
                    return availableAspects
                minDiffAspect = self.findClosestAspectImage(imageInSlot, self.maskWithoutNumbers)

                aspectCount = 0
                for i in range(2, -1, -1):
                    numberImage = imageInSlot.crop((
                        ASPECTS_IMAGES_SIZE - ASPECT_COUNT_NUMBER_SIZE[0] * (i + 1), ASPECTS_IMAGES_SIZE - ASPECT_COUNT_NUMBER_SIZE[1],
                        ASPECTS_IMAGES_SIZE - ASPECT_COUNT_NUMBER_SIZE[0] * i, ASPECTS_IMAGES_SIZE
                    ))
                    minDiffCount = 100
                    minNum = None
                    for idx in range(len(self.numbersImages)):
                        curDiff = getImagesDiffPercent(numberImage, self.numbersImages[idx])
                        if curDiff < minDiffCount:
                            minDiffCount = curDiff
                            minNum = idx
                    aspectCount = int(aspectCount) * 10 + int(minNum)
                minDiffAspect.count = aspectCount
                print(minDiffAspect)

                availableAspects.append(minDiffAspect)
            if x == THAUM_ASPECTS_INVENTORY_SLOTS_X - 1:
                self.scrollRight()
                self.eventsDelay()
            else:
                x += 1


    def printAvailableAspects(self):
        for i in range(len(self.availableAspects)):
            print(self.availableAspects[i], end=" ")
            if i % THAUM_ASPECTS_INVENTORY_SLOTS_Y == THAUM_ASPECTS_INVENTORY_SLOTS_Y - 1:
                print()
        print()

    def getExistingAspectsOnField(self):
        self.printAvailableAspects()
        debugHighlightingRect = None
        if DEBUG:
            debugHighlightingRect = UIPrimitives.Rect(
                self.rectHexagonsCC.x + (-THAUM_HEXAGONS_SLOTS_COUNT / 2) * self.hexagonSlotSizeX,
                self.rectHexagonsCC.y + (-THAUM_HEXAGONS_SLOTS_COUNT / 2) * self.hexagonSlotSizeY,
                self.rectHexagonsCC.x + (THAUM_HEXAGONS_SLOTS_COUNT / 2) * self.hexagonSlotSizeX,
                self.rectHexagonsCC.y + THAUM_HEXAGONS_SLOTS_COUNT / 2 * self.hexagonSlotSizeY,
                fill=QColor('blue'), fillOpacity=0.3, lineWidth=1, color=QColor('blue'))
            self.UI.addObject(debugHighlightingRect)
            self.renderDelay()
        realHexagonSlotHeight = self.hexagonSlotSizeY * 0.85
        existingAspects = []
        freeHexagons = []
        noneHexagons = []
        for x in range(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1, THAUM_HEXAGONS_SLOTS_COUNT // 2 + 1):
            for y in range(-THAUM_HEXAGONS_SLOTS_COUNT // 2 + abs(x) // 2 + 1,
                           THAUM_HEXAGONS_SLOTS_COUNT // 2 - (abs(x) + 1) // 2 + 1):
                print(x, y)
                # find pos of hexagons
                slotLTx = self.rectHexagonsCC.x + x * self.hexagonSlotSizeX - self.hexagonSlotSizeX / 2
                slotLTy = self.rectHexagonsCC.y + y * self.hexagonSlotSizeY - self.hexagonSlotSizeX / 2
                if x % 2 == 1:
                    slotLTy += self.hexagonSlotSizeY / 2

                screenshotLTy = slotLTy - (self.hexagonSlotSizeX - realHexagonSlotHeight) / 2
                if DEBUG:
                    debugHighlightingRect.setCoords(slotLTx, screenshotLTy, slotLTx + self.hexagonSlotSizeX,
                                                    slotLTy + self.hexagonSlotSizeX)
                    if x >= -2:
                        self.renderDelay()
                    debugHighlightingRect.setVisibility(False)
                    time.sleep(0.1)

                # Ensure values are integers before taking screenshot
                region = (
                    int(slotLTx),
                    int(screenshotLTy),
                    int(self.hexagonSlotSizeX),
                    int(self.hexagonSlotSizeX)
                )

                # Print region values for debugging
                print(f"Region values: {region}")
                print(f"Region types: {tuple(type(value) for value in region)}")

                imageInSlot = self.imageResize(pyautogui.screenshot(region=region))

                if DEBUG:
                    debugHighlightingRect.setVisibility(True)
                minDiffAspect = self.findClosestAspectImage(imageInSlot, mask=self.hexagonBorderMaskImage,
                                                            specialReturns=[(self.freeHexagonImages, -1),
                                                                            (self.noneHexagonImage, -2)])
                if minDiffAspect == -1:  # free slot
                    print("FREE")
                    freeHexagons.append((x, y))
                elif minDiffAspect == -2:  # none slot
                    print("NONE (NO CELL)")
                    noneHexagons.append((x, y))
                else:  # aspect in slot
                    print(minDiffAspect.name)
                    existingAspects.append((minDiffAspect, (x, y)))
        print("END!!!")
        print(existingAspects, noneHexagons)
        exit()
        return existingAspects, freeHexagons
