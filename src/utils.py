import json
import math
import os

from src.LinkableValue import linkableValueDumpsToJSON
from src.constants import THAUM_CONTROLS_CONFIG_NAME, THAUM_CONTROLS_CONFIG_DIR


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def saveThaumControlsConfig(pointWritingMaterials, pointScrolls, rectAspectsListingLT, rectAspectsListingRB,
                            pointAspectsScrollLeft, pointAspectsScrollRight,
                            pointAspectsMixLeft, pointAspectsMixCreate, pointAspectsMixRight, rectInventoryLT,
                            rectInventoryRB, rectHexagonsLT, rectHexagonsRB):
    if not os.path.exists(THAUM_CONTROLS_CONFIG_DIR):
        os.makedirs(THAUM_CONTROLS_CONFIG_DIR)

    with open(os.path.join(THAUM_CONTROLS_CONFIG_DIR, THAUM_CONTROLS_CONFIG_NAME), 'w') as file:
        json.dump({
            "pointWritingMaterials": {"x": pointWritingMaterials.x, "y": pointWritingMaterials.y},
            "pointScrolls": {"x": pointScrolls.x, "y": pointScrolls.y},
            "rectAspectsListingLT": {"x": rectAspectsListingLT.x, "y": rectAspectsListingLT.y},
            "rectAspectsListingRB": {"x": rectAspectsListingRB.x, "y": rectAspectsListingRB.y},
            "pointAspectsScrollLeft": {"x": pointAspectsScrollLeft.x, "y": pointAspectsScrollLeft.y},
            "pointAspectsScrollRight": {"x": pointAspectsScrollRight.x, "y": pointAspectsScrollRight.y},
            "pointAspectsMixLeft": {"x": pointAspectsMixLeft.x, "y": pointAspectsMixLeft.y},
            "pointAspectsMixCreate": {"x": pointAspectsMixCreate.x, "y": pointAspectsMixCreate.y},
            "pointAspectsMixRight": {"x": pointAspectsMixRight.x, "y": pointAspectsMixRight.y},
            "rectInventoryLT": {"x": rectInventoryLT.x, "y": rectInventoryLT.y},
            "rectInventoryRB": {"x": rectInventoryRB.x, "y": rectInventoryRB.y},
            "rectHexagonsLT": {"x": rectHexagonsLT.x, "y": rectHexagonsLT.y},
            "rectHexagonsRB": {"x": rectHexagonsRB.x, "y": rectHexagonsRB.y},
        }, file, indent=4, ensure_ascii=False, default=linkableValueDumpsToJSON)


def readThaumControlsConfig():
    if not os.path.isfile(os.path.join(THAUM_CONTROLS_CONFIG_DIR, THAUM_CONTROLS_CONFIG_NAME)):
        return None
    with open(os.path.join(THAUM_CONTROLS_CONFIG_DIR, THAUM_CONTROLS_CONFIG_NAME), 'r') as file:
        config = json.load(file)
    return config
