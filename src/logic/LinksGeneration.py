import heapq

from src.utils.utils import loadRecipesForSelectedVersion

MAX_PATH_LEN = 10

class AspectGraph:
    graph: dict[str, [str, str]]

    def __init__(self, aspectRecipes: dict[str, [str, str]]):
        self.graph = {}
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
        class PathElement:
            path: list[str]
            length: int
            def __init__(self, path: list[str], length: int):
                self.path = path
                self.length = length
            def __repr__(self):
                return f"{'{'}{self.length}{'}'}"
            def __lt__(self, other):
                return self.length < other.length

        def search(queue, to):
            print("START FINDING ASPECT PATH IN", steps, "STEPS...")
            while queue:
                element = heapq.heappop(queue)
                last_node = element.path[-1]

                # print(element, element.path, last_node, to, steps)
                # print(self.graph.get(last_node, []))
                if element.length > steps:
                    continue
                if (last_node == to) and (element.length == steps):
                    return element.path
                for neighbor in self.graph.get(last_node, []):
                    heapq.heappush(queue, PathElement(element.path + [neighbor], element.length + 1))
            return None

        queue = [PathElement([from_aspect], 0)]
        return search(queue, to_aspect)

    def __repr__(self):
        return f"AspectsGraph(graph={self.graph})"


class Aspect:
    name: str
    coord: (int, int)
    linked_to_initials: set

    def __init__(self, name, coord):
        self.name = name
        self.coord = coord
        self.linked_to_initials = set()

    def __repr__(self):
        return f"{self.name}{self.coord}"

    def get_min_distance_path_to(self, targetAspect, hexagonFieldRadius: int, holesSet: set[(int, int)], initial_aspects: set, minLength: int = 0):
        # Алгоритм Дейкстры
        # Для каждой клетки храним минимальное расстояние до неё. Или None, если клетка ещё не посещена
        class PathElement:
            path: list[(int, int)]
            dist: int = 999999
            coord: (int, int)
            def __init__(self, x: int, y: int):
                self.coord = (x, y)
                self.path = []
            def __repr__(self):
                return f"{self.coord}{'{'}{self.dist}{'}'}"
            def __lt__(self, other):
                return self.dist < other.dist
        cells: dict[(int, int), PathElement] = {}
        unvisitedNodes: set[PathElement] = set()

        # Создаем все клетки
        for x in range(-hexagonFieldRadius, hexagonFieldRadius + 1):
            for y in range(-hexagonFieldRadius + (abs(x) + 1) // 2, hexagonFieldRadius - (abs(x)) // 2 + 1):
                pathElem = PathElement(x, y)
                cells[(x, y)] = pathElem
                unvisitedNodes.add(pathElem)

        # В начальной ставим расстояние 0
        startCell = cells[self.coord]
        startCell.dist = 0
        startCell.path = [self.coord]

        # Пока есть узлы, в которых мы не были
        while len(unvisitedNodes) > 0:
            currentNode = min(unvisitedNodes)
            # Получаем список соседей для текущей клетки
            if currentNode.coord[0] % 2 == 1:
                cell_neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1)]
            else:
                cell_neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, 1)]
            # Приоритизируем его, чтобы первым делом поиск производился в сторону других аспектов
            def comparator(coord):
                totalDiff = 0
                for initialAspect in initial_aspects:
                    totalDiff += abs(initialAspect.coord[0] - coord[0])
                    totalDiff += abs(initialAspect.coord[1] - coord[1])
                return totalDiff
            cell_neighbours.sort(key=comparator)
            # Приведенный ниже блок кода извлекает соседей текущего узла и обновляет их расстояния.
            for neighborDirection in cell_neighbours:
                neighborCoord = (currentNode.coord[0] + neighborDirection[0], currentNode.coord[1] + neighborDirection[1])
                if neighborCoord in holesSet:
                    continue
                neighborNode = cells.get(neighborCoord, None)
                if neighborNode is None:
                    continue
                tentative_value = currentNode.dist + 1
                if neighborNode.coord == targetAspect.coord:
                   if (tentative_value >= minLength) and (tentative_value < neighborNode.dist):
                       neighborNode.dist = tentative_value
                       neighborNode.path = currentNode.path + [neighborCoord]
                else:
                    if tentative_value < neighborNode.dist:
                        neighborNode.dist = tentative_value
                        neighborNode.path = currentNode.path + [neighborCoord]
            unvisitedNodes.remove(currentNode)
        print(f"All dists to all cells (min dist: {minLength}):", cells)
        return cells[targetAspect.coord].dist, cells[targetAspect.coord].path


def generateLinkMap(existing_aspects: dict[(int, int), str], holes_set: set[(int, int)]) -> dict[(int, int): str]:
    print("-----------")
    print("Existing aspects:", existing_aspects)
    print("Holes hexagons:", holes_set)
    print("Started solving...")
    aspect_recipes = loadRecipesForSelectedVersion()
    aspect_graph = AspectGraph(aspect_recipes)

    result = {}
    initial_aspects: set[Aspect] = set()
    aspects_on_field: set[Aspect] = set()
    maxX = 0
    maxY = 0

    # Первоначальная обработка входных данных
    for coord, aspectName in existing_aspects.items():
        aspectObject = Aspect(aspectName, coord)
        initial_aspects.add(aspectObject)
        aspects_on_field.add(aspectObject)
        aspectObject.linked_to_initials.add(aspectObject)
        result[coord] = aspectName
        maxX = max(maxX, abs(coord[0]))
        maxY = max(maxY, abs(coord[1]))

    hexagonFieldRadius = max(maxX, maxY)

    # Продолжаем, пока все изначальные аспекты не будут связаны
    isAllAspectsLinked = False
    while not isAllAspectsLinked:
        isAllAspectsLinked = True
        # Вывбираем один аспект из изначальных
        for start_aspect in initial_aspects:
            # Получаем, к каким изначальынм аспектам он не привязан
            # Говорим, что хотим привязать его к первому из них
            not_linked_to_aspects = initial_aspects.difference(start_aspect.linked_to_initials)
            if len(not_linked_to_aspects) == 0:
                continue
            isAllAspectsLinked = False
            initial_aspect_to_link = not_linked_to_aspects.pop()
            min_len_aspect = None
            min_len_to_aspect = 0
            print("Needs to link", start_aspect, "to", initial_aspect_to_link)
            # Ищем ближайщий ПО РАССТОЯНИЮ аспект, связанный с тем, к которому хотим привязать
            for end_aspect_candidate in aspects_on_field:
                if start_aspect.coord == end_aspect_candidate.coord:
                    continue
                if initial_aspect_to_link not in end_aspect_candidate.linked_to_initials:
                    continue

                path_len, _ = start_aspect.get_min_distance_path_to(end_aspect_candidate, hexagonFieldRadius, holes_set, initial_aspects)
                if (min_len_aspect is None) or (path_len < min_len_to_aspect):
                    min_len_aspect = end_aspect_candidate
                    min_len_to_aspect = path_len

            if min_len_to_aspect > MAX_PATH_LEN:
                print(f"Error: End cell with aspect {start_aspect} is unreachable from any other aspects")
                return existing_aspects
            # К выбранному аспекту пытаемся построить цепочки. Сначала самую короткую, потом всё длиннее
            end_aspect = min_len_aspect
            target_path_len = min_len_to_aspect
            while target_path_len < MAX_PATH_LEN:
                aspectsPath = aspect_graph.find_path(start_aspect.name, end_aspect.name, target_path_len) # TODO: find length of path
                print(f"Trying to generate path from {start_aspect} to {end_aspect}, len: {target_path_len}")
                if not aspectsPath:
                    target_path_len += 1
                    continue
                print(f"Path generated: {aspectsPath}")
                # Если цепочка найдена, пытаемся пройти найти маршрут заданной длины
                _, coordsPath = start_aspect.get_min_distance_path_to(end_aspect, hexagonFieldRadius, holes_set, initial_aspects, target_path_len)
                print(f"Coordinates path regenerated: {coordsPath}")

                print("Successfully generated path")
                totalLinkedToInitials = start_aspect.linked_to_initials.union(end_aspect.linked_to_initials)
                start_aspect.linked_to_initials = totalLinkedToInitials
                end_aspect.linked_to_initials = totalLinkedToInitials
                for i in range(target_path_len):
                    result[coordsPath[i]] = aspectsPath[i]
                    addedAspect = Aspect(aspectsPath[i], coordsPath[i])
                    addedAspect.linked_to_initials = totalLinkedToInitials
                    aspects_on_field.add(addedAspect)
                break
            if target_path_len == MAX_PATH_LEN:
                print(f"Error: Path from {start_aspect} to {end_aspect} cannot be generated")
                return existing_aspects
    print("Solved:", result)
    return result

