from pathlib import Path
from typing import List, Tuple


# Сдвиги для направлений в cube-координатах
DIRS = {
    "n":  (0,  1, -1),
    "ne": (1,  0, -1),
    "se": (1, -1,  0),
    "s":  (0, -1,  1),
    "sw": (-1, 0,  1),
    "nw": (-1, 1,  0),
}


def _parse_steps(data: str) -> List[str]:
    """
    Парсим содержимое input.txt в список шагов:
    n, ne, se, s, sw, nw
    Берём все непустые токены, разделённые запятыми/пробелами.
    """
    text = data.strip()
    if not text:
        return []

    # Меняем переводы строк на запятые, чтобы не мешали split по запятой
    # (на всякий, если input разбит на несколько строк)
    text = text.replace("\n", ",").replace("\r", ",")
    raw_tokens = text.split(",")

    steps: List[str] = []
    for token in raw_tokens:
        t = token.strip()
        if not t:
            continue
        steps.append(t)
    return steps


def _cube_add(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def _cube_dist(pos: Tuple[int, int, int]) -> int:
    """
    Расстояние от (0,0,0) до pos в cube-координатах.
    """
    x, y, z = pos
    return (abs(x) + abs(y) + abs(z)) // 2


def solve_part1(data: str) -> int:
    """
    Day 11, Part 1:
    Пройти все шаги и вернуть расстояние от старта до конечной точки.
    """
    steps = _parse_steps(data)
    x = y = z = 0  # старт в (0,0,0)

    for step in steps:
        dx, dy, dz = DIRS[step]
        x += dx
        y += dy
        z += dz

    return _cube_dist((x, y, z))


def solve_part2(data: str) -> int:
    """
    Day 11, Part 2:
    Пройти все шаги и вернуть максимальное расстояние от старта,
    которое встречалось в процессе.
    """
    steps = _parse_steps(data)
    x = y = z = 0
    max_dist = 0

    for step in steps:
        dx, dy, dz = DIRS[step]
        x += dx
        y += dy
        z += dz
        d = _cube_dist((x, y, z))
        if d > max_dist:
            max_dist = d

    return max_dist


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
