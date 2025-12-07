from pathlib import Path
from collections import defaultdict, deque


def parse_bricks(data: str):
    bricks = []
    for line in data.strip().splitlines():
        left, right = line.split("~")
        x1, y1, z1 = map(int, left.split(","))
        x2, y2, z2 = map(int, right.split(","))
        # нормализуем так, чтобы x1<=x2, y1<=y2, z1<=z2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if z1 > z2:
            z1, z2 = z2, z1
        bricks.append((x1, y1, z1, x2, y2, z2))
    return bricks


def footprint_cells(brick):
    """Возвращает список (x,y) ячеек в проекции кирпича на плоскость XY."""
    x1, y1, _z1, x2, y2, _z2 = brick
    cells = []
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            cells.append((x, y))
    return cells


def settle_bricks(bricks):
    """
    Осаживает кирпичи вниз по Z, строит граф опор.
    Возвращает:
      - new_bricks: список новых координат (после падения)
      - supports:  dict[int, set[int]]  — кого кирпич i держит сверху
      - supported_by: dict[int, set[int]] — на ком стоит кирпич i
    """

    n = len(bricks)

    # Индексы кирпичей, отсортированные по нижней координате z1
    order = sorted(range(n), key=lambda i: bricks[i][2])

    # Для каждой колонки (x,y) храним (top_z, brick_index),
    # то есть на какой высоте сейчас стоит верхний кирпич и кто это.
    col_top = defaultdict(lambda: (0, None))  # z=0 — "пол" (z=1 будет над ним)

    new_bricks = list(bricks)
    supports = {i: set() for i in range(n)}
    supported_by = {i: set() for i in range(n)}

    for i in order:
        x1, y1, z1, x2, y2, z2 = new_bricks[i]
        cells = footprint_cells(new_bricks[i])
        height = z2 - z1  # "высота" кирпича (включая все слои -1, поэтому просто разность)

        # Находим максимально высокий "пол" под этим кирпичом
        max_support_z = 0
        for (x, y) in cells:
            sz, _b = col_top[(x, y)]
            if sz > max_support_z:
                max_support_z = sz

        # Новый диапазон по Z
        new_z1 = max_support_z + 1
        new_z2 = new_z1 + height
        new_bricks[i] = (x1, y1, new_z1, x2, y2, new_z2)

        # Определяем, какие кирпичи именно его держат:
        # это те кирпичи, у которых верх как раз на max_support_z под одной из клеток
        supporters = set()
        for (x, y) in cells:
            sz, b = col_top[(x, y)]
            if sz == max_support_z and b is not None:
                supporters.add(b)

        supported_by[i] = supporters
        for b in supporters:
            supports[b].add(i)

        # Теперь этот кирпич становится верхним для всех своих ячеек
        for (x, y) in cells:
            col_top[(x, y)] = (new_z2, i)

    return new_bricks, supports, supported_by


def solve_part1(data: str) -> str:
    bricks = parse_bricks(data)
    new_bricks, supports, supported_by = settle_bricks(bricks)

    safe_count = 0
    n = len(new_bricks)

    for i in range(n):
        # кирпич i безопасен, если каждый, кто на нём стоит,
        # имеет как минимум 2 опоры (т.е. останется ещё на ком стоять)
        ok = True
        for above in supports[i]:
            if len(supported_by[above]) == 1:  # только i держит above
                ok = False
                break
        if ok:
            safe_count += 1

    return str(safe_count)


def count_chain_reaction(start, supports, supported_by) -> int:
    """
    Считает, сколько кирпичей упадёт, если убрать кирпич `start`.
    Сам start в количестве не учитываем (вернём только "других").
    """
    fallen = set([start])
    q = deque([start])

    while q:
        b = q.popleft()
        for above in supports[b]:
            if above in fallen:
                continue
            # кирпич above падает, если у него НЕ осталось ни одной опоры
            if all(s in fallen for s in supported_by[above]):
                fallen.add(above)
                q.append(above)

    return len(fallen) - 1  # не считаем исходный start


def solve_part2(data: str) -> str:
    bricks = parse_bricks(data)
    new_bricks, supports, supported_by = settle_bricks(bricks)

    total = 0
    n = len(new_bricks)
    for i in range(n):
        total += count_chain_reaction(i, supports, supported_by)

    return str(total)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
