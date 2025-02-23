import logging
import os
import sys

import appdata

app_paths = appdata.AppDataPaths('.ThaumcraftAutoResearcher')

app_paths.setup()

# ------------------------
# UI and visual part
MARGIN = 20
FPS = 60


# ------------------------
# Files paths
def to_resource_path(relative_path):
    ''' Get absolute path to resource, works for dev and for PyInstaller '''
    base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base_path, relative_path)


def to_appdata_path(relative_path):
    ''' Get absolute path to file into appdata folder, cross-platform '''
    return os.path.join(str(app_paths.app_data_path), relative_path)


THAUM_VERSION_CONFIG_PATH = to_appdata_path('user_configs/thaumVersionConfig.json')
THAUM_CONTROLS_CONFIG_PATH = to_appdata_path('user_configs/thaumControlsConfig.json')
THAUM_ASPECT_RECIPES_CONFIG_PATH = to_resource_path('aspects_configs/aspectsRecipes.json')
THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH = to_resource_path('aspects_configs/addonsAspectsRecipes.json')
THAUM_ASPECTS_ORDER_CONFIG_PATH = to_resource_path('aspects_configs/aspectsOrder.json')


def getAspectImagePath(aspectName, colored=True):
    return to_resource_path(f'images/{"color" if colored else "mono"}/{aspectName}.png')

UNKNOWN_ASPECT_IMAGE_PATH = to_resource_path('images/unknownAspect.png')
ASPECTS_IMAGES_SIZE = 32  # px

# ------------------------
# In-game inventory
# !!! Don't touch if you not sure !!!
INVENTORY_SLOTS_X = 9
INVENTORY_SLOTS_Y = 3

THAUM_ASPECTS_INVENTORY_SLOTS_X = 5
THAUM_ASPECTS_INVENTORY_SLOTS_Y = 5

THAUM_HEXAGONS_SLOTS_COUNT = 9  # must be odd

DELAY_BETWEEN_EVENTS = 0.15  # seconds
DELAY_BETWEEN_RENDER = 0.5  # seconds

# ------------------------
# Neurolink constants
FIELD_OBJECT_DETECTION_PATH = to_resource_path("models/field_object_detection.onnx")
INVENTORY_OBJECT_DETECTION_PATH = to_resource_path("models/inventory_object_detection.onnx")
FIELD_CLASS_NAMES_PATH = to_resource_path("models/field_class_names.txt")
INVENTORY_CLASS_NAMES_PATH = to_resource_path("models/inventory_class_names.txt")
NEUROLINK_FREE_HEXAGON_PREDICTION_NAME = "free_hex"
NEUROLINK_SCRIPT_IMAGE_PREDICTION_NAME = "script"
NEUROLINK_UNKNOWN_ASPECT_PREDICTION_NAME = "unknown"


# ------------------------
# Other constants
IMAGES_TOLERANCE_PERCENT = 0.02
IMAGE_TMP_PATH = to_appdata_path('.tmp/tmp.png')
LOG_FILE_PATH = to_appdata_path('logs/logs.log')

# Loggers
MAX_LOG_FILE_SIZE_BYTES = 1024 * 1024 * 5  # 5 Mb
MAX_LOG_FILES_COUNT = 20
LOG_LEVEL = logging.DEBUG

# ------------------------
# DEBUG = True
DEBUG = False
