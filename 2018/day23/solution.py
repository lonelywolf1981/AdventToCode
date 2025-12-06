from __future__ import annotations

from pathlib import Path
import heapq
import re
from typing import List, Tuple


Bot = Tuple[int, int, int, int]  # x, y, z, r


# ----------------------------------------------------
#   Парсер входных данных
# ----------------------------------------------------

def parse_input(data: str) -> List[Bot]:
    bots: List[Bot] = []
    pattern = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>,\s*r=(\d+)")
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if not m:
            continue
        x, y, z, r = map(int, m.groups())
        bots.append((x, y, z, r))
    return bots


def manhattan(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


# ----------------------------------------------------
#   Part 1
# ----------------------------------------------------

def solve_part1(data: str) -> str:
    bots = parse_input(data)
    if not bots:
        return "0"

    # Бот с максимальным радиусом
    strongest = max(bots, key=lambda b: b[3])
    sx, sy, sz, sr = strongest

    count = 0
    for x, y, z, r in bots:
        if manhattan((x, y, z), (sx, sy, sz)) <= sr:
            count += 1

    return str(count)


# ----------------------------------------------------
#   Part 2 — поиск точки с макс. количеством ботов
#   Используем поиск по кубам (branch & bound) + очередь
# ----------------------------------------------------

def bots_in_range_of_cube(bots: List[Bot], cx: int, cy: int, cz: int, size: int) -> int:
    """
    Считаем, сколько ботов пересекают куб:
    куб с углом (cx,cy,cz) и ребром size (включительно [cx,cx+size-1]).
    """
    count = 0
    max_x = cx + size - 1
    max_y = cy + size - 1
    max_z = cz + size - 1

    for x, y, z, r in bots:
        dx = 0
        if x < cx:
            dx = cx - x
        elif x > max_x:
            dx = x - max_x

        dy = 0
        if y < cy:
            dy = cy - y
        elif y > max_y:
            dy = y - max_y

        dz = 0
        if z < cz:
            dz = cz - z
        elif z > max_z:
            dz = z - max_z

        if dx + dy + dz <= r:
            count += 1
    return count


def cube_min_distance_to_origin(cx: int, cy: int, cz: int, size: int) -> int:
    """
    Минимальная манхэттен-дистанция от любой точки куба до (0,0,0).
    """
    max_x = cx + size - 1
    max_y = cy + size - 1
    max_z = cz + size - 1

    def axis_dist(a_min: int, a_max: int) -> int:
        # диапазон полностью справа от 0
        if a_min > 0:
            return a_min
        # диапазон полностью слева от 0
        if a_max < 0:
            return -a_max
        # 0 внутри диапазона
        return 0

    return axis_dist(cx, max_x) + axis_dist(cy, max_y) + axis_dist(cz, max_z)


def solve_part2(data: str) -> str:
    bots = parse_input(data)
    if not bots:
        return "0"

    # Находим границы по координатам
    xs = [b[0] for b in bots]
    ys = [b[1] for b in bots]
    zs = [b[2] for b in bots]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    # Строим исходный куб, который покрывает всех ботов.
    size = 1
    max_span = max(max_x - min_x, max_y - min_y, max_z - min_z)
    while size <= max_span:
        size <<= 1

    # Начальный куб (min_x..min_x+size-1 и т.д.)
    start_cube = (min_x, min_y, min_z, size)

    # Очередь с приоритетом:
    #   (-count_bots, distance_to_origin, size, x, y, z)
    heap = []

    cx, cy, cz, s = start_cube
    cnt = bots_in_range_of_cube(bots, cx, cy, cz, s)
    dist0 = cube_min_distance_to_origin(cx, cy, cz, s)
    heapq.heappush(heap, (-cnt, dist0, s, cx, cy, cz))

    while heap:
        neg_count, dist, size, cx, cy, cz = heapq.heappop(heap)
        count = -neg_count

        # Если размер куба 1 — это точка, возвращаем её расстояние от (0,0,0)
        if size == 1:
            # точка с координатами (cx,cy,cz)
            return str(abs(cx) + abs(cy) + abs(cz))

        # Иначе делим куб на 8 меньших кубиков (размер size//2)
        half = size // 2
        for dx in (0, half):
            for dy in (0, half):
                for dz in (0, half):
                    nx = cx + dx
                    ny = cy + dy
                    nz = cz + dz
                    sub_count = bots_in_range_of_cube(bots, nx, ny, nz, half)
                    if sub_count == 0:
                        continue
                    sub_dist = cube_min_distance_to_origin(nx, ny, nz, half)
                    heapq.heappush(heap, (-sub_count, sub_dist, half, nx, ny, nz))

    # На всякий случай, если очередь опустела (не должно быть)
    return "0"


# ----------------------------------------------------
#   Прямой запуск
# ----------------------------------------------------

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
