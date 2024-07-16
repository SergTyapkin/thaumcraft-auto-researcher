import math
import random

from PIL import Image

from utils.constants import getAspectImagePath, THAUM_ASPECT_RECIPES_CONFIG_PATH, \
    THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH
from utils.utils import readJSONConfig, createDirByFilePath


class P:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"

class Aspect:
    idx: int = None
    name: str = None
    image: Image.Image = None
    withLighting: bool = False

    def __init__(self, name: str, idx: int, withLighting: bool = False):
        self.name = name
        self.idx = idx
        self.withLighting = withLighting

    def __repr__(self):
        return f"{self.name}[id={self.idx}]"


HEXAGON_FIELD_RADIUS = 4  # 2...4
GENERATED_IMAGES_COUNT = 334
QUALITY_MODIFIER = 2 # by default, at value 1, result image is 256x256. You can increase it
EMPTY_HEXAGON_PATH = './scripts_other/fake_researches_generator/empty_hexagon.png'
BACKGROUND_TABLE_IMAGE_PATH = './scripts_other/fake_researches_generator/table_background.png'
BACKGROUND_TABLE_PAPER_IMAGE_PATH = './scripts_other/fake_researches_generator/table_background_paper.png'
LIGHTING_IMAGE_PATH = './scripts_other/fake_researches_generator/lighting_large.png'
SCRIPTS_IMAGE_PATH = './scripts_other/fake_researches_generator/scripts.png'
GET_TMP_SAVED_IMAGES_PATH = lambda idx: f'./scripts_other/fake_researches_generator/tmp-{idx}.png'
CENTER_CELL_COORDS = P(72, 72) # in px. selected according to image's original size
HEXAGON_SLOT_SIZE_Y = 15.5 # in px. selected according to image's original size
HEXAGON_SLOT_SIZE_X = HEXAGON_SLOT_SIZE_Y * math.cos(math.pi / 6)
ASPECTS_IMAGES_SIZE = HEXAGON_SLOT_SIZE_Y
GET_OUTPUT_IMAGE_NAME = lambda idx: f'./scripts_other/fake_researches_generator/output/aspects-addons-rad-{HEXAGON_FIELD_RADIUS}-id-{idx}.png'
LOADED_ASPECTS_ADDONS = {"Thaumic Boots", "GTNH (2.1.3.0+)", "Avaritia", "GregTech", "Forbidden Magic", "Magic Bees"} # any from aspects config + "original"



def getResizedImage(image: Image.Image, useOriginals: bool = False, resizeTo: tuple[float | int, float | int] | None = None) -> Image.Image:
    if resizeTo:
        return image.resize((int(resizeTo[0]), int(resizeTo[1])), Image.Resampling.LANCZOS)
    if not useOriginals:
        return image.resize((int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER), int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER)), Image.Resampling.LANCZOS)
    return image.resize((int(image.width * QUALITY_MODIFIER), int(image.height * QUALITY_MODIFIER)), Image.Resampling.LANCZOS)

def loadImage(path: str, backgroundImage: Image.Image = None, noResize: bool = False) -> Image.Image:
    image = Image.open(path)
    image = getResizedImage(image, useOriginals=noResize)
    image = image.convert("RGBA")
    if backgroundImage is not None:
        backgroundImage = backgroundImage or Image.new("RGBA", image.size, "BLACK")  # Create a white rgba background
        newImage = backgroundImage.convert("RGBA")
        newImage.paste(image, mask=image)  # Paste the image on the background. Go to the links given below for details.
        image = newImage.convert('RGB')
    print(f"Loaded image {path}")
    return image

def loadAspectsImages(allAspects):
    print(f"Loading thaum aspects images...")
    for aspect in allAspects:
        aspect.image = loadImage(getAspectImagePath(aspect.name))
        aspect.mask = Image.open(getAspectImagePath(aspect.name, colored=False)).convert("L")

_imageIdx = 0
def saveImage(image: Image.Image):
    global _imageIdx
    image.save(GET_TMP_SAVED_IMAGES_PATH(_imageIdx))
    _imageIdx += 1

def loadBackgroundImage() -> Image.Image:
    backgroundTableImage = loadImage(BACKGROUND_TABLE_IMAGE_PATH, noResize=True)
    backgroundTablePaperImage = loadImage(BACKGROUND_TABLE_PAPER_IMAGE_PATH, noResize=True)
    pasteImageWithOpacity(backgroundTableImage, backgroundTablePaperImage, box=(int(4 * QUALITY_MODIFIER), int(5 * QUALITY_MODIFIER)))
    return backgroundTableImage

def getCellBoxCoords(cellX, cellY):
    x = CENTER_CELL_COORDS.x + HEXAGON_SLOT_SIZE_X * cellX
    y = CENTER_CELL_COORDS.y + HEXAGON_SLOT_SIZE_Y * cellY - (cellX % 2) * (HEXAGON_SLOT_SIZE_Y / 2)
    x *= QUALITY_MODIFIER
    y *= QUALITY_MODIFIER
    return int(x), int(y), int(HEXAGON_SLOT_SIZE_Y * QUALITY_MODIFIER), int(HEXAGON_SLOT_SIZE_Y * QUALITY_MODIFIER)

def modifyImageChannels(image: Image.Image, channelIndexes: tuple[int] | list[int], multiplier: float):
    for x in range(image.width):
        for y in range(image.height):
            pixel = list(image.getpixel((x, y)))
            for channelIdx in channelIndexes:
                pixel[channelIdx] = min(int(pixel[channelIdx] * multiplier), 255)
            image.putpixel((x, y), tuple(pixel))

def pasteImageWithOpacity(backgroundImage: Image.Image, overlayImage: Image.Image, box: tuple[int, int] | tuple[int, int, int, int]):
    newImage = Image.new("RGBA", size=backgroundImage.size, color=(0, 0, 0, 0))
    newImage.paste(overlayImage, box=box, mask=overlayImage)
    backgroundImage.alpha_composite(newImage)


def getJackaledImage(image: Image.Image, multiplier: float = 2):
    imageSize = image.size
    newImage = getResizedImage(image, resizeTo=(int(imageSize[0] / multiplier), int(imageSize[1] / multiplier)))
    newImage = getResizedImage(newImage, resizeTo=imageSize)
    return newImage

def invertImageChannels(image: Image.Image, channelIndexes: tuple[int] | list[int]):
    for x in range(image.width):
        for y in range(image.height):
            pixel = list(image.getpixel((x, y)))
            for channelIdx in channelIndexes:
                pixel[channelIdx] = 255 - pixel[channelIdx]
            image.putpixel((x, y), tuple(pixel))

def getResizedInCenterTransparentImage(image: Image.Image, sizeModifier: float):
    backgroundImage = Image.new("RGBA", image.size, (0, 0, 0, 0))
    newSize = (int(image.width / sizeModifier), int(image.height / sizeModifier))
    smallImage = getResizedImage(image, resizeTo=newSize)
    pasteImageWithOpacity(backgroundImage, smallImage, box=((image.size[0]-newSize[0]) // 2, (image.size[1]-newSize[1]) // 2))
    resultImage = getResizedImage(backgroundImage, resizeTo=(int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER), int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER)))
    return resultImage


if __name__ == '__main__':
    allAspects = set()

    # load aspects
    if "original" in LOADED_ASPECTS_ADDONS:
        allRecipes = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
        for (version, recipes) in allRecipes.items():
            for aspectName in recipes.keys():
                allAspects.add(Aspect(aspectName, len(allAspects)))

    # load addons aspects
    allAddonsRecipes = readJSONConfig(THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH)
    for (addon, recipes) in allAddonsRecipes.items():
        if addon not in LOADED_ASPECTS_ADDONS:
            continue
        for aspectName in recipes.keys():
            allAspects.add(Aspect(aspectName, len(allAspects)))
    allAspects = list(allAspects)

    # load aspects images
    loadAspectsImages(allAspects)
    for aspect in allAspects:
        aspect.image = getResizedInCenterTransparentImage(aspect.image, 1)
        aspect.image = getJackaledImage(aspect.image, 1.7)

    # load background image
    backgroundImage = loadBackgroundImage()

    # load empty hexagon image
    emptyHexagonImage = loadImage(EMPTY_HEXAGON_PATH)
    emptyHexagonImage = getJackaledImage(emptyHexagonImage, 2)
    # imageResize(emptyHexagonImage, resizeTo=imageSize)
    modifyImageChannels(emptyHexagonImage, [3], 0.65)

    # load aspect highlighting image
    aspectHighlightingImage = loadImage(LIGHTING_IMAGE_PATH)
    aspectHighlightingImage = getJackaledImage(aspectHighlightingImage, 2)
    modifyImageChannels(aspectHighlightingImage, [3], 0.85)

    # load scripts images. Split by sprites
    scriptsSpriteImage = loadImage(SCRIPTS_IMAGE_PATH, noResize=True)
    scriptsSpriteImage = getResizedImage(scriptsSpriteImage, resizeTo=(int(scriptsSpriteImage.width * QUALITY_MODIFIER), int(scriptsSpriteImage.height * QUALITY_MODIFIER)))
    invertImageChannels(scriptsSpriteImage, [0, 1, 2])
    modifyImageChannels(scriptsSpriteImage, [3], 2)
    modifyImageChannels(scriptsSpriteImage, [3], 0.7)
    scriptSizePx = scriptsSpriteImage.height
    scriptsImageAspects = []
    for fromX in range(0, scriptsSpriteImage.width, scriptSizePx):
        scriptImageBig = scriptsSpriteImage.crop((fromX, 0, fromX + scriptSizePx, scriptSizePx))
        scriptImage = getResizedInCenterTransparentImage(scriptImageBig, sizeModifier=1.5)
        scriptImage = getJackaledImage(scriptImage, 1.7)

        scriptAspect = Aspect("_SCRIPT_", -2)
        scriptAspect.image = scriptImage
        scriptsImageAspects.append(scriptAspect)

    def generateImage():
        # generate all cells
        cells: dict[P, Aspect|None] = {}
        for x in range(-HEXAGON_FIELD_RADIUS, HEXAGON_FIELD_RADIUS + 1):
            for y in range(-HEXAGON_FIELD_RADIUS + (abs(x) + 1) // 2, HEXAGON_FIELD_RADIUS - (abs(x)) // 2 + 1):
                cells[P(x, y)] = None

        # generate random none cells
        noneCellsCount = random.randint(HEXAGON_FIELD_RADIUS, HEXAGON_FIELD_RADIUS*3)
        aspectWithEmptyImage = Aspect("_EMPTY_", -1)
        aspectWithEmptyImage.image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        for i in range(noneCellsCount):
            point = random.choice(list(cells.keys()))
            if random.random() < 0.5:
                cells[point] = random.choice(scriptsImageAspects)
            else:
                cells[point] = aspectWithEmptyImage

        # write aspects to random cells
        aspectsOnFieldCount = random.randint(HEXAGON_FIELD_RADIUS, HEXAGON_FIELD_RADIUS*3)
        aspectsLeft = allAspects.copy()
        for i in range(aspectsOnFieldCount):
            # select available points to set aspect on them
            availablePoints = []
            for (point, aspect) in cells.items():
                if aspect is None:
                    availablePoints.append(point)
            # set aspect on one of them
            point = random.choice(availablePoints)
            aspect = random.choice(aspectsLeft)
            aspect.withLighting = (random.random() < 0.3)
            cells[point] = aspect
            aspectsLeft.remove(aspect)

        # draw aspects on field by gotten cells
        resultImage = backgroundImage.copy()
        for point in cells.keys():
            aspect = cells[point]
            cellBoxCoords = getCellBoxCoords(point.x, point.y)
            if aspect is not None:
                if aspect.withLighting:
                    pasteImageWithOpacity(resultImage, aspectHighlightingImage, box=(cellBoxCoords[0], cellBoxCoords[1]))
                pasteImageWithOpacity(resultImage, aspect.image, box=(cellBoxCoords[0], cellBoxCoords[1]))
                # print(aspect, "TO:", cellBoxCoords)
            else:
                pasteImageWithOpacity(resultImage, emptyHexagonImage, box=(cellBoxCoords[0], cellBoxCoords[1]))
        return resultImage

    # generate images and save
    createDirByFilePath(GET_OUTPUT_IMAGE_NAME(0))
    for i in range(GENERATED_IMAGES_COUNT):
        pathToSave = GET_OUTPUT_IMAGE_NAME(i)
        generateImage().save(pathToSave)
        print("Output image saved to", pathToSave)
