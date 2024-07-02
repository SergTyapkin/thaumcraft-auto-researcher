import heapq

from src.utils.utils import loadRecipesForSelectedVersion, readJSONConfig

MAX_PATH_LEN = 10

class PathElement:
    def __init__(self, path, length):
        self.path = path
        self.length = length

    def __lt__(self, other):
        return self.length < other.length

class AspectGraph:
    graph: dict[str, [str, str]] = {}

    def __init__(self, aspectRecipes: dict[str, [str, str]]):
        self.regenerate_graph_combinations(aspectRecipes)

    def regenerate_graph_combinations(self, aspectRecipes: dict[str, [str, str]]):
        self.graph.clear()
        for aspectName, recipe in aspectRecipes.items():
            for component in recipe:
                self.add_connection(aspectName, component)

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

    def __repr__(self):
        return f"AspectsGraph(graph={self.graph})"


class Aspect:
    name: str
    coord: (int, int)
    linked_to_initials: set[str] = set()
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord
    def get_distance_to(self, other_aspect):
        return (
            other_aspect.coord[0] - self.coord[0] +
            other_aspect.coord[1] - self.coord[1]
        )


def generateLinkMap(existing_aspects: dict[str, (int, int)], holes_set: set[(int, int)]) -> dict[str, (int, int)]:
    print("Started solving...")
    print("Existing aspects:", existing_aspects)
    print("Free hexagons:", holes_set)
    aspect_recipes = loadRecipesForSelectedVersion()
    aspect_graph = AspectGraph(aspect_recipes)

    result = {}
    initial_aspects: set[Aspect] = set()
    aspects_on_field: set[Aspect] = set()

    for aspectName, coord in existing_aspects.items():
        coord = existing_aspects[aspectName]
        initial_aspects.add = Aspect(aspectName, coord)
        aspects_on_field.add = Aspect(aspectName, coord)
        result[aspectName] = coord

    for start_aspect in initial_aspects:
        aspect_not_linked_to = start_aspect.linked_to_initials.difference(initial_aspects)
        target_initial_aspect = aspect_not_linked_to.pop()
        min_len_aspect = None
        min_len_to_aspect = 0
        for end_aspect_candidate in aspects_on_field:
            if start_aspect.coord == end_aspect_candidate.coord:
                continue
            if target_initial_aspect not in end_aspect_candidate.linked_to_initials:
                continue

            path_len = start_aspect.get_distance_to(target_initial_aspect)
            if (min_len_aspect is None) or (path_len < min_len_to_aspect):
                min_len_aspect = end_aspect_candidate
                min_len_to_aspect = path_len

        end_aspect = min_len_aspect
        for target_path_len in range(min_len_to_aspect, MAX_PATH_LEN):
            path = aspect_graph.find_path(start_aspect, end_aspect, 10) # TODO: find length of path
            if not path:
                continue

            current_coord = start_coord
            for aspect in path[1:]:
                # if aspect not in placed_aspects.values():
                    free_coord = find_free_coordinate(placed_aspects, holes_set, current_coord)
                    if not free_coord:
                        continue
                    result[aspect] = free_coord
                    placed_aspects[free_coord] = aspect
                    current_coord = free_coord
    print("Solved:", result)
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

