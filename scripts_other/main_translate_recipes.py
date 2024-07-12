from src.utils.constants import THAUM_ASPECT_RECIPES_CONFIG_PATH, THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH
from src.utils.utils import readJSONConfig, saveJSONConfig

THAUM_TRANSLATION_CONFIG_PATH = './scripts_other/translationDictionary.json'

if __name__ == '__main__':
    translationsConfig = readJSONConfig(THAUM_TRANSLATION_CONFIG_PATH)
    aspectsRecipes = readJSONConfig(THAUM_ASPECT_RECIPES_CONFIG_PATH)
    addonsRecipes = readJSONConfig(THAUM_ADDONS_ASPECT_RECIPES_CONFIG_PATH)
    newAspectRecipes = {}
    allAddonsRecipes = {}
    for addonName, recipes in addonsRecipes.items():
        allAddonsRecipes |= recipes

    for version, recipes in aspectsRecipes.items():
        newRecipes = {}
        for aspect, recipe in recipes.items():
            aspect = translationsConfig.get(aspect, aspect)
            recipe = list(map(lambda asp: translationsConfig.get(asp, asp), recipe))
            if aspect not in allAddonsRecipes:
                newRecipes[aspect] = recipe
        newAspectRecipes[version] = newRecipes
    print(newAspectRecipes)
    saveJSONConfig('./scripts_other/new_recipes.json', newAspectRecipes)
    print("New recipes written to", "new_recipes.json")
