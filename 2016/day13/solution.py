# Advent of Code 2016 - Day 13
# A Maze of Twisty Little Cubicles
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — одно целое число: favorite number.

from pathlib import Path
from collections import deque


def _get_favorite(data: str) -> int:
    """
    Берём первое целое число из входа как favorite number.
    """
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        return int(line)
    raise ValueError("Favorite number not found in input")


def _is_open(x: int, y: int, favorite: int) -> bool:
    """
    True если клетка (x, y) — свободна, False если стена.
    """
    if x < 0 or y < 0:
        return False
    v = x * x + 3 * x + 2 * x * y + y + y * y + favorite
    ones = bin(v).count("1")
    return ones % 2 == 0  # чётное -> open


def _neighbors(x: int, y: int):
    """
    4-соседей (вверх/вниз/влево/вправо).
    """
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def solve_part1(data: str) -> int:
    """
    Part 1:
    Минимальное число шагов от (1,1) до (31,39).
    Если цели недостижима (что маловероятно для AoC), вернём -1.
    """
    favorite = _get_favorite(data)
    start = (1, 1)
    goal = (31, 39)

    queue = deque()
    queue.append((start[0], start[1], 0))  # x, y, steps
    visited = set()
    visited.add(start)

    # разумное ограничение по "полю" для безопасности (но BFS сам отрежет)
    # можно не ограничивать вообще, но сделаем ограничение по x,y
    max_coord = 100

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == goal:
            return steps

        for nx, ny in _neighbors(x, y):
            if not (0 <= nx <= max_coord and 0 <= ny <= max_coord):
                continue
            if (nx, ny) in visited:
                continue
            if not _is_open(nx, ny, favorite):
                continue
            visited.add((nx, ny))
            queue.append((nx, ny, steps + 1))

    return -1


def solve_part2(data: str) -> int:
    """
    Part 2:
    Сколько различных позиций можно посетить за не более чем 50 шагов
    (включая стартовую) из (1,1).
    """
    favorite = _get_favorite(data)
    start = (1, 1)

    max_steps = 50
    queue = deque()
    queue.append((start[0], start[1], 0))
    visited = set()
    visited.add(start)

    max_coord = 100  # с запасом

    while queue:
        x, y, steps = queue.popleft()

        if steps == max_steps:
            # дальше из этой позиции двигаться нельзя по условию
            continue

        for nx, ny in _neighbors(x, y):
            if not (0 <= nx <= max_coord and 0 <= ny <= max_coord):
                continue
            if (nx, ny) in visited:
                continue
            if not _is_open(nx, ny, favorite):
                continue
            visited.add((nx, ny))
            queue.append((nx, ny, steps + 1))

    # количество различных клеток, которые мы посетили
    return len(visited)


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

