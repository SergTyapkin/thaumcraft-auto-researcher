import os
import sys

THAUM_VERSION = '4.1.1.14'

# UI and visual part
MARGIN = 20
FPS = 60


# Files paths
def to_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


THAUM_VERSION_CONFIG_PATH = to_resource_path('user_configs/thaumVersionConfig.json')
THAUM_CONTROLS_CONFIG_PATH = to_resource_path('user_configs/thaumControlsConfig.json')
THAUM_ASPECT_RECIPES_CONFIG_PATH = to_resource_path('aspects_configs/aspectsRecipes.json')
THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH = to_resource_path('aspects_configs/addonsAspectsRecipes.json')
THAUM_ASPECTS_ORDER_CONFIG_PATH = to_resource_path('aspects_configs/aspectsOrder.json')


def getAspectImagePath(aspectName, colored=True):
    return to_resource_path(f"images/{'color' if colored else 'mono'}/{aspectName}.png")
def getImagePathByNumber(number):
    return to_resource_path(f"images/numbers/{number}.png")
UNKNOWN_ASPECT_IMAGE_PATH = "images/unknownAspect.png"

EMPTY_ASPECT_SLOT_IMAGE_PATH = to_resource_path('images/emptyAspectPlace.png')
HEXAGON_MASK_IMAGE_PATH = to_resource_path('images/hexagons/hexagonMask.png')
HEXAGON_BORDER_MASK_IMAGE_PATH = to_resource_path('images/hexagons/hexagonBorderMask.png')
MASK_WITHOUT_NUMBER_IMAGE_PATH = to_resource_path('images/maskWithoutNumbers.png')
MASK_ONLY_NUMBER_IMAGE_PATH = to_resource_path('images/maskOnlyNumbers.png')
NONE_HEXAGON_SLOT_IMAGE_PATH = to_resource_path('images/hexagons/noneHexagon.png')
FREE_HEXAGON_SLOT_IMAGES_PATHS = [
    to_resource_path('images/hexagons/freeHexagons/1.png'),
    to_resource_path('images/hexagons/freeHexagons/2.png'),
    to_resource_path('images/hexagons/freeHexagons/3.png'),
    to_resource_path('images/hexagons/freeHexagons/4.png'),
    to_resource_path('images/hexagons/freeHexagons/5.png'),
    to_resource_path('images/hexagons/freeHexagons/6.png'),
    to_resource_path('images/hexagons/freeHexagons/7.png'),
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

# DELAY_BETWEEN_EVENTS = 0.1  # seconds
DELAY_BETWEEN_EVENTS = 0.2  # seconds
# DELAY_BETWEEN_RENDER = 0.5  # seconds
DELAY_BETWEEN_RENDER = 0.5  # seconds

EMPTY_TOLERANCE_PERCENT = 0.02

LOG_FILE_PATH = to_resource_path("logs/logs.log")
MAX_LOG_FILE_SIZE_BYTES = 1024 * 1024 # 1 Mb
# DEBUG = True
DEBUG = False
