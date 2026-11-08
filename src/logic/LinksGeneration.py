import heapq
import itertools
import logging

from configs.constants import MAX_ASPECTS_SOLVING_PATH_LEN
from utils import AppState

INF_PATH_LEN = 999999
CYCLE_COST = 10 ** 6
ROUTE_ENUMERATION_MAX_POP_COUNT = 100_000
ROUTE_ENUMERATION_MAX_YIELD_COUNT = 5_000

'''
Описание работы алгоритма:

0. Из рецептов доступных аспектов строится граф соединяемости: аспекты соединимы,
   если один является компонентом другого. Каждому аспекту сопоставляется
   стоимость — количество базовых аспектов, необходимых для синтеза одной штуки.

1. Пока есть несвязанные между собой изначальные аспекты:
1.1. Берём изначальный аспект и изначальный аспект, с которым он ещё не связан.
1.2. Из всех аспектов на поле выбираем ближайшую пару: стартовый (связанный с первым)
     и целевой (связанный со вторым). Расстояние — обход поля в ширину.

2. Ищем способ соединить выбранную пару:
2.1. Маршруты по полю перебираются в порядке (длина, количество новых аспектов);
     через уже стоящие на поле аспекты маршрут проходит бесплатно (переиспользование).
2.2. Для каждого маршрута ищется цепочка аспектов той же длины из графа рецептов,
     уважающая стоящие на маршруте аспекты и минимальная по суммарной стоимости
     (динамическое программирование — полный перебор среди равных по длине).
2.3. Первый маршрут, для которого нашлась цепочка, и используется.

3. Раскладываем цепочку по маршруту (стоящие аспекты переиспользуем бесплатно),
   объединяем группы связанности изначальных аспектов.

4. Заканчиваем, когда все изначальные аспекты связаны друг с другом.
'''


class AspectGraph:
    graph: dict[str, set[str]]
    aspects_cost: dict[str, int]

    def __init__(self, aspect_recipes: dict[str, list[str]]):
        self.graph = {}
        self.aspects_cost = {}
        self.regenerate_graph_combinations(aspect_recipes)

    def regenerate_graph_combinations(self, aspect_recipes: dict[str, list[str]]):
        self.graph.clear()
        for aspect_name, recipe in aspect_recipes.items():
            for component in recipe:
                if component in aspect_recipes:
                    self.add_connection(aspect_name, component)
        self._compute_aspects_cost(aspect_recipes)

    def add_connection(self, aspect1, aspect2):
        if aspect1 not in self.graph:
            self.graph[aspect1] = set()
        if aspect2 not in self.graph:
            self.graph[aspect2] = set()
        self.graph[aspect1].add(aspect2)
        self.graph[aspect2].add(aspect1)

    def _compute_aspects_cost(self, aspect_recipes: dict[str, list[str]]):
        visiting = set()

        def cost_of(aspect_name: str) -> int:
            if aspect_name in self.aspects_cost:
                return self.aspects_cost[aspect_name]
            recipe = aspect_recipes.get(aspect_name)
            if not recipe or len(recipe) < 2:
                self.aspects_cost[aspect_name] = 1
                return 1
            if aspect_name in visiting:
                logging.error(f"Cycle detected in aspects recipes on aspect '{aspect_name}'")
                return CYCLE_COST
            visiting.add(aspect_name)
            cost = sum(cost_of(component) for component in recipe[:2])
            visiting.discard(aspect_name)
            self.aspects_cost[aspect_name] = cost
            return cost

        for aspect_name in aspect_recipes:
            cost_of(aspect_name)

    def find_path(self, from_aspect: str, to_aspect: str, steps: int,
                  fixed_positions: dict[int, str] | None = None) -> list[str] | None:
        fixed_positions = fixed_positions or {}
        dp: list[dict[str, tuple[int, str]]] = [{from_aspect: (0, None)}]
        for i in range(1, steps + 1):
            layer = {}
            required_aspect = fixed_positions.get(i)
            is_last = i == steps
            for node, (cost, _) in dp[-1].items():
                for neighbor in sorted(self.graph.get(node, ())):
                    if required_aspect is not None and neighbor != required_aspect:
                        continue
                    added_cost = 0 if (is_last or required_aspect is not None) \
                        else self.aspects_cost.get(neighbor, 0)
                    new_cost = cost + added_cost
                    if neighbor not in layer or new_cost < layer[neighbor][0]:
                        layer[neighbor] = (new_cost, node)
            dp.append(layer)
        if to_aspect not in dp[steps]:
            return None
        chain = [to_aspect]
        current = to_aspect
        for i in range(steps, 0, -1):
            current = dp[i][current][1]
            chain.append(current)
        return list(reversed(chain))

    def __repr__(self):
        return f"AspectsGraph(graph={self.graph})"


class Aspect:
    name: str
    coord: tuple[int, int]
    linked_to_initials: set

    def __init__(self, name, coord, linked_to_initials):
        self.name = name
        self.coord = coord
        self.linked_to_initials = linked_to_initials

    def __repr__(self):
        return f"{self.name}{self.coord}"

    def get_cell_neighbours(self, coord: tuple[int, int]) -> tuple[tuple[int, int], ...]:
        if coord[0] % 2 == 1:
            return (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1)
        return (-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, 1)

    def iter_routes_to(
            self,
            target_aspect,
            hexagon_field_radius: int,
            holes_set: set[tuple[int, int]],
            passable_aspects: dict[tuple[int, int], str] | None = None,
            interruptingFlag: list[bool] | None = None,
    ):
        passable_aspects = passable_aspects or {}
        cells = set()
        for x in range(-hexagon_field_radius, hexagon_field_radius + 1):
            for y in range(-hexagon_field_radius + (abs(x) + 1) // 2, hexagon_field_radius - (abs(x)) // 2 + 1):
                cells.add((x, y))
        if self.coord not in cells or target_aspect.coord not in cells:
            return
        blocked = holes_set | {self.coord}

        counter = itertools.count()
        heap = [(0, 0, next(counter), (self.coord,))]
        pop_count = 0
        yield_count = 0
        while heap:
            if interruptingFlag and interruptingFlag[0]:
                return
            dist, placed, _, path = heapq.heappop(heap)
            pop_count += 1
            if pop_count > ROUTE_ENUMERATION_MAX_POP_COUNT:
                logging.error(f"Route enumeration budget exceeded: {self.coord} -> {target_aspect.coord}")
                return
            coord = path[-1]
            if coord == target_aspect.coord:
                yield_count += 1
                if yield_count > ROUTE_ENUMERATION_MAX_YIELD_COUNT:
                    logging.error(f"Route enumeration yield budget exceeded: {self.coord} -> {target_aspect.coord}")
                    return
                fixed_positions = {
                    i: passable_aspects[cell]
                    for i, cell in enumerate(path)
                    if 0 < i < len(path) - 1 and cell in passable_aspects
                }
                yield dist, path, fixed_positions
                continue
            if dist + 1 >= MAX_ASPECTS_SOLVING_PATH_LEN:
                continue
            for dx, dy in self.get_cell_neighbours(coord):
                neighbor_coord = (coord[0] + dx, coord[1] + dy)
                if neighbor_coord in path:
                    continue
                if neighbor_coord in blocked and neighbor_coord != target_aspect.coord:
                    continue
                if neighbor_coord not in cells:
                    continue
                neighbor_placed = placed + (0 if neighbor_coord in passable_aspects else 1)
                heapq.heappush(heap, (dist + 1, neighbor_placed, next(counter), path + (neighbor_coord,)))


def generateLinkMap(existing_aspects: dict[tuple[int, int], str], holes_set: set[tuple[int, int]],
                    available_aspects: set[str], interruptingFlag: list[bool]) -> dict[tuple[int, int], str] | None:
    logging.debug("-----------")
    logging.info("START SOLVING")
    logging.debug("#---0. Setting up:")
    logging.info(f"EXISTING ASPECTS: {existing_aspects}")
    logging.info(f"HOLES HEXAGONS: {holes_set}")
    aspect_recipes = AppState.aspectRecipes
    available_aspect_recipes: dict[str, list[str]] = {
        aspect_name: recipe
        for aspect_name, recipe in aspect_recipes.items()
        if aspect_name in available_aspects
    }
    aspect_graph = AspectGraph(available_aspect_recipes)

    result = dict(existing_aspects)
    initial_aspects: set[Aspect] = set()
    aspects_on_field: set[Aspect] = set()
    max_dist_from_center = 0

    # Первоначальная обработка входных данных
    for coord, aspect_name in existing_aspects.items():
        aspect_object = Aspect(aspect_name, coord, set())
        aspect_object.linked_to_initials.add(aspect_object)
        initial_aspects.add(aspect_object)
        aspects_on_field.add(aspect_object)
        dist_from_center = abs(coord[0]) + abs(coord[1]) - abs(coord[0]) // 2
        max_dist_from_center = max(max_dist_from_center, dist_from_center)

    hexagon_field_radius = max_dist_from_center
    logging.debug(f"Hexagon field radius: {hexagon_field_radius}")

    def get_field_aspect_by_coord(coord: tuple[int, int]) -> Aspect | None:
        for aspect in aspects_on_field:
            if aspect.coord == coord:
                return aspect
        return None

    def merge_linked_groups(aspect_a: Aspect, aspect_b: Aspect) -> None:
        # Объединяет группы связанности двух аспектов, обновляя все изначальные аспекты групп
        aspect_a.linked_to_initials.update(aspect_b.linked_to_initials)
        visited_initials = set()

        def propagate(from_initial):
            if from_initial in visited_initials or interruptingFlag[0]:
                return
            from_initial.linked_to_initials.update(aspect_a.linked_to_initials)
            visited_initials.add(from_initial)
            for initial_aspect in from_initial.linked_to_initials:
                propagate(initial_aspect)

        propagate(aspect_b)
        logging.debug(f"Aspects {visited_initials} is now linked between themselves")

    # Продолжаем, пока все изначальные аспекты не будут связаны
    is_all_aspects_linked = False
    iteration_number = 0
    while not is_all_aspects_linked and not interruptingFlag[0]:
        is_all_aspects_linked = True
        # Выбираем один аспект из изначальных
        for start_initial_aspect in sorted(initial_aspects, key=lambda a: (a.coord, a.name)):
            iteration_number += 1
            logging.debug(f"#### Iteration {iteration_number} ####")
            # Получаем, к каким изначальным аспектам он не привязан
            not_linked_to_aspects = initial_aspects.difference(start_initial_aspect.linked_to_initials)
            logging.debug(f"{start_initial_aspect} not linked to {not_linked_to_aspects}")
            if len(not_linked_to_aspects) == 0:
                continue
            is_all_aspects_linked = False

            field_aspects_passable = {aspect.coord: aspect.name for aspect in aspects_on_field}
            min_start_aspect = None
            min_end_aspect = None
            min_end_initial_aspect = None
            min_len_between_aspects = INF_PATH_LEN
            # Говорим, что хотим привязать его к каждому из них по очереди
            for end_initial_aspect in sorted(not_linked_to_aspects, key=lambda a: (a.coord, a.name)):
                if interruptingFlag[0]:
                    break
                logging.debug(f"#---1. Found initial aspects to link: {start_initial_aspect} to {end_initial_aspect}")
                # Ищем ближайшие ПО РАССТОЯНИЮ аспекты, связанные с теми, от которого и к которому хотим привязать
                for start_aspect_candidate in sorted(aspects_on_field, key=lambda a: (a.coord, a.name)):
                    if start_initial_aspect not in start_aspect_candidate.linked_to_initials:
                        continue
                    for end_aspect_candidate in sorted(aspects_on_field, key=lambda a: (a.coord, a.name)):
                        if start_aspect_candidate.coord == end_aspect_candidate.coord:
                            continue
                        if end_initial_aspect not in end_aspect_candidate.linked_to_initials:
                            continue
                        passable = {coord: name for coord, name in field_aspects_passable.items()
                                    if coord not in (start_aspect_candidate.coord, end_aspect_candidate.coord)}
                        route = next(start_aspect_candidate.iter_routes_to(
                            end_aspect_candidate, hexagon_field_radius, holes_set, passable_aspects=passable), None)
                        if route is None:
                            continue
                        path_len = route[0]
                        if path_len < min_len_between_aspects:
                            min_start_aspect = start_aspect_candidate
                            min_end_aspect = end_aspect_candidate
                            min_end_initial_aspect = end_initial_aspect
                            min_len_between_aspects = path_len
            if min_len_between_aspects > MAX_ASPECTS_SOLVING_PATH_LEN:
                logging.error(f"Warning: Cell with aspect {start_initial_aspect} is unreachable from any other aspects")
                return existing_aspects

            logging.debug(f"Min distance {min_len_between_aspects} found from aspect: {min_start_aspect} to aspect: {min_end_aspect}")
            end_initial_aspect = min_end_initial_aspect
            end_aspect = min_end_aspect
            start_aspect = min_start_aspect
            passable = {coord: name for coord, name in field_aspects_passable.items()
                        if coord not in (start_aspect.coord, end_aspect.coord)}

            solved = False
            routes = start_aspect.iter_routes_to(
                end_aspect, hexagon_field_radius, holes_set,
                passable_aspects=passable, interruptingFlag=interruptingFlag)
            for route_len, coords_path, fixed_positions in routes:
                logging.debug(f"#---2. Route with len {route_len} found: {coords_path}. Trying to find aspects chain "
                              f"from {start_aspect.name} to {end_aspect.name}")
                aspects_chain = aspect_graph.find_path(start_aspect.name, end_aspect.name, route_len, fixed_positions)
                if aspects_chain is None:
                    logging.debug(f"Aspects chain with len {route_len} not found for route {coords_path}")
                    continue
                logging.debug(f"Aspects chain generated: {aspects_chain}")

                logging.debug("#---3. Fill gotten aspects and prepare to next step")
                merged_initials = set(start_initial_aspect.linked_to_initials) | set(end_initial_aspect.linked_to_initials)
                touched_aspects = []
                for i in range(1, route_len):
                    coord = coords_path[i]
                    aspect_name = aspects_chain[i]
                    reused_aspect = get_field_aspect_by_coord(coord)
                    if reused_aspect is not None:
                        if reused_aspect.name != aspect_name:
                            logging.error(
                                f"Route aspect mismatch at {coord}: field has {reused_aspect.name}, chain needs {aspect_name}")
                            return None
                        reused_aspect.linked_to_initials.update(merged_initials)
                        touched_aspects.append(reused_aspect)
                        continue
                    result[coord] = aspect_name
                    added_aspect = Aspect(aspect_name, coord, merged_initials)
                    aspects_on_field.add(added_aspect)
                    touched_aspects.append(added_aspect)

                merge_linked_groups(start_initial_aspect, end_initial_aspect)
                for aspect in touched_aspects:
                    aspect.linked_to_initials.update(start_initial_aspect.linked_to_initials)
                solved = True
                logging.debug(f"Aspect path putted on field. Total aspects: {aspects_on_field}")
                logging.debug("Iteration finished.")
                break
            if not solved and not interruptingFlag[0]:
                logging.error(f"Error: Path from {start_aspect} to {end_aspect} cannot be generated")
                return None
    logging.info(f"Final solving: {result}")
    return result
