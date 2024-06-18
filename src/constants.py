THAUM_VERSION = '4.1.1.14'

# UI and visual part
MARGIN = 20
FPS = 60

# Files names
THAUM_VERSION_CONFIG_PATH = 'configs/thaumVersionConfig.json'
THAUM_CONTROLS_CONFIG_PATH = 'configs/thaumControlsConfig.json'
THAUM_ASPECT_RECIPES_CONFIG_PATH = 'configs/aspectsRecipes.json'
THAUM_TRANSLATION_CONFIG_PATH = 'configs/translationDictionary.json'
def getAspectImagePath(aspectName, color=True):
    return f"images/{'color' if color else 'mono'}/{aspectName}.png"
def getImagePathByNumber(number):
    return f"images/numbers/{number}.png"
EMPTY_ASPECT_SLOT_IMAGE_PATH = 'images/emptyAspectPlace.png'
HEXAGON_MASK_IMAGE_PATH = 'images/hexagons/hexagonMask.png'
HEXAGON_BORDER_MASK_IMAGE_PATH = 'images/hexagons/hexagonBorderMask.png'
MASK_WITHOUT_NUMBER_IMAGE_PATH = 'images/maskWithoutNumbers.png'
MASK_ONLY_NUMBER_IMAGE_PATH = 'images/maskOnlyNumbers.png'
NONE_HEXAGON_SLOT_IMAGE_PATH = 'images/hexagons/noneHexagon.png'
FREE_HEXAGON_SLOT_IMAGES_PATHS = [
    'images/hexagons/freeHexagons/1.png',
    'images/hexagons/freeHexagons/2.png',
    'images/hexagons/freeHexagons/3.png',
    'images/hexagons/freeHexagons/4.png',
    'images/hexagons/freeHexagons/5.png',
    'images/hexagons/freeHexagons/6.png',
    'images/hexagons/freeHexagons/7.png',
]
ASPECTS_IMAGES_SIZE = 32  # px
ASPECT_COUNT_NUMBER_SIZE = (6, 10)  # px

# In-game inventory
# !!! Don't touch if you not sure !!!
INVENTORY_SLOTS_X = 9
INVENTORY_SLOTS_Y = 3

THAUM_ASPECTS_INVENTORY_SLOTS_X = 5
THAUM_ASPECTS_INVENTORY_SLOTS_Y = 5

THAUM_HEXAGONS_SLOTS_COUNT = 9  # must be odd

# DELAY_BETWEEN_EVENTS = 0.1  # secs
DELAY_BETWEEN_EVENTS = 0.5  # secs
# DELAY_BETWEEN_RENDER = 0.5  # secs
DELAY_BETWEEN_RENDER = 1.4  # secs

EMPTY_TOLERANCE_PERCENT = 0.02

DEBUG = True
