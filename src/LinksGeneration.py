import logging
class Aspect:
    name: str
    recipe: list
    includes: set

    def __init__(self, name):
        self.name = name
        self.recipe = []
        self.includes = set()

    def __str__(self):
        return f"{self.name} = {list(map(lambda x: x.name, self.recipe))}"



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generateLinkMap(existingAspects, freeHexagons, aspectRecipes):
    # Create list of Aspect classes
    aspects = {}
    for aspectName in aspectRecipes.keys():
        aspects[aspectName] = Aspect(aspectName)
    for aspectName in aspects.keys():
        aspect = aspects[aspectName]
        aspect.recipe = list(map(lambda x: aspects[x], aspectRecipes[aspectName]))
        for recipeAspect in aspect.recipe:
            recipeAspect.includes.add(aspect)

    # Prepare the output list
    placed_aspects = []

    # Helper function to find the nearest free hexagon
    def find_nearest_free_hexagon(start):
        min_distance = float('inf')
        nearest_hex = None
        for hexagon in freeHexagons:
            distance = abs(start[0] - hexagon[0]) + abs(start[1] - hexagon[1])
            if distance < min_distance:
                min_distance = distance
                nearest_hex = hexagon
        return nearest_hex

    # Place each aspect optimally on the grid
    for aspectName, coord in existingAspects.items():
        placed_aspects.append((aspectName, coord[0], coord[1]))

    for aspectName, aspect in aspects.items():
        if aspectName not in existingAspects:
            nearest_hex = find_nearest_free_hexagon((0, 0))  # Assuming (0, 0) as the starting point
            if nearest_hex:
                placed_aspects.append((aspectName, nearest_hex[0], nearest_hex[1]))
                freeHexagons.remove(nearest_hex)

    # Log the result
    logger.info("Aspect placement successful")
    logger.info("Placed Aspects: %s", placed_aspects)

    return placed_aspects


