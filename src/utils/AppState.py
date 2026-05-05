import json
import logging
import os

from configs.constants import LANGUAGE_CONFIG_PATH, THAUM_VERSION_CONFIG_PATH, THAUM_ASPECT_RECIPES_CONFIG_PATH, \
    THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH, THAUM_CONTROLS_CONFIG_PATH, THAUM_ASPECTS_ORDER_CONFIG_PATH
from configs.translations import TRANSLATIONS
from utils.LinkableValue import linkableValueDumpsToJSON
from utils.utils import createDirByFilePath


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


def saveJSONConfig(fullpath: str, jsonToSave: dict):
    createDirByFilePath(fullpath)
    with open(fullpath, 'w') as file:
        json.dump(jsonToSave, file, indent=4, ensure_ascii=False, default=linkableValueDumpsToJSON)


class _AppState:
    def __init__(self):
        self.selectedLanguage: None | str = None
        self.translatedTexts: dict[str, str] = {}

        self.selectedThaumVersion: None | str = None
        self.aspectRecipes: dict[str, str] = {}
        self.aspectsOrder: list[str] = []
        self.allAspectRecipes: dict[str, dict[str, str]] = {}
        self.allAddonsRecipes: dict[str, dict[str, str]] = {}

        self.selectedThaumVersion: None | str = None
        self.aspectRecipes: dict[str, str] = {}

        self.thaumWindowControls: dict[str, str] | None = None

    # -------------------------
    def rereadLanguage(self):
        # get selected language
        readed = readJSONConfig(LANGUAGE_CONFIG_PATH)
        if readed is None:
            self.selectedLanguage = None
            return
        self.selectedLanguage = readed['language']
        logging.debug(f"Selected language rereaded: {self.selectedLanguage}")

        # get translations for language
        self.translatedTexts = TRANSLATIONS.get(self.selectedLanguage)
        if self.translatedTexts is None:
            logging.critical(f"No translations found for selected language: {self.selectedLanguage}")
            self.translatedTexts = {}
        logging.debug(f"Selected language and translations successfully rereaded. Selected language: {self.selectedLanguage}")

    def saveLanguage(self, language: str):
        saveJSONConfig(LANGUAGE_CONFIG_PATH, {
            'language': language,
        })
        logging.debug(f"Selected language successfully saved: {language}")
        self.rereadLanguage()

    # -------------------------
    def rereadThaumVersion(self):
        # get all recipes
        self.allAspectRecipes = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
        if self.allAspectRecipes is None:
            logging.error(f'Cannot load all recipes')
            return
        logging.debug(f"All aspects recipes rereaded")

        # get aspects order
        readed = readJSONConfig(THAUM_ASPECTS_ORDER_CONFIG_PATH)
        if readed is None:
            self.aspectsOrder = []
            logging.error(f'Cannot load recipes order config')
            return
        self.aspectsOrder = readed['aspects']
        logging.debug(f"Aspects order rereaded")

        # get selected version
        readed = readJSONConfig(THAUM_VERSION_CONFIG_PATH)
        if readed is None:
            self.selectedThaumVersion = None
            self.aspectRecipes = {}
            return
        self.selectedThaumVersion = readed['version']
        logging.debug(f"Selected version rereaded: {self.selectedThaumVersion}")

        # get recipes FOR selected version
        self.aspectRecipes = self.allAspectRecipes.get(self.selectedThaumVersion)
        if self.aspectRecipes is None:
            logging.critical(f"No aspect recipes found for selected thaum version: {self.selectedThaumVersion}")
            self.aspectRecipes = {}
            return

        # add all recipes for addons
        self.allAddonsRecipes = readJSONConfig(THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH)
        for addonRecipes in self.allAddonsRecipes.values():
            self.aspectRecipes |= addonRecipes
        logging.debug(f"Thaum version and aspects recipes successfully rereaded. Selected version: {self.selectedThaumVersion}")

    def saveThaumVersion(self, version: str):
        saveJSONConfig(THAUM_VERSION_CONFIG_PATH, {
            'version': version,
        })
        logging.debug(f"Thaum version successfully saved: {version}")
        self.rereadThaumVersion()

    # -------------------------
    def rereadThaumWindowControls(self):
        self.thaumWindowControls = readJSONConfig(THAUM_CONTROLS_CONFIG_PATH)
        logging.debug(f"Thaum window controls rereaded")

    def saveThaumWindowControls(self, pointWritingMaterials, pointPapers, rectAspectsListingLT, rectAspectsListingRB,
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
        logging.info(f"Thaum window controls config successfully saved: (long JSON ommitted)")
        self.rereadThaumWindowControls()

    # -------------------------
    def rereadAllConfigs(self):
        self.rereadLanguage()
        self.rereadThaumVersion()
        self.rereadThaumWindowControls()

# Создаем единственный экземпляр для экспорта
AppState = _AppState()
