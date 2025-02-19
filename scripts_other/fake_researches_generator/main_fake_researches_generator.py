import datetime
import json
import math
import random
import time
from multiprocessing import Process

import numpy as np

from PIL import Image

from src.utils.constants import getAspectImagePath, THAUM_ASPECT_RECIPES_CONFIG_PATH, \
    THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH
from src.utils.utils import readJSONConfig, createDirByFilePath


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
    mask: Image.Image = None
    withLighting: bool = False
    hueRotated: float = 0.0

    def __init__(self, name: str, idx: int, withLighting: bool = False):
        self.name = name
        self.idx = idx
        self.withLighting = withLighting

    def __repr__(self):
        return f"{self.name}[id={self.idx}]"


GENERATED_IMAGES_COUNT = 100
HEXAGON_FIELD_RADIUS = 2  # 2...4
QUALITY_MODIFIER = 2 # by default, at value 1, result image is 160x160. You can increase it
GET_OUTPUT_IMAGE_NAME = lambda idx: f'./scripts_other/fake_researches_generator/output/all_aspects_rad_{HEXAGON_FIELD_RADIUS}_quality_{QUALITY_MODIFIER}/aspects-all-rad-{HEXAGON_FIELD_RADIUS}-quality-{QUALITY_MODIFIER}-id-{idx}.png'
GET_COCO_JSON_PATH = lambda: f'./scripts_other/fake_researches_generator/output/all_aspects_rad_{HEXAGON_FIELD_RADIUS}_quality_{QUALITY_MODIFIER}.coco.json'
LOADED_ASPECTS_ADDONS = {"original", "Thaumic Boots", "Avaritia", "GregTech", "Forbidden Magic", "Magic Bees", "GregTech NewHorizons", "Botanical addons", "The Elysium", "Thaumic Revelations", "Essential Thaumaturgy", "AbyssalCraft Integration"} # any addons from aspects config + "original"

EMPTY_HEXAGON_PATH = './scripts_other/fake_researches_generator/empty_hexagon.png'
BACKGROUND_TABLE_IMAGE_PATH = './scripts_other/fake_researches_generator/table_background.png'
BACKGROUND_TABLE_PAPER_IMAGE_PATH = './scripts_other/fake_researches_generator/table_background_paper.png'
LIGHTING_IMAGE_PATH = './scripts_other/fake_researches_generator/lighting_large.png'
SCRIPTS_IMAGE_PATH = './scripts_other/fake_researches_generator/scripts.png'

GET_TMP_SAVED_IMAGES_PATH = lambda idx: f'./scripts_other/fake_researches_generator/tmp-images/tmp-{idx}.png'
CENTER_CELL_COORDS = P(72, 72) # in px. selected according to image's original size
HEXAGON_SLOT_SIZE_Y = 15.5 # in px. selected according to image's original size
HEXAGON_SLOT_SIZE_X = HEXAGON_SLOT_SIZE_Y * math.cos(math.pi / 6)
ASPECTS_IMAGES_SIZE = HEXAGON_SLOT_SIZE_Y


def getResizedImage(image: Image.Image, useOriginals: bool = False, resizeTo: tuple[float | int, float | int] | None = None) -> Image.Image:
    if resizeTo:
        return image.resize((int(resizeTo[0]), int(resizeTo[1])), Image.Resampling.LANCZOS)
    if not useOriginals:
        return image.resize((int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER), int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER)), Image.Resampling.LANCZOS)
    return image.resize((int(image.width * QUALITY_MODIFIER), int(image.height * QUALITY_MODIFIER)), Image.Resampling.LANCZOS)

def loadImage(path: str, backgroundImage: Image.Image = None, noResize: bool = False, colorMode: str = 'RGBA') -> Image.Image:
    image = Image.open(path)
    image = getResizedImage(image, useOriginals=noResize)
    image = image.convert(colorMode)
    if backgroundImage is not None:
        backgroundImage = backgroundImage or Image.new(colorMode, image.size, "BLACK")  # Create a white rgba background
        newImage = backgroundImage.convert(colorMode)
        newImage.paste(image, mask=image)  # Paste the image on the background. Go to the links given below for details.
        image = newImage.convert(colorMode)
    print(f"Loaded image {path}")
    return image

def loadAspectsImages(allAspects):
    print(f"Loading thaum aspects images...")
    for aspect in allAspects:
        aspect.image = loadImage(getAspectImagePath(aspect.name))
        aspect.mask = loadImage(getAspectImagePath(aspect.name, colored=False))

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

def modifyImageChannels(image: Image.Image, channelIndexes: tuple[int] | list[int], multiplier: float = 1, addition: int = 0):
    for x in range(image.width):
        for y in range(image.height):
            pixel = list(image.getpixel((x, y)))
            for channelIdx in channelIndexes:
                pixel[channelIdx] = min(int(pixel[channelIdx] * multiplier + (0 if (channelIdx == 3 and pixel[channelIdx] == 0) else addition)), 255)
            image.putpixel((x, y), tuple(pixel))

def pasteImageWithOpacity(backgroundImage: Image.Image, overlayImage: Image.Image, box: tuple[int, int] | tuple[int, int, int, int], mask: Image.Image = None):
    newImage = Image.new("RGBA", size=backgroundImage.size, color=(0, 0, 0, 0))
    newImage.paste(overlayImage, box=box, mask=mask)
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

def getResizedInCenterTransparentImage(image: Image.Image, sizeModifier: float, addImages: [Image.Image] = []):
    backgroundImage = Image.new("RGBA", image.size, (0, 0, 0, 0))
    newSize = (int(image.width / sizeModifier), int(image.height / sizeModifier))
    smallImage = getResizedImage(image, resizeTo=newSize)
    pasteBoxCoords = ((image.size[0]-newSize[0]) // 2, (image.size[1]-newSize[1]) // 2)
    pasteImageWithOpacity(backgroundImage, smallImage, box=pasteBoxCoords)
    for addImage in addImages:
        addImageResized = getResizedImage(addImage, resizeTo=newSize)
        pasteImageWithOpacity(backgroundImage, addImageResized, box=pasteBoxCoords)
    backgroundImage = getResizedImage(backgroundImage, resizeTo=(int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER), int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER)))
    return backgroundImage

def rgbToHsv(rgb):
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv

def hsvToRgb(hsv):
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')

def hueRotate(img, hout):
    hsv = rgbToHsv(np.array(img))
    hsv[..., 0] = hout
    rgb = hsvToRgb(hsv)
    return Image.fromarray(rgb, 'RGBA')


def main(hexagon_field_radius, quality_modifier, generated_images_count):
    global HEXAGON_FIELD_RADIUS, GENERATED_IMAGES_COUNT, QUALITY_MODIFIER
    HEXAGON_FIELD_RADIUS = hexagon_field_radius
    GENERATED_IMAGES_COUNT = generated_images_count
    QUALITY_MODIFIER = quality_modifier

    allAspects = []

    cocoJsonCategories = []
    cocoJsonImages = []
    cocoJsonAnnotations = []

    # add free hexagon category
    cocoJsonCategories.append({
        "id": 0,
        "name": "free_hex",
        "supercategory": "none",
    })
    # add script category
    cocoJsonCategories.append({
        "id": 1,
        "name": "script",
        "supercategory": "none",
    })

    def addAspectToAllAspects(aspectName):
        # check if aspect already in list
        for aspect in allAspects:
            if aspect.name == aspectName:
                return

        # aspect not in list
        aspectId = len(allAspects) + 2
        allAspects.append(Aspect(aspectName, aspectId))
        cocoJsonCategories.append({
            "id": aspectId,
            "name": aspectName,
            "supercategory": "none",
        })
    # load aspects and fill them in coco categories
    if "original" in LOADED_ASPECTS_ADDONS:
        allRecipes = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
        for (version, recipes) in allRecipes.items():
            for aspectName in recipes.keys():
                addAspectToAllAspects(aspectName)
    print("Original aspects list loaded")

    # load addons aspects
    allAddonsRecipes = readJSONConfig(THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH)
    for (addon, recipes) in allAddonsRecipes.items():
        if addon not in LOADED_ASPECTS_ADDONS:
            continue
        for aspectName in recipes.keys():
            addAspectToAllAspects(aspectName)
    print("Addons aspects list loaded")

    # load aspects images
    loadAspectsImages(allAspects)
    for aspect in allAspects:
        aspect.image = getResizedInCenterTransparentImage(aspect.image, 1)#, addImages=[aspect.mask])
        aspect.image = getJackaledImage(aspect.image, 1.7 - 0.1 * QUALITY_MODIFIER)
    print("Aspects images loaded")

    # load background image
    backgroundImage = loadBackgroundImage()
    print("Background image loaded")

    # load empty hexagon image
    emptyHexagonImage = loadImage(EMPTY_HEXAGON_PATH)
    emptyHexagonImage = getJackaledImage(emptyHexagonImage, 1 + 0.5 * QUALITY_MODIFIER)
    modifyImageChannels(emptyHexagonImage, [3], 0.3)
    print("Empty hexagon image loaded")

    # load aspect highlighting image
    aspectHighlightingImage = loadImage(LIGHTING_IMAGE_PATH)
    aspectHighlightingImage = getJackaledImage(aspectHighlightingImage, 2)
    modifyImageChannels(aspectHighlightingImage, [3], 0.5)
    print("Aspects highlighting image loaded")

    # load scripts images. Split by sprites
    scriptsSpriteImage = loadImage(SCRIPTS_IMAGE_PATH, noResize=True)
    scriptsSpriteImage = getResizedImage(scriptsSpriteImage, resizeTo=(int(scriptsSpriteImage.width * QUALITY_MODIFIER), int(scriptsSpriteImage.height * QUALITY_MODIFIER)))
    print("Inverting scripts...")
    invertImageChannels(scriptsSpriteImage, [0, 1, 2])
    print("Opacity modifying scripts...")
    modifyImageChannels(scriptsSpriteImage, [3], 0.4)
    scriptSizePx = scriptsSpriteImage.height
    scriptsImageAspects = []
    for fromX in range(0, scriptsSpriteImage.width, scriptSizePx):
        scriptImageBig = scriptsSpriteImage.crop((fromX, 0, fromX + scriptSizePx, scriptSizePx))
        scriptImage = getResizedInCenterTransparentImage(scriptImageBig, sizeModifier=1.5)
        scriptImage = getJackaledImage(scriptImage, 1.7)

        scriptAspect = Aspect("_SCRIPT_", 1)
        scriptAspect.image = scriptImage
        scriptsImageAspects.append(scriptAspect)
        print(f"Script image {len(scriptsImageAspects)} loaded")
    print("Scripts images loaded")


    def generateImage(currentImageAnnotationId):
        # generate all cells
        cells: dict[P, Aspect|None] = {}
        for x in range(-HEXAGON_FIELD_RADIUS, HEXAGON_FIELD_RADIUS + 1):
            for y in range(-HEXAGON_FIELD_RADIUS + (abs(x) + 1) // 2, HEXAGON_FIELD_RADIUS - (abs(x)) // 2 + 1):
                cells[P(x, y)] = None

        # generate random none cells
        noneCellsCount = random.randint(HEXAGON_FIELD_RADIUS, HEXAGON_FIELD_RADIUS*3)
        aspectWithEmptyImage = Aspect("_EMPTY_", 0)
        aspectWithEmptyImage.image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        for i in range(noneCellsCount):
            point = random.choice(list(cells.keys()))
            if random.random() < 0.5:
                cells[point] = random.choice(scriptsImageAspects)
            else:
                cells[point] = aspectWithEmptyImage

        # write aspects to random cells
        aspectsOnFieldCount = random.randint(HEXAGON_FIELD_RADIUS*2, HEXAGON_FIELD_RADIUS*4)
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

        # draw aspects on field by gotten cells and fill coco json
        resultImage = backgroundImage.copy()
        for point in cells.keys():
            aspect = cells[point]
            cellBoxCoords = getCellBoxCoords(point.x, point.y)
            if aspect is not None:
                if aspect.withLighting:
                    pasteImageWithOpacity(resultImage, aspectHighlightingImage, box=(cellBoxCoords[0], cellBoxCoords[1]))
                # rotate hue for tincturem
                aspectImage = aspect.image
                if aspect.name == 'tincturem':
                    aspect.hueRotated += 0.08
                    aspectImage = hueRotate(aspect.image, aspect.hueRotated)
                if aspect.idx == 1: # script. Needs to apply random opacity [0.6 ... 1]
                    aspectImage = aspectImage.copy()
                    modifyImageChannels(aspectImage, [3], 0.6 + random.random() * 0.4)
                # paste aspect image on field
                pasteImageWithOpacity(resultImage, aspectImage, box=(cellBoxCoords[0], cellBoxCoords[1]))
                # write to coco json
                if aspect.idx >= 1: # it's aspect or script, not empty cell
                    cocoJsonAnnotations.append({
                        "id": len(cocoJsonAnnotations),
                        "image_id": currentImageAnnotationId,
                        "category_id": aspect.idx,
                        "bbox": list(cellBoxCoords),
                        "area": cellBoxCoords[2] * cellBoxCoords[3],
                        "segmentation": [],
                        "iscrowd": 0
                    })
            else:
                pasteImageWithOpacity(resultImage, emptyHexagonImage, box=(cellBoxCoords[0], cellBoxCoords[1]))
                # write to coco
                cocoJsonAnnotations.append({
                    "id": len(cocoJsonAnnotations),
                    "image_id": currentImageAnnotationId,
                    "category_id": 0,
                    "bbox": list(cellBoxCoords),
                    "area": cellBoxCoords[2] * cellBoxCoords[3],
                    "segmentation": [],
                    "iscrowd": 0
                })
        return resultImage

    # generate images and save
    createDirByFilePath(GET_OUTPUT_IMAGE_NAME(0))
    for i in range(GENERATED_IMAGES_COUNT):
        pathToSave = GET_OUTPUT_IMAGE_NAME(i)
        fileName = pathToSave.split('/')[-1]
        image = generateImage(i)
        cocoJsonImages.append({
            "id": i,
            "license": 1,
            "file_name": fileName,
            "height": image.height,
            "width": image.width,
            "date_captured": str(datetime.datetime.now()),
        })
        image.save(pathToSave)
        print("Output image saved to", pathToSave)

    # save coco json
    createDirByFilePath(GET_COCO_JSON_PATH())
    with open(GET_COCO_JSON_PATH(), "w") as cocoFile:
        cocoFile.write(json.dumps({
            "info": {
                "year": "2024",
                "version": "1",
                "description": "Thaumcraft images for TaumcraftAutoResearcher project",
                "contributor": "Tyapkin Sergey",
                "url": "",
                "date_created": str(datetime.datetime.now())
            },
            "licenses": [
                {
                    "id": 1,
                    "url": "https://mit-license.org/",
                    "name": "MIT"
                }
            ],
            "categories": cocoJsonCategories,
            "images": cocoJsonImages,
            "annotations": cocoJsonAnnotations,
        }, indent="  "))
        print("COCO json file saved to ", GET_COCO_JSON_PATH())

if __name__ == '__main__':
    start_time = time.time()

    processes = set()
    for quality_modifier in range(2, 7, 1):
        for hexagon_field_radius in range(2, 5, 1):
            print(f"Started new process with (quality={quality_modifier}, radius={hexagon_field_radius}, images_count={GENERATED_IMAGES_COUNT})")
            process = Process(target=main, args=(hexagon_field_radius, quality_modifier, GENERATED_IMAGES_COUNT), daemon=True)
            processes.add(process)
            process.start()
            print()
            print("------------------------------------------------------------")
            print(f"GENERATED ALL IMAGES WITH (quality={quality_modifier}, radius={hexagon_field_radius}, images_count={GENERATED_IMAGES_COUNT})")
            print("------------------------------------------------------------")
            print()
    print(f"Started {len(processes)} processes")


    for process in processes:
        process.join()
        print(f"Process joined")
    print(f"All processes joined")


    print("--- Time execution: %s seconds ---" % (time.time() - start_time))
