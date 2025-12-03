# Advent of Code 2016 - Day 11
# Radioisotope Thermoelectric Generators
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — описания этажей вида:
# The first floor contains a promethium generator and a promethium-compatible microchip.
# ...
#
# Ответ: минимальное количество ходов, чтобы все предметы оказались на верхнем этаже.

from pathlib import Path
import re
from collections import deque


NUM_FLOORS = 4  # этажи 0..3


def _parse_input(data: str):
    """
    Парсим текстовое описание этажей в словарь:
      element -> {'G': floor, 'M': floor}
    где floor = 0..3.
    """
    floor_names = {
        "first": 0,
        "second": 1,
        "third": 2,
        "fourth": 3,
    }

    elements = {}  # name -> {'G': floor, 'M': floor}

    for line in data.splitlines():
        line = line.strip().rstrip(".")
        if not line:
            continue
        if "contains nothing relevant" in line:
            # на этаже нет предметов
            continue

        # Пример: "The first floor contains ..."
        m_floor = re.match(r"The (\w+) floor contains (.+)", line)
        if not m_floor:
            continue  # или raise, но вход AoC нормализован
        floor_word, rest = m_floor.groups()
        floor = floor_names[floor_word]

        # Находим все микросхемы и генераторы
        # ... a thulium generator ...
        # ... a thulium-compatible microchip ...
        gens = re.findall(r"(\w+) generator", rest)
        chips = re.findall(r"(\w+)-compatible microchip", rest)

        for name in gens:
            el = elements.setdefault(name, {})
            el["G"] = floor
        for name in chips:
            el = elements.setdefault(name, {})
            el["M"] = floor

    # Преобразуем в два списка половинок: g_floors[i], m_floors[i]
    # i соответствует какому-то элементу, порядок зафиксируем (sort по имени)
    element_names = sorted(elements.keys())
    g_floors = []
    m_floors = []

    for name in element_names:
        info = elements[name]
        if "G" not in info or "M" not in info:
            raise ValueError(f"Элемент {name!r} не имеет пары G/M полностью в описании")
        g_floors.append(info["G"])
        m_floors.append(info["M"])

    return g_floors, m_floors


def _build_initial_state(data: str, extra_pairs_for_part2: bool):
    """
    Строит начальное состояние:
      elevator_floor: int
      items: tuple[int] длиной 2N, по схеме:
        (g0, m0, g1, m1, ..., g(N-1), m(N-1))
    Если extra_pairs_for_part2=True — добавляет две пары (elerium, dilithium)
    оба на первом этаже (floor 0) поверх исходных.
    """
    g_floors, m_floors = _parse_input(data)

    if extra_pairs_for_part2:
        # Добавляем elerium и dilithium на первый этаж
        # Элементам не нужны имена, нам важны только пары позиций.
        g_floors.extend([0, 0])
        m_floors.extend([0, 0])

    items = []
    for g, m in zip(g_floors, m_floors):
        items.append(g)
        items.append(m)

    elevator = 0  # по условию лифт стартует на первом этаже
    elevator, items_tuple = _canonicalize(elevator, tuple(items))
    return elevator, items_tuple


def _canonicalize(elevator: int, items: tuple[int, ...]):
    """
    Канонизируем состояние:
      - пары (G_i, M_i) сортируем по значениям этажей, чтобы
        перестановка типов элементов не давала новых уникальных состояний.
    Возвращаем (elevator, canonical_items).
    """
    n_pairs = len(items) // 2
    pairs = []
    for i in range(n_pairs):
        g = items[2 * i]
        m = items[2 * i + 1]
        pairs.append((g, m))

    # сортируем пары по (g, m)
    pairs.sort()
    flat = []
    for g, m in pairs:
        flat.append(g)
        flat.append(m)

    return elevator, tuple(flat)


def _is_valid(items: tuple[int, ...]) -> bool:
    """
    Проверяет корректность состояния:
      - ни одна микросхема не "сгорит".
    """
    n_pairs = len(items) // 2

    for floor in range(NUM_FLOORS):
        gens_on_floor = set(
            i for i in range(n_pairs) if items[2 * i] == floor
        )
        if not gens_on_floor:
            # генераторов нет, все микросхемы на этом этаже безопасны
            continue

        # есть хотя бы один генератор, любая микросхема без своего генератора здесь сгорит
        for i in range(n_pairs):
            chip_floor = items[2 * i + 1]
            if chip_floor == floor and i not in gens_on_floor:
                return False

    return True


def _bfs_min_steps(elevator: int, items: tuple[int, ...]) -> int:
    """
    BFS по пространству состояний, возвращает минимальное количество шагов,
    чтобы все предметы оказались на верхнем этаже.
    """
    start_state = (elevator, items)
    start_state = _canonicalize(*start_state)
    start_elev, start_items = start_state

    # Быстрый тест цели: все предметы на самом верхнем этаже
    def is_goal(it: tuple[int, ...]) -> bool:
        return all(f == NUM_FLOORS - 1 for f in it)

    if is_goal(start_items):
        return 0

    visited = set()
    visited.add(start_state)

    queue = deque()
    queue.append((start_elev, start_items, 0))  # (elevator, items, steps)

    while queue:
        elev, items, steps = queue.popleft()

        if is_goal(items):
            return steps

        n_items = len(items)
        min_floor = min(items)

        # Какие предметы находятся на текущем этаже лифта
        present_indices = [i for i, f in enumerate(items) if f == elev]

        # Формируем набор перемещений: сначала пары, потом одиночные
        move_combos = []

        # два предмета
        for i in range(len(present_indices)):
            for j in range(i + 1, len(present_indices)):
                move_combos.append((present_indices[i], present_indices[j]))
        # один предмет
        for i in range(len(present_indices)):
            move_combos.append((present_indices[i],))

        # Возможные направления лифта
        for direction in (1, -1):
            new_elev = elev + direction
            if not (0 <= new_elev < NUM_FLOORS):
                continue

            # Не спускаемся ниже нижнего занятого этажа — это бессмысленно
            if direction == -1 and elev == min_floor:
                continue

            for combo in move_combos:
                new_items = list(items)
                for idx in combo:
                    new_items[idx] = new_elev

                new_items_t = tuple(new_items)
                if not _is_valid(new_items_t):
                    continue

                new_state = _canonicalize(new_elev, new_items_t)
                if new_state in visited:
                    continue

                visited.add(new_state)
                queue.append((new_state[0], new_state[1], steps + 1))

    # Теоретически не должно происходить для корректного входа AoC
    raise RuntimeError("Не удалось достичь целевого состояния")


def solve_part1(data: str) -> int:
    """
    Part 1:
    Минимальное количество ходов, чтобы все элементы оказались на верхнем этаже,
    для исходной конфигурации.
    """
    elevator, items = _build_initial_state(data, extra_pairs_for_part2=False)
    return _bfs_min_steps(elevator, items)


def solve_part2(data: str) -> int:
    """
    Part 2:
    То же, но добавляем на первый этаж:
      - elerium generator + elerium-compatible microchip
      - dilithium generator + dilithium-compatible microchip
    """
    elevator, items = _build_initial_state(data, extra_pairs_for_part2=True)
    return _bfs_min_steps(elevator, items)


def main():
    # Локальный запуск: читаем input.txt из текущей папки
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()

