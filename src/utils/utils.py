import json
import logging
import math
import os
import re
import time

from PIL import Image
from PyQt5.QtGui import QColor

from src.utils.LinkableValue import linkableValueDumpsToJSON
from src.utils.constants import THAUM_CONTROLS_CONFIG_PATH, THAUM_ASPECT_RECIPES_CONFIG_PATH, THAUM_VERSION_CONFIG_PATH, \
    DELAY_BETWEEN_EVENTS, DELAY_BETWEEN_RENDER, THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def createDirByFilePath(fullpath: str):
    dir_path = os.path.dirname(fullpath)
    if not os.path.exists(dir_path):
        logging.info(f"Directory {dir_path} not exists. Creating...")
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"Directory {dir_path} successfully created")


def saveJSONConfig(fullpath: str, jsonToSave: dict):
    createDirByFilePath(fullpath)
    with open(fullpath, 'w') as file:
        json.dump(jsonToSave, file, indent=4, ensure_ascii=False, default=linkableValueDumpsToJSON)


def saveThaumControlsConfig(pointWritingMaterials, pointPapers, rectAspectsListingLT, rectAspectsListingRB,
                            pointAspectsScrollLeft, pointAspectsScrollRight,
                            pointAspectsMixLeft, pointAspectsMixCreate, pointAspectsMixRight, rectInventoryLT,
                            rectInventoryRB, rectHexagonsCC, hexagonSlotSizeY):
    saveJSONConfig(THAUM_CONTROLS_CONFIG_PATH, {
        "pointWritingMaterials": {"x": pointWritingMaterials.x, "y": pointWritingMaterials.y},
        "pointPapers": {"x": pointPapers.x, "y": pointPapers.y},
        "rectAspectsListingLT": {"x": rectAspectsListingLT.x, "y": rectAspectsListingLT.y},
        "rectAspectsListingRB": {"x": rectAspectsListingRB.x, "y": rectAspectsListingRB.y},
        "pointAspectsScrollLeft": {"x": pointAspectsScrollLeft.x, "y": pointAspectsScrollLeft.y},
        "pointAspectsScrollRight": {"x": pointAspectsScrollRight.x, "y": pointAspectsScrollRight.y},
        "pointAspectsMixLeft": {"x": pointAspectsMixLeft.x, "y": pointAspectsMixLeft.y},
        "pointAspectsMixCreate": {"x": pointAspectsMixCreate.x, "y": pointAspectsMixCreate.y},
        "pointAspectsMixRight": {"x": pointAspectsMixRight.x, "y": pointAspectsMixRight.y},
        "rectInventoryLT": {"x": rectInventoryLT.x, "y": rectInventoryLT.y},
        "rectInventoryRB": {"x": rectInventoryRB.x, "y": rectInventoryRB.y},
        "rectHexagonsCC": {"x": rectHexagonsCC.x, "y": rectHexagonsCC.y},
        "hexagonSlotSizeY": hexagonSlotSizeY,
    })
    logging.info(f"Thaum controls config successfully saved")


def readJSONConfig(fullpath: str):
    if not os.path.isfile(fullpath):
        logging.warning(f"Config {fullpath} not exists")
        return None
    try:
        with open(fullpath, 'r') as file:
            config = json.load(file)
    except Exception as e:
        logging.critical(f"Something went wrong while opening config {fullpath}: {e}")
        return None
    logging.debug(f"Config {fullpath} successfully loaded")
    return config


def getImagesDiffPercent(image1: Image.Image, image2: Image.Image, masks: list[Image.Image] = []) -> float:
    if image1.size != image2.size:
        raise ValueError("Images sizes must be the same")
    if image1.mode != image2.mode:
        raise ValueError("Image modes must be the same")

    pixels1 = list(image1.getdata())
    pixels2 = list(image2.getdata())
    # for i in range(0, len(pixels1), image1.width):
    #     print(pixels1[i : i + image1.width])
    #     print(pixels2[i : i + image1.width])
    #     print()
    pixelsCount = len(pixels1)

    convertedMasks = []
    for mask in masks:
        if mask.size != image1.size:
            raise ValueError("Images and all masks sizes must be the same")
        grayMask = mask.convert("L")  # convert to grayScale
        convertedMasks.append(list(grayMask.getdata()))
    totalBoolMask = [True] * pixelsCount
    for mask in convertedMasks:
        for i in range(pixelsCount):
            totalBoolMask[i] = totalBoolMask[i] and (mask[i] != 0)

    totalDiff = 0
    activePixelsCount = 0
    pixels = len(pixels1)
    directions = len(pixels1[0])
    diffs = []
    for pixelIdx in range(pixels):
        pixel1 = pixels1[pixelIdx]
        pixel2 = pixels2[pixelIdx]
        if not totalBoolMask[pixelIdx]:
            diffs.append('___')
            continue
        activePixelsCount += 1
        curDiff = 0
        for directionIdx in range(directions):
            curDiff += abs(pixel1[directionIdx] - pixel2[directionIdx])
        totalDiff += curDiff
        diffs.append(str(curDiff).zfill(3))
    percentDiff = totalDiff / (activePixelsCount * directions * 255)

    # for i in range(0, len(pixels1), image1.width):
    # print(diffs[i : i + image1.width])

    return percentDiff


def saveThaumVersionConfig(version: str, addons: list[str]):
    saveJSONConfig(THAUM_VERSION_CONFIG_PATH, {
        'version': version,
        'addons': addons
    })


def loadThaumVersionConfig() -> tuple[str | None, list[str] | None]:
    conf = readJSONConfig(THAUM_VERSION_CONFIG_PATH)
    if conf is None:
        return None, None
    return conf['version'], conf['addons']


def loadRecipesForSelectedVersion() -> dict[str, list[str, str]] | None:
    selectedVersion, selectedAddons = loadThaumVersionConfig()
    allRecipes = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
    if None in (selectedVersion, selectedAddons, allRecipes):
        logging.error(f'Cannot load recipes for selected version. One of selectedVersion, selectedAddons, allRecipes is None: ({selectedVersion}, {selectedAddons}, {allRecipes})')
        return None
    versionRecipes = allRecipes.get(selectedVersion)
    allAddonsRecipes = readJSONConfig(THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH)
    addonsRecipes = {}
    for addonName in selectedAddons:
        addonsRecipes |= allAddonsRecipes.get(addonName, set())
    allRecipes = versionRecipes | addonsRecipes
    return allRecipes


def eventsDelay():
    time.sleep(DELAY_BETWEEN_EVENTS)


def renderDelay():
    time.sleep(DELAY_BETWEEN_RENDER)


def loadImage(
        path: str,
        backgroundImage: Image.Image = None,
        resize: tuple[int, int] | None = None) -> Image.Image:
    image = Image.open(path)
    if resize:
        image = image.resize(resize, Image.Resampling.LANCZOS)
    image = image.convert("RGBA")
    backgroundImage = backgroundImage or Image.new("RGBA", image.size, "BLACK")  # Create a white rgba background
    newImage = backgroundImage.convert("RGBA")
    newImage.paste(image, mask=image)  # Paste the image on the background. Go to the links given below for details.
    result = newImage.convert('RGB')
    logging.debug(f"Loaded image {path}")
    return result
