import logging

from src.utils.utils import loadRecipesForSelectedVersion

MAX_PATH_LEN = 18
DEFAULT_INITIAL_PATH_LEN = 999999

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
    graph: dict[str, set[str]]

    def __init__(self, aspect_recipes: dict[str, list[str, str]]):
        self.graph = {}
        self.regenerate_graph_combinations(aspect_recipes)

    def regenerate_graph_combinations(self, aspect_recipes: dict[str, list[str, str]]):
        self.graph.clear()
        for aspect_name, recipe in aspect_recipes.items():
            for component in recipe:
                if component in aspect_recipes:
                    self.add_connection(aspect_name, component)

    def add_connection(self, aspect1, aspect2):
        if aspect1 not in self.graph:
            self.graph[aspect1] = set()
        if aspect2 not in self.graph:
            self.graph[aspect2] = set()
        self.graph[aspect1].add(aspect2)
        self.graph[aspect2].add(aspect1)

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

        def searchDFS(current_path_element):
            if current_path_element.length > steps:
                return None
            last_node = current_path_element.path[-1]
            if (last_node == to_aspect) and (current_path_element.length == steps):
                return current_path_element.path
            for neighbor in self.graph.get(last_node, []):
                result = searchDFS(PathElement(current_path_element.path + [neighbor], current_path_element.length + 1))
                if result is not None:
                    return result

        return searchDFS(PathElement([from_aspect], 0))

    def __repr__(self):
        return f"AspectsGraph(graph={self.graph})"


class Aspect:
    name: str
    coord: (int, int)
    linked_to_initials: set

    def __init__(self, name, coord, linked_to_initials):
        self.name = name
        self.coord = coord
        self.linked_to_initials = linked_to_initials

    def __repr__(self):
        return f"{self.name}{self.coord}"

    def get_min_distance_path_to(self, target_aspect, hexagon_field_radius: int, holesSet: set[(int, int)], initial_aspects: set, min_length: int = 0) -> tuple[int, set[tuple[int, int]]]:
        # Алгоритм Дейкстры
        # Для каждой клетки храним минимальное расстояние до неё. Или None, если клетка ещё не посещена

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
        unvisited_nodes: set[PathElement] = set()
        # Создаем все клетки
        for x in range(-hexagon_field_radius, hexagon_field_radius + 1):
            for y in range(-hexagon_field_radius + (abs(x) + 1) // 2, hexagon_field_radius - (abs(x)) // 2 + 1):
                path_elem = PathElement(x, y)
                cells[(x, y)] = path_elem
                unvisited_nodes.add(path_elem)

        # В начальной ставим расстояние 0
        if cells.get(self.coord) is None:
            return DEFAULT_INITIAL_PATH_LEN, set()
        start_cell = cells[self.coord]
        start_cell.dist = 0
        start_cell.path = [self.coord]

        # Пока есть узлы, в которых мы не были
        while len(unvisited_nodes) > 0:
            current_node = min(unvisited_nodes)
            # Получаем список соседей для текущей клетки
            if current_node.coord[0] % 2 == 1:
                cell_neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1)]
            else:
                cell_neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, 1)]
            # Приоритизируем его, чтобы первым делом поиск производился в сторону других аспектов
            def comparator(coord):
                totalDiff = 0
                for initial_aspect in initial_aspects:
                    totalDiff += abs(initial_aspect.coord[0] - coord[0])
                    totalDiff += abs(initial_aspect.coord[1] - coord[1])
                return totalDiff
            cell_neighbours.sort(key=comparator)
            # Приведенный ниже блок кода извлекает соседей текущего узла и обновляет их расстояния.
            for neighbor_direction in cell_neighbours:
                neighbor_coord = (current_node.coord[0] + neighbor_direction[0], current_node.coord[1] + neighbor_direction[1])
                if (neighbor_coord in holesSet) and (neighbor_coord != target_aspect.coord):
                    continue
                neighborNode = cells.get(neighbor_coord, None)
                if neighborNode is None:
                    continue
                tentative_value = current_node.dist + 1
                if neighborNode.coord == target_aspect.coord:
                    if (tentative_value >= min_length) and (tentative_value < neighborNode.dist):
                        neighborNode.dist = tentative_value
                        neighborNode.path = current_node.path + [neighbor_coord]
                else:
                    if tentative_value < neighborNode.dist:
                        neighborNode.dist = tentative_value
                        neighborNode.path = current_node.path + [neighbor_coord]
            unvisited_nodes.remove(current_node)
        return cells[target_aspect.coord].dist, cells[target_aspect.coord].path


def generateLinkMap(existing_aspects: dict[(int, int), str], holes_set: set[(int, int)], available_aspects: set[str]) -> dict[(int, int): str]:
    logging.debug("-----------")
    logging.info("START SOLVING")
    logging.debug("#---0. Setting up:")
    logging.info(f"EXISTING ASPECTS: {existing_aspects}")
    logging.info(f"HOLES HEXAGONS: {holes_set}")
    aspect_recipes = loadRecipesForSelectedVersion()
    available_aspect_recipes: dict[str, list[str, str]] = {}
    for recipe_aspect in aspect_recipes:
        if recipe_aspect in available_aspects:
            available_aspect_recipes[recipe_aspect] = aspect_recipes[recipe_aspect]
    aspect_graph = AspectGraph(available_aspect_recipes)

    result = {}
    initial_aspects: set[Aspect] = set()
    aspects_on_field: set[Aspect] = set()
    maxDistFromCenter = 0

    # Первоначальная обработка входных данных
    for coord, aspectName in existing_aspects.items():
        aspectObject = Aspect(aspectName, coord, set())
        initial_aspects.add(aspectObject)
        aspects_on_field.add(aspectObject)
        aspectObject.linked_to_initials.add(aspectObject)
        result[coord] = aspectName
        distFromCenter = abs(coord[0]) + abs(coord[1]) - abs(coord[0]) // 2
        maxDistFromCenter = max(maxDistFromCenter, distFromCenter)

    hexagon_field_radius = maxDistFromCenter
    logging.debug(f"Hexagon field radius: {hexagon_field_radius}")

    # Продолжаем, пока все изначальные аспекты не будут связаны
    is_all_aspects_linked = False
    iteration_number = 0
    while not is_all_aspects_linked:
        is_all_aspects_linked = True
        # Вывбираем один аспект из изначальных
        for start_initial_aspect in initial_aspects:
            iteration_number += 1
            logging.debug(f"#### Iteration {iteration_number} ####")
            # Получаем, к каким изначальынм аспектам он не привязан
            # Говорим, что хотим привязать его к первому из них
            not_linked_to_aspects = initial_aspects.difference(start_initial_aspect.linked_to_initials)
            logging.debug(f"{start_initial_aspect} not linked to {not_linked_to_aspects}")
            if len(not_linked_to_aspects) == 0:
                continue
            is_all_aspects_linked = False
            min_start_aspect = None
            min_end_aspect = None
            min_end_initial_aspect = None
            min_len_between_aspects = DEFAULT_INITIAL_PATH_LEN
            while len(not_linked_to_aspects) > 0:
                end_initial_aspect = not_linked_to_aspects.pop()
                logging.debug(f"#---1. Found initial aspects to link: {start_initial_aspect} to {end_initial_aspect}")
                # Ищем ближайшие ПО РАССТОЯНИЮ аспекты, связанные с теми, от которого и к которому хотим привязать
                for start_aspect_candidate in aspects_on_field:
                    if start_initial_aspect not in start_aspect_candidate.linked_to_initials:
                        continue
                    for end_aspect_candidate in aspects_on_field:
                        if start_aspect_candidate.coord == end_aspect_candidate.coord:
                            continue
                        if end_initial_aspect not in end_aspect_candidate.linked_to_initials:
                            continue

                        path_len, _ = start_aspect_candidate.get_min_distance_path_to(end_aspect_candidate, hexagon_field_radius, holes_set, initial_aspects)
                        if path_len < min_len_between_aspects:
                            min_start_aspect = start_aspect_candidate
                            min_end_aspect = end_aspect_candidate
                            min_end_initial_aspect = end_initial_aspect
                            min_len_between_aspects = path_len
            if min_len_between_aspects > MAX_PATH_LEN:
                logging.error(f"Warning: Cell with aspect {start_initial_aspect} is unreachable from any other aspects")
                return existing_aspects

            logging.debug(f"Min distance {min_len_between_aspects} found from aspect: {min_start_aspect} to aspect: {min_end_aspect}")
            # К выбранному аспекту пытаемся построить цепочки. Сначала самую короткую, потом всё длиннее
            end_initial_aspect = min_end_initial_aspect
            end_aspect = min_end_aspect
            start_aspect = min_start_aspect
            target_path_len = min_len_between_aspects
            logging.debug(f"#---2. Trying to found aspects path from {start_aspect.name} to {end_aspect.name}")
            while target_path_len < MAX_PATH_LEN:
                aspects_path = aspect_graph.find_path(start_aspect.name, end_aspect.name, target_path_len)
                if not aspects_path:
                    logging.debug(f"Path with len {target_path_len} not found")
                    target_path_len += 1
                    continue
                logging.debug(f"Path with len: {target_path_len} generated: {aspects_path}")
                # Если цепочка найдена, пытаемся пройти найти маршрут заданной длины
                logging.debug(f"#---3. Trying to find coordinates path with len {target_path_len} from {start_aspect} to {end_aspect}")
                all_holes_set = holes_set | set(map(lambda asp: asp.coord, aspects_on_field))
                min_len_between_aspects, coordsPath = start_aspect.get_min_distance_path_to(end_aspect, hexagon_field_radius, all_holes_set, initial_aspects, target_path_len)
                if min_len_between_aspects > MAX_PATH_LEN:
                    logging.debug(f"Coordinates path with len {target_path_len} not found")
                    target_path_len += 1
                    continue
                logging.debug(f"Coordinates path found: {coordsPath}")

                logging.debug("#---4. Fill gotten aspects and prepare to next step")
                # Объединяем linked_to, и записываем в оба исходых аспекта один и тот же этот список)
                all_added_aspects = set()
                for i in range(1, target_path_len):
                    result[coordsPath[i]] = aspects_path[i]
                    addedAspect = Aspect(aspects_path[i], coordsPath[i], start_initial_aspect.linked_to_initials)
                    aspects_on_field.add(addedAspect)
                    all_added_aspects.add(addedAspect)
                start_initial_aspect.linked_to_initials.update(end_initial_aspect.linked_to_initials)

                # Recursive update all aspects that linked to this
                visited_initials = set()
                def update_all_linked_aspects(from_initial):
                    if from_initial in visited_initials:
                        return
                    from_initial.linked_to_initials.update(start_initial_aspect.linked_to_initials)
                    visited_initials.add(from_initial)
                    for initial_aspect in from_initial.linked_to_initials:
                        update_all_linked_aspects(initial_aspect)
                update_all_linked_aspects(end_initial_aspect)
                logging.debug(f"Aspects {visited_initials} is now linked between themselves")

                logging.debug(f"Aspect path putted on field. Total aspects: {aspects_on_field}")
                logging.debug("Iteration finished.")
                break
            if target_path_len == MAX_PATH_LEN:
                logging.error(f"Error: Path from {start_aspect} to {end_aspect} cannot be generated")
                return existing_aspects
    logging.info(f"Final solving: {result}")
    return result

