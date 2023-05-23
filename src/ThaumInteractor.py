import time

import keyboard
import mouse

from src.constants import INVENTORY_SLOTS_X, INVENTORY_SLOTS_Y, THAUM_ASPECTS_INVENTORY_SLOTS_X, \
    THAUM_ASPECTS_INVENTORY_SLOTS_Y, DELAY_BETWEEN_EVENTS


class P:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def click(self, button=mouse.LEFT, shift=False):
        mouse.move(self.x, self.y)
        if not shift:
            mouse.click(button)
            return
        keyboard.press('shift')
        mouse.click(button)
        keyboard.release('shift')

    def hold(self, button=mouse.LEFT):
        mouse.move(self.x, self.y)
        mouse.press(button)

    def release(self, button=mouse.LEFT):
        mouse.move(self.x, self.y)
        mouse.release(button)


class ThaumInteractor:
    workingInventorySlot = 0  # can be 0..26 (inventory 9x3)
    currentAspectsPageIdx = 0
    aspects: list[str] = []
    recipes: dict[str, (str, str)]
    pagesCount: int = None

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
    rectHexagonsLT: P
    rectHexagonsRB: P

    def __init__(self, controlsConfig: dict[str, dict[str, float]], availableAspects: list[str], aspectsRecipes: dict[str, (str, str)]):
        conf = controlsConfig
        self.pointWritingMaterials = P(conf['pointWritingMaterials']['x'], conf['pointWritingMaterials']['y'])
        self.pointPapers = P(conf['pointPapers']['x'], conf['pointPapers']['y'])
        self.rectAspectsListingLT = P(conf['rectAspectsListingLT']['x'], conf['rectAspectsListingLT']['y'])
        self.rectAspectsListingRB = P(conf['rectAspectsListingRB']['x'], conf['rectAspectsListingRB']['y'])
        self.pointAspectsScrollLeft = P(conf['pointAspectsScrollLeft']['x'], conf['pointAspectsScrollLeft']['y'])
        self.pointAspectsScrollRight = P(conf['pointAspectsScrollRight']['x'], conf['pointAspectsScrollRight']['y'])
        self.pointAspectsMixLeft = P(conf['pointAspectsMixLeft']['x'], conf['pointAspectsMixLeft']['y'])
        self.pointAspectsMixCreate = P(conf['pointAspectsMixCreate']['x'], conf['pointAspectsMixCreate']['y'])
        self.pointAspectsMixRight = P(conf['pointAspectsMixRight']['x'], conf['pointAspectsMixRight']['y'])
        self.rectInventoryLT = P(conf['rectInventoryLT']['x'], conf['rectInventoryLT']['y'])
        self.rectInventoryRB = P(conf['rectInventoryRB']['x'], conf['rectInventoryRB']['y'])
        self.rectHexagonsLT = P(conf['rectHexagonsLT']['x'], conf['rectHexagonsLT']['y'])
        self.rectHexagonsRB = P(conf['rectHexagonsRB']['x'], conf['rectHexagonsRB']['y'])

        self.aspects = availableAspects
        self.recipes = aspectsRecipes
        self.pagesCount = max(((len(availableAspects) - 1) // THAUM_ASPECTS_INVENTORY_SLOTS_Y) - 4, 0)

    def scrollLeft(self):
        if self.currentAspectsPageIdx <= 0:
            raise IndexError("Trying to scroll page to -1")
        self.pointAspectsScrollLeft.click()
        self.currentAspectsPageIdx -= 1
    def scrollRight(self):
        self.pointAspectsScrollRight.click()
        self.currentAspectsPageIdx += 1

    def takeOutPaper(self):
        self.pointPapers.click(shift=True)
    def insertPaper(self):
        areaWidth = self.rectInventoryRB.x - self.rectInventoryLT.x
        areaHeight = self.rectInventoryRB.y - self.rectInventoryLT.y
        slotWidth = areaWidth / INVENTORY_SLOTS_X
        slotHeight = areaHeight / INVENTORY_SLOTS_Y
        P(
            self.rectInventoryLT.x + (slotWidth * 0.5) + slotWidth * (self.workingInventorySlot % INVENTORY_SLOTS_X),
            self.rectInventoryLT.y + (slotHeight * 0.5) + slotHeight * (self.workingInventorySlot // INVENTORY_SLOTS_X)
        ).click(shift=True)

    def takeAspectByCellCoords(self, cellX, cellY):
        areaWidth = self.rectAspectsListingRB.x - self.rectAspectsListingLT.x
        areaHeight = self.rectAspectsListingRB.y - self.rectAspectsListingLT.y
        slotWidth = areaWidth / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = areaHeight / THAUM_ASPECTS_INVENTORY_SLOTS_Y
        P(
            self.rectAspectsListingLT.x + (slotWidth * 0.5) + slotWidth * cellX,
            self.rectAspectsListingLT.y + (slotHeight * 0.5) + slotHeight * cellY
        ).hold()
    def putAspect(self, cellX, cellY):
        areaWidth = self.rectHexagonsRB.x - self.rectHexagonsLT.x
        areaHeight = self.rectHexagonsRB.y - self.rectHexagonsLT.y

        slotWidth = areaWidth / THAUM_ASPECTS_INVENTORY_SLOTS_X
        slotHeight = areaHeight / THAUM_ASPECTS_INVENTORY_SLOTS_Y

        P(
            self.rectAspectsListingLT.x + (slotWidth * 0.5) + slotWidth * cellX,
            self.rectAspectsListingLT.y + (slotHeight * 0.5) + slotHeight * cellY
        ).release()

    def scrollToAspect(self, aspect: str) -> (int, int):
        try:
            aspectIdx = self.aspects.index(aspect)
        except ValueError:
            raise ValueError(f"Aspect {aspect} not exists in known aspects list")

        cellX = aspectIdx // THAUM_ASPECTS_INVENTORY_SLOTS_Y
        cellY = aspectIdx % THAUM_ASPECTS_INVENTORY_SLOTS_Y

        cellPageIdxMin = max(cellX - 4, 0)
        cellPageIdxMax = min(cellX, self.pagesCount)

        if self.currentAspectsPageIdx < cellPageIdxMin:
            for _ in range(self.currentAspectsPageIdx, cellPageIdxMin):
                self.scrollRight()
                self.eventsDelay()
        elif self.currentAspectsPageIdx > cellPageIdxMax:
            for _ in range(cellPageIdxMax, self.currentAspectsPageIdx):
                self.scrollRight()
                self.eventsDelay()

        return cellX, cellY - self.currentAspectsPageIdx

    def takeAspect(self, aspect: str):
        (cellX, cellY) = self.scrollToAspect(aspect)
        self.takeAspectByCellCoords(cellX, cellY)

    def eventsDelay(self):
        time.sleep(DELAY_BETWEEN_EVENTS)

    def mixAspect(self, aspect, useShift=True):
        if useShift:
            (cellX, cellY) = self.scrollToAspect(aspect)
            self.eventsDelay()
            P(cellX, cellY).click(shift=True)
            return

        recipe = self.recipes.get(aspect)
        if recipe is None:
            raise ValueError(f"Aspect {aspect} not exists in known aspects recipes")

        (cellX, cellY) = self.scrollToAspect(recipe[0])
        self.eventsDelay()
        P(cellX, cellY).click()
        self.eventsDelay()
        (cellX, cellY) = self.scrollToAspect(recipe[0])
        self.eventsDelay()
        P(cellX, cellY).click()
        self.eventsDelay()
        self.pointAspectsMixCreate.click()

    def fillByLinkMap(self, aspectsMap: dict[str, (int, int)]):
        for aspect in aspectsMap.keys():
            self.takeAspect(aspect)
            self.eventsDelay()
            self.putAspect(*aspectsMap[aspect])
            self.eventsDelay()
