# Advent of Code 2016 - Day 17
# Two Steps Forward
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> str
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — одна строка: passcode.

from pathlib import Path
import hashlib
from collections import deque


def _get_passcode(data: str) -> str:
    """
    Берём первую непустую строку как passcode.
    """
    for line in data.splitlines():
        line = line.strip()
        if line:
            return line
    raise ValueError("Passcode not found in input")


def _open_doors(passcode: str, path: str):
    """
    Определяем открытые двери для состояния (passcode + path).
    Возвращает список (dir_char, dx, dy) для открытых направлений.
    """
    s = passcode + path
    h = hashlib.md5(s.encode("utf-8")).hexdigest()
    first4 = h[:4]

    dirs = []
    # порядок: U, D, L, R
    mapping = [
        ("U", 0, -1),
        ("D", 0, 1),
        ("L", -1, 0),
        ("R", 1, 0),
    ]

    for ch_hash, (dch, dx, dy) in zip(first4, mapping):
        if ch_hash in "bcdef":
            dirs.append((dch, dx, dy))

    return dirs


def solve_part1(data: str) -> str:
    """
    Part 1:
    Находим кратчайший путь (строка UDLR) от (0,0) до (3,3).
    Если путь не найден — возвращаем пустую строку.
    """
    passcode = _get_passcode(data)

    start = (0, 0)
    goal = (3, 3)

    # BFS по состояниям (x, y, path)
    queue = deque()
    queue.append((start[0], start[1], ""))

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == goal:
            # в BFS первое достижение цели даёт кратчайший путь
            return path

        for dch, dx, dy in _open_doors(passcode, path):
            nx, ny = x + dx, y + dy
            # проверяем границы лабиринта 4x4
            if 0 <= nx <= 3 and 0 <= ny <= 3:
                queue.append((nx, ny, path + dch))

    # если почему-то не нашли
    return ""


def solve_part2(data: str) -> int:
    """
    Part 2:
    Находим длину самого длинного пути, который заканчивается в (3,3).
    """
    passcode = _get_passcode(data)

    start = (0, 0)
    goal = (3, 3)

    max_len = 0

    # Стек для DFS: (x, y, path)
    stack = [(start[0], start[1], "")]

    while stack:
        x, y, path = stack.pop()

        if (x, y) == goal:
            # достигли цели — фиксируем длину пути
            if len(path) > max_len:
                max_len = len(path)
            # дальше из цели НЕ идём (по условию пути должны заканчиваться в vault)
            continue

        for dch, dx, dy in _open_doors(passcode, path):
            nx, ny = x + dx, y + dy
            if 0 <= nx <= 3 and 0 <= ny <= 3:
                stack.append((nx, ny, path + dch))

    return max_len


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
