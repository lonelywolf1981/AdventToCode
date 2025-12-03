# Advent of Code 2016 - Day 24
# Air Duct Spelunking
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — карта из символов:
# # . 0-9
# Пример:
# ###########
# #0.1.....2#
# #.#######.#
# #4.......3#
# ###########

from pathlib import Path
from collections import deque
from itertools import permutations


def _parse_map(data: str):
    """
    Парсим карту:
      - grid: список строк
      - pois: dict[digit_char] = (x, y)
    """
    grid = [list(line.rstrip("\n")) for line in data.splitlines() if line.strip()]
    pois = {}
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch.isdigit():
                pois[ch] = (x, y)
    return grid, pois


def _bfs_distances_from(grid, start):
    """
    BFS от одной точки.
    start: (x, y)
    Возвращает словарь {(x, y): расстояние}
    """
    width = len(grid[0])
    height = len(grid)
    sx, sy = start
    dist = { (sx, sy): 0 }
    q = deque([(sx, sy)])

    while q:
        x, y = q.popleft()
        d = dist[(x, y)]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if grid[ny][nx] == '#':
                continue
            if (nx, ny) in dist:
                continue
            dist[(nx, ny)] = d + 1
            q.append((nx, ny))
    return dist


def _build_distance_matrix(grid, pois):
    """
    Строим матрицу расстояний между всеми цифрами.
    Возвращаем:
      - labels: отсортированный список символов цифр (например ['0','1','2','3'])
      - dist_map: dict[(a, b)] = расстояние между цифрами 'a' и 'b'
    """
    labels = sorted(pois.keys(), key=int)
    dist_map = {}

    # для каждой точки делаем BFS и берём расстояния до остальных
    for a in labels:
        dists = _bfs_distances_from(grid, pois[a])
        for b in labels:
            if a == b:
                continue
            ax, ay = pois[a]
            bx, by = pois[b]
            dist_map[(a, b)] = dists[(bx, by)]
    return labels, dist_map


def solve_part1(data: str) -> int:
    """
    Part 1:
    Кратчайший путь, стартуя в '0', посетить все остальные цифры хотя бы по разу.
    Возвращает длину маршрута.
    """
    grid, pois = _parse_map(data)
    labels, dist_map = _build_distance_matrix(grid, pois)

    start = '0'
    others = [lbl for lbl in labels if lbl != start]

    best = None

    for order in permutations(others):
        # маршрут: 0 -> order[0] -> order[1] -> ... -> order[-1]
        path = (start,) + order
        total = 0
        ok = True
        for a, b in zip(path, path[1:]):
            d = dist_map.get((a, b))
            if d is None:
                ok = False
                break
            total += d
        if not ok:
            continue
        if best is None or total < best:
            best = total

    return best if best is not None else 0


def solve_part2(data: str) -> int:
    """
    Part 2:
    То же, но маршрут должен вернуться в '0':
      0 -> ... -> last -> 0
    Возвращает длину маршрута.
    """
    grid, pois = _parse_map(data)
    labels, dist_map = _build_distance_matrix(grid, pois)

    start = '0'
    others = [lbl for lbl in labels if lbl != start]

    best = None

    for order in permutations(others):
        # маршрут: 0 -> ... -> last -> 0
        path = (start,) + order + (start,)
        total = 0
        ok = True
        for a, b in zip(path, path[1:]):
            d = dist_map.get((a, b))
            if d is None:
                ok = False
                break
            total += d
        if not ok:
            continue
        if best is None or total < best:
            best = total

    return best if best is not None else 0


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
