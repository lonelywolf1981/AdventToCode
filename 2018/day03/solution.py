import re
from pathlib import Path
from typing import List, Tuple


Claim = Tuple[int, int, int, int, int]  # (id, x, y, w, h)


def parse_input(data: str) -> List[Claim]:
    """
    Разбирает строки вида:
    #1 @ 1,3: 4x4

    Возвращает список кортежей (id, x, y, w, h).
    """
    claims: List[Claim] = []
    pattern = re.compile(
        r"#(?P<id>\d+)\s*@\s*"
        r"(?P<x>\d+),(?P<y>\d+):\s*"
        r"(?P<w>\d+)x(?P<h>\d+)"
    )

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if not m:
            continue
        cid = int(m.group("id"))
        x = int(m.group("x"))
        y = int(m.group("y"))
        w = int(m.group("w"))
        h = int(m.group("h"))
        claims.append((cid, x, y, w, h))

    return claims


def build_fabric(claims: List[Claim]):
    """
    Строит двумерный массив fabric[y][x] — сколько заявок покрывают клетку.
    Размер подбираем по максимальным x и y.
    """
    if not claims:
        return []

    max_x = 0
    max_y = 0
    for _, x, y, w, h in claims:
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)

    # fabric[y][x]
    fabric = [[0] * max_x for _ in range(max_y)]

    for _, x, y, w, h in claims:
        for yy in range(y, y + h):
            row = fabric[yy]
            for xx in range(x, x + w):
                row[xx] += 1

    return fabric


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    claims = parse_input(data)
    fabric = build_fabric(claims)

    # считаем клетки, где наложения >= 2
    overlap = 0
    for row in fabric:
        for cell in row:
            if cell >= 2:
                overlap += 1

    return str(overlap)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    claims = parse_input(data)
    fabric = build_fabric(claims)

    # ищем заявку, у которой все клетки покрыты ровно 1 раз
    for cid, x, y, w, h in claims:
        intact = True
        for yy in range(y, y + h):
            row = fabric[yy]
            for xx in range(x, x + w):
                if row[xx] != 1:
                    intact = False
                    break
            if not intact:
                break

        if intact:
            return str(cid)

    # по условию AoC такая заявка всегда есть
    return ""


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
