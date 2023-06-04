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


def generateLinkMap(
        existingAspects: dict[str, (int, int)],
        freeHexagons: list[(int, int)],
        aspectRecipes: dict[str, (str, str)]) -> list[(str, int, int)]:
    # Create list of Aspect classes
    aspects = {}
    for aspectName in aspectRecipes.keys():
        aspects[aspectName] = Aspect(aspectName)
    for aspectName in aspects.keys():
        aspect = aspects[aspectName]
        recipeAspects = list(map(lambda x: aspects[x], aspectRecipes[aspectName]))
        aspect.recipe = recipeAspects
        for recipeAspect in recipeAspects:
            recipeAspect.includes.add(aspect)

    # Start of logic
    pass
