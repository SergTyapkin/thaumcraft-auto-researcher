import heapq

from src.utils.constants import THAUM_TRANSLATION_CONFIG_PATH
from src.utils.utils import loadRecipesForSelectedVersion, readJSONConfig

class PathElement:
    def __init__(self, path, length):
        self.path = path
        self.length = length

    def __lt__(self, other):
        return self.length < other.length

class AspectGraph:
    def __init__(self):
        self.graph = {}
        self.translation_dictionary = readJSONConfig(THAUM_TRANSLATION_CONFIG_PATH)
        self.combinations = loadRecipesForSelectedVersion()

    def add_aspect_combinations(self):
        for aspect, components in self.combinations.items():
            translated_aspect = self.translate_aspect(aspect)
            for component in components:
                translated_component = self.translate_aspect(component)
                self.add_connection(translated_aspect, translated_component)

    def add_connection(self, aspect1, aspect2):
        if aspect1 not in self.graph:
            self.graph[aspect1] = []
        if aspect2 not in self.graph:
            self.graph[aspect2] = []
        self.graph[aspect1].append(aspect2)
        self.graph[aspect2].append(aspect1)

    def find_path(self, from_aspect, to_aspect, steps):
        def search(queue, to, visited):
            while queue:
                element = heapq.heappop(queue)
                path, length = element.path, element.length
                last_node = path[-1]
                if last_node == to:
                    return path
                if last_node not in visited:
                    visited.add(last_node)
                    for neighbor in self.graph.get(last_node, []):
                        if neighbor not in visited:
                            heapq.heappush(queue, PathElement(path + [neighbor], length + 1))
            return None

        queue = [PathElement([from_aspect], 0)]
        visited = set()
        return search(queue, to_aspect, visited)

    def translate_aspect(self, aspect):
        translated = self.translation_dictionary.get(aspect, aspect)
        # print(f"Translated aspect: {aspect} to {translated}")  # Debug
        return translated

    def __repr__(self):
        return f"Aspect(name={self.name})"

def generateLinkMap(existingAspects, noneHexagons):
    aspect_graph = AspectGraph()

    aspect_graph.add_aspect_combinations()

    holes_set = set(tuple(hole) for hole in noneHexagons)
    result = {}
    placed_aspects = {}

    for aspect in existingAspects:
        coord = existingAspects[aspect]
        if tuple(coord) not in holes_set:
            translated_aspect = aspect_graph.translate_aspect(aspect)
            placed_aspects[tuple(coord)] = translated_aspect
            result[translated_aspect] = coord

    for start_coord, start_aspect in list(placed_aspects.items()):
        for end_coord, end_aspect in list(placed_aspects.items()):
            if start_coord != end_coord:
                path = aspect_graph.find_path(start_aspect, end_aspect, 10)
                if path:
                    current_coord = start_coord
                    for aspect in path[1:]:
                        if aspect not in placed_aspects.values():
                            free_coord = find_free_coordinate(placed_aspects, holes_set, current_coord)
                            if free_coord:
                                result[aspect] = free_coord
                                placed_aspects[free_coord] = aspect
                                current_coord = free_coord

    return result

def find_free_coordinate(placed_aspects, holes_set, start_coord):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]
    queue = [start_coord]
    visited = set()

    while queue:
        x, y = queue.pop(0)
        for dx, dy in directions:
            new_coord = (x + dx, y + dy)
            if new_coord not in placed_aspects and new_coord not in holes_set and new_coord not in visited:
                return new_coord
            if new_coord not in visited:
                visited.add(new_coord)
                queue.append(new_coord)

    return None

