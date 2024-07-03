import heapq

from src.utils.utils import loadRecipesForSelectedVersion

MAX_PATH_LEN = 15

'''
Описание работы алгоритма:

1. Надо узнать, какой аспект с каким будем соединять, для этого: 
1.1. Берём любой аспект из базовых (базовые - это те, что стояли. изначально). Он будет стартовым
1.2. Смотрим, с какими базовыми он ещё не соединён, выбираем любой из них.
1.3. Из всех аспектов на поле выбираем ближайший к стартовому, и соединенный с выбранным. Расстояние определяется алгоритмом Дейкстры.

2. У нас есть 2 аспекта, которые надо соединить, и кратчайшее расстояние между ними. Ищем цепочку аспектов, реализующую это. Для этого используем BFS:
2.1. От стартового берем все аспекты, с которыми он может связаться (граф аспектов) (получаем длину цепочки 2), от них, от каждого, берём все аспекты, с которыми они могут связаться (получаем длину цепочки 3), и т.д. 
2.2. Если любая из полученных цепочек имеет требуемую длину, и заканчивается на необходимый аспект, мы ее нашли!
2.3. Если были перебраны все цепочки до MAX_PATH_LEN=10 длины, и среди них нет ни одной подходящей, выходим, запускаем всё это заново, но теперь будем пытаться найти цепочку на 1 длиннее.
2.4. Если цепочка так и не была найдена - кидаем ошибку, так не должно быть.

3. У нас есть два аспекта, и длина цепочки между ними. Надо найти положения, как будем раскладывать аспекты. Для этого:
3.1. Запускаем алгоритм Дейкстры, который ищет не минимальное расстояние до целевой клетки, а только заданное расстояние. Таким образом находим маршрут до клетки.
3.2. Если маршрут требуемой длины не найден - кидаем ошибку, так не должно быть

4. Есть всё, подготовка к следующему шагу:
4.1. Записываем полученные аспекты на полученные места.
4.2. Говорим, что все аспекты соединены со всеми базовыми аспектами, с которыми был соединён стартовый, и с которыми был соединён целевой

5. Заканчиваем, когда все базовые аспекты соединены друг с другом
'''

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

        def search(queue, to, visited):
            while queue:
                element = heapq.heappop(queue)
                last_node = element.path[-1]

                # print(element, element.path, last_node, to, steps)
                # print(self.graph.get(last_node, []))
                if element.length > steps:
                    continue
                if (last_node in visited) and (element.length in visited[last_node]):
                    continue
                if (last_node == to) and (element.length == steps):
                    return element.path
                for neighbor in self.graph.get(last_node, []):
                    heapq.heappush(queue, PathElement(element.path + [neighbor], element.length + 1))
                if last_node not in visited:
                    visited[last_node] = []
                visited[last_node].append(element.length)
            return None

        queue = [PathElement([from_aspect], 0)]
        visited = {}
        return search(queue, to_aspect, visited)

    def __repr__(self):
        return f"AspectsGraph(graph={self.graph})"


class Aspect:
    name: str
    coord: (int, int)
    linked_to: set

    def __init__(self, name, coord):
        self.name = name
        self.coord = coord
        self.linked_to = set()

    def __repr__(self):
        return f"{self.name}{self.coord}"

    def get_min_distance_path_to(self, targetAspect, hexagonFieldRadius: int, holesSet: set[(int, int)], initial_aspects: set, minLength: int = 0):
        # Алгоритм Дейкстры
        # Для каждой клетки храним минимальное расстояние до неё. Или None, если клетка ещё не посещена
        DEFAULT_INITIAL_PATH_LEN = 999999

        class PathElement:
            path: list[(int, int)]
            dist: int = DEFAULT_INITIAL_PATH_LEN
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
        if cells.get(self.coord) is None:
            return DEFAULT_INITIAL_PATH_LEN, set()
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
        return cells[targetAspect.coord].dist, cells[targetAspect.coord].path


def generateLinkMap(existing_aspects: dict[(int, int), str], holes_set: set[(int, int)]) -> dict[(int, int): str]:
    print("-----------")
    print("START SOLVING")
    print("#---0. Setting up:")
    print("EXISTING ASPECTS:", existing_aspects)
    print("HOLES HEXAGONS:", holes_set)
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
        aspectObject.linked_to.add(aspectObject)
        result[coord] = aspectName
        maxX = max(maxX, abs(coord[0]))
        maxY = max(maxY, abs(coord[1]))

    hexagonFieldRadius = max(maxX, maxY)
    print("Hexagon field radius:", hexagonFieldRadius)

    # Продолжаем, пока все изначальные аспекты не будут связаны
    isAllAspectsLinked = False
    while not isAllAspectsLinked:
        isAllAspectsLinked = True
        # Вывбираем один аспект из изначальных
        for start_initial_aspect in initial_aspects:
            # Получаем, к каким изначальынм аспектам он не привязан
            # Говорим, что хотим привязать его к первому из них
            not_linked_to_aspects = initial_aspects.difference(start_initial_aspect.linked_to)
            print(start_initial_aspect, "not linked to", not_linked_to_aspects)
            if len(not_linked_to_aspects) == 0:
                continue
            isAllAspectsLinked = False
            end_initial_aspect = not_linked_to_aspects.pop()
            min_start_aspect = None
            min_end_aspect = None
            min_len_between_aspects = 0
            print("#---1. Found initial aspects to link:", start_initial_aspect, "to", end_initial_aspect)
            # Ищем ближайшие ПО РАССТОЯНИЮ аспекты, связанные с теми, от котороо и к которому хотим привязать
            for start_aspect_candidate in aspects_on_field:
                if start_initial_aspect not in start_aspect_candidate.linked_to:
                    continue
                for end_aspect_candidate in aspects_on_field:
                    if start_aspect_candidate.coord == end_aspect_candidate.coord:
                        continue
                    if end_initial_aspect not in end_aspect_candidate.linked_to:
                        continue

                    path_len, _ = start_aspect_candidate.get_min_distance_path_to(end_aspect_candidate, hexagonFieldRadius, holes_set, initial_aspects)
                    if (min_start_aspect is None or min_end_aspect is None) or (path_len < min_len_between_aspects):
                        min_start_aspect = start_aspect_candidate
                        min_end_aspect = end_aspect_candidate
                        min_len_between_aspects = path_len

            if min_len_between_aspects > MAX_PATH_LEN:
                print(f"Error: End cell with aspect {end_initial_aspect} is unreachable from {start_initial_aspect}")
                return existing_aspects
            print("Min distance", min_len_between_aspects, "found from aspect:", min_start_aspect, "to aspect:", min_end_aspect)
            # К выбранному аспекту пытаемся построить цепочки. Сначала самую короткую, потом всё длиннее
            end_aspect = min_end_aspect
            start_aspect = min_start_aspect
            target_path_len = min_len_between_aspects
            print("#---2. Trying to found aspects path from", start_aspect.name, "to", end_aspect.name)
            while target_path_len < MAX_PATH_LEN:
                aspectsPath = aspect_graph.find_path(start_aspect.name, end_aspect.name, target_path_len) # TODO: find length of path
                if not aspectsPath:
                    print("Path with len", target_path_len, "not found")
                    target_path_len += 1
                    continue
                print("Path with len:", target_path_len, "generated:", aspectsPath)
                # Если цепочка найдена, пытаемся пройти найти маршрут заданной длины
                print("#---3. Trying to find coordinates path with len", target_path_len, "from", start_aspect, "to", end_aspect)
                min_len_between_aspects, coordsPath = start_aspect.get_min_distance_path_to(end_aspect, hexagonFieldRadius, holes_set, initial_aspects, target_path_len)
                if min_len_between_aspects > MAX_PATH_LEN:
                    print("Coordinates path with len", target_path_len, "not found")
                    target_path_len += 1
                    continue
                print(f"Coordinates path found: {coordsPath}")

                print("#---4. Fill gotten aspects and prepare to next step")
                # Объединяем linked_to, и записываем в оба исходых аспекта один и тот же этот список)
                all_added_aspects = set()
                for i in range(target_path_len):
                    result[coordsPath[i]] = aspectsPath[i]
                    addedAspect = Aspect(aspectsPath[i], coordsPath[i])
                    aspects_on_field.add(addedAspect)
                    all_added_aspects.add(addedAspect)
                start_initial_aspect.linked_to.update(all_added_aspects)
                start_initial_aspect.linked_to.update(end_initial_aspect.linked_to)
                end_initial_aspect.linked_to.update(start_initial_aspect.linked_to)
                print(start_aspect, "is now linked to initials", start_aspect.linked_to.intersection(initial_aspects))
                print(end_aspect, "is now linked to initials", end_aspect.linked_to.intersection(initial_aspects))

                for aspect in start_initial_aspect.linked_to.copy():
                    aspect.linked_to.update(start_aspect.linked_to)
                print("Aspect path putted on field. Total aspects:", aspects_on_field)
                print("Iteration finished.")
                break
            if target_path_len == MAX_PATH_LEN:
                print(f"Error: Path from {start_aspect} to {end_aspect} cannot be generated")
                return existing_aspects
    print("SOLVED:", result)
    return result

