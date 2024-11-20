import datetime
import json
import random
import time
from multiprocessing import Process

import numpy as np

from PIL import Image, ImageDraw, ImageFont

from src.utils.constants import getAspectImagePath, THAUM_ASPECT_RECIPES_CONFIG_PATH, \
    THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH, THAUM_ASPECTS_INVENTORY_SLOTS_X, THAUM_ASPECTS_INVENTORY_SLOTS_Y
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
    count: int = 0
    hueRotated: float = 0.0

    def __init__(self, name: str, idx: int, count: int = -1, withLighting: bool = False):
        self.name = name
        self.idx = idx
        self.count = count
        self.withLighting = withLighting

    def __repr__(self):
        return f"{self.name}[id={self.idx}]"


GENERATED_IMAGES_COUNT = 10
HEXAGON_FIELD_RADIUS = 2  # 2...4
QUALITY_MODIFIER_MIN = 2 # by default, at value 1, result image is 160x160. You can increase it
QUALITY_MODIFIER_MAX = 7 # by default, at value 1, result image is 160x160. You can increase it
QUALITY_MODIFIER = None # rewritble in code
GET_OUTPUT_IMAGE_NAME = lambda idx: f'./scripts_other/fake_aspects_inventory_generator/output/quality_{QUALITY_MODIFIER}/aspects-all-quality-{QUALITY_MODIFIER}-id-{idx}.png'
GET_COCO_JSON_PATH = lambda: f'./scripts_other/fake_aspects_inventory_generator/output/quality_{QUALITY_MODIFIER}.coco.json'
LOADED_ASPECTS_ADDONS = {"original", "Thaumic Boots", "Avaritia", "GregTech", "Forbidden Magic", "Magic Bees", "GregTech NewHorizons", "Botanical addons", "The Elysium", "Thaumic Revelations", "Essential Thaumaturgy", "AbyssalCraft Integration"} # any addons from aspects config + "original"

BACKGROUND_TABLE_IMAGE_PATH = './scripts_other/fake_aspects_inventory_generator/table_background.png'
LIGHTING_IMAGE_PATH = './scripts_other/fake_aspects_inventory_generator/particle_highlighting.png'
MINECRAFT_FONT_PATH = './scripts_other/fake_aspects_inventory_generator/minecraft.ttf'

GET_TMP_SAVED_IMAGES_PATH = lambda idx: f'./scripts_other/fake_aspects_inventory_generator/tmp-images/tmp-{idx}.png'
FIRST_CELL_COORDS = P(4, 5) # in px. selected according to image's original size
ASPECTS_IMAGES_SIZE = 15.5 # in px. selected according to image's original size


def getResizedImage(image: Image.Image, useOriginals: bool = False, resizeTo: tuple[float | int, float | int] | None = None) -> Image.Image:
    if resizeTo:
        return image.resize((int(resizeTo[0]), int(resizeTo[1])), Image.Resampling.LANCZOS)
    if not useOriginals:
        return image.resize((int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER), int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER)), Image.Resampling.LANCZOS)
    return image.resize((int(image.width * QUALITY_MODIFIER), int(image.height * QUALITY_MODIFIER)), Image.Resampling.LANCZOS)

def loadImage(path: str, backgroundImage: Image.Image = None, noResize: bool = False, size: tuple[float | int, float | int] | None = None, colorMode: str = 'RGBA') -> Image.Image:
    image = Image.open(path)
    image = getResizedImage(image, useOriginals=noResize, resizeTo=size)
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
    return backgroundTableImage

def getCellBoxCoords(cellX, cellY):
    x = FIRST_CELL_COORDS.x + cellX * ASPECTS_IMAGES_SIZE
    y = FIRST_CELL_COORDS.y + cellY * ASPECTS_IMAGES_SIZE
    x *= QUALITY_MODIFIER
    y *= QUALITY_MODIFIER
    return int(x), int(y), int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER), int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER)

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

def drawTextOnImage(image: Image, text: str, posRB: P, font_size: float, font_path: str, font_color:tuple[int, int, int]):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, size=int(font_size * 0.76))
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    draw.text((posRB.x - w - 0.12 * font_size, posRB.y - h), text, font=font, fill=(0, 0, 0))
    draw.text((posRB.x - w, posRB.y - h - 0.12 * font_size), text, font=font, fill=(0, 0, 0))
    draw.text((posRB.x - w + 0.12 * font_size, posRB.y - h), text, font=font, fill=(0, 0, 0))
    draw.text((posRB.x - w, posRB.y - h + 0.12 * font_size), text, font=font, fill=(0, 0, 0))

    draw.text((posRB.x - w, posRB.y - h), text, font=font, fill=font_color)
    return (posRB.x - w - 0.12 * font_size, posRB.y - h - 0.12 * font_size, w + 0.24 * font_size, h + 0.24 * font_size)

def main(quality_modifier, generated_images_count):
    global GENERATED_IMAGES_COUNT, QUALITY_MODIFIER
    GENERATED_IMAGES_COUNT = generated_images_count
    QUALITY_MODIFIER = quality_modifier

    allAspects = []

    cocoJsonCategories = []
    cocoJsonImages = []
    cocoJsonAnnotations = []

    # add unknown aspect category
    cocoJsonCategories.append({
        "id": 0,
        "name": "unknown",
        "supercategory": "none",
    })
    for i in range(0, 10):
        cocoJsonCategories.append({
            "id": 1 + i,
            "name": str(i),
            "supercategory": "none",
        })

    def addAspectToAllAspects(aspectName):
        # check if aspect already in list
        for aspect in allAspects:
            if aspect.name == aspectName:
                return

        # aspect not in list
        aspectId = len(cocoJsonCategories)
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

    # load aspect highlighting image
    aspectHighlightingImage = loadImage(LIGHTING_IMAGE_PATH, size=(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER * 1.4, ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER * 1.4))
    modifyImageChannels(aspectHighlightingImage, [3], 2)
    modifyImageChannels(aspectHighlightingImage, [0,1,2], 1.5)
    aspectHighlightingImage = getJackaledImage(aspectHighlightingImage, 2)
    hueRotate(aspectHighlightingImage, 100)
    print("Aspects highlighting image loaded")


    def generateImage(currentImageAnnotationId):
        # generate all cells with aspects
        availableAspects = allAspects.copy()
        cells: dict[P, Aspect|None] = {}
        for x in range(THAUM_ASPECTS_INVENTORY_SLOTS_X):
            for y in range(THAUM_ASPECTS_INVENTORY_SLOTS_Y):
                # known or unknown aspect
                if random.random() < 0.04:
                    aspect = Aspect("UNKNOWN", 0)
                    aspectColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
                    aspect.image = Image.new("RGBA", (int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER), int(ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER)), aspectColor)
                else:
                    aspect = random.choice(availableAspects)
                # aspect highlighting
                aspect.withLighting = (random.random() < 0.2)
                # aspect count
                aspect.count = 0
                v = random.random()
                if v > 0.6:
                    aspect.count = random.randint(100, 999)
                elif v > 0.15:
                    aspect.count = random.randint(10, 99)
                else:
                    aspect.count = random.randint(1, 9)
                # put aspect to cell
                cells[P(x, y)] = aspect
                if aspect.idx != 0:
                    availableAspects.remove(aspect)

        # generate random none cells
        noneCellsCount = random.randint(0, 7)
        aspectWithEmptyImage = Aspect("_EMPTY_", 0)
        aspectWithEmptyImage.image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        for i in range(noneCellsCount):
            point = random.choice(list(cells.keys()))
            cells[point] = aspectWithEmptyImage

        # draw aspects on field by gotten cells and fill coco json
        resultImage = backgroundImage.copy()
        for point in cells.keys():
            aspect = cells[point]
            cellBoxCoords = getCellBoxCoords(point.x, point.y)
            if aspect is None:
                continue
            # rotate hue for tincturem
            aspectImage = aspect.image
            if aspect.name == 'tincturem':
                aspect.hueRotated += 0.08
                aspectImage = hueRotate(aspect.image, aspect.hueRotated)
            if aspect.count == 0: # 0 count aspect. Needs to apply lower opacity
                print(aspect)
                aspectImage = aspectImage.copy()
                modifyImageChannels(aspectImage, [3], 0.4)
            # paste aspect image on field
            pasteImageWithOpacity(resultImage, aspectImage, box=(cellBoxCoords[0], cellBoxCoords[1]))
            # paste aspect highlighting image
            if aspect.withLighting:
                pasteImageWithOpacity(resultImage, aspectHighlightingImage.rotate(random.randint(0, 360)), box=(int(cellBoxCoords[0] - cellBoxCoords[2] * 0.5), int(cellBoxCoords[1] - cellBoxCoords[3] * 0.5)))
            # paste aspect text count
            if aspect.count > 0:
                charPosRB = P(cellBoxCoords[0] + cellBoxCoords[2], cellBoxCoords[1] + cellBoxCoords[3])
                for char in str(aspect.count)[::-1]:
                    fontSize = ASPECTS_IMAGES_SIZE * QUALITY_MODIFIER * 0.35
                    charBoundingBox = drawTextOnImage(resultImage, char, charPosRB, fontSize, MINECRAFT_FONT_PATH, (255, 255, 255))
                    charPosRB.x = charBoundingBox[0] + fontSize * 0.12
                    cocoJsonAnnotations.append({
                        "id": len(cocoJsonAnnotations),
                        "image_id": currentImageAnnotationId,
                        "category_id": int(char) + 1,
                        "bbox": list(charBoundingBox),
                        "area": charBoundingBox[2] * charBoundingBox[3],
                        "segmentation": [],
                        "iscrowd": 0
                    })
            # write to coco json
            if aspect.idx >= 1: # it's aspect, not empty cell
                cocoJsonAnnotations.append({
                    "id": len(cocoJsonAnnotations),
                    "image_id": currentImageAnnotationId,
                    "category_id": aspect.idx,
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
    for quality_modifier in range(QUALITY_MODIFIER_MIN, QUALITY_MODIFIER_MAX):
        QUALITY_MODIFIER = quality_modifier
        print(f"Started new process with (quality={quality_modifier}, images_count={GENERATED_IMAGES_COUNT})")
        process = Process(target=main, args=(quality_modifier, GENERATED_IMAGES_COUNT), daemon=True)
        processes.add(process)
        process.start()
        print()
        print("------------------------------------------------------------")
        print(f"GENERATED ALL IMAGES WITH (quality={quality_modifier}, images_count={GENERATED_IMAGES_COUNT})")
        print("------------------------------------------------------------")
        print()
    print(f"Started {len(processes)} processes")


    for process in processes:
        process.join()
        print(f"Process joined")
    print(f"All processes joined")


    print("--- Time execution: %s seconds ---" % (time.time() - start_time))
