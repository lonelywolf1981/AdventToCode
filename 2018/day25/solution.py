from __future__ import annotations

from pathlib import Path
from typing import List, Tuple


Point4D = Tuple[int, int, int, int]


def parse_input(data: str) -> List[Point4D]:
    """
    Каждая строка: x,y,z,t
    """
    points: List[Point4D] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != 4:
            continue
        x, y, z, t = map(int, parts)
        points.append((x, y, z, t))
    return points


def manhattan4(a: Point4D, b: Point4D) -> int:
    return (
        abs(a[0] - b[0]) +
        abs(a[1] - b[1]) +
        abs(a[2] - b[2]) +
        abs(a[3] - b[3])
    )


# ---- Union-Find (DSU) -------------------------------------------------


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


def count_constellations(points: List[Point4D]) -> int:
    """
    Строим DSU: соединяем пары точек с dist <= 3, считаем количество компонент.
    """
    n = len(points)
    if n == 0:
        return 0

    dsu = DSU(n)

    for i in range(n):
        for j in range(i + 1, n):
            if manhattan4(points[i], points[j]) <= 3:
                dsu.union(i, j)

    roots = {dsu.find(i) for i in range(n)}
    return len(roots)


def solve_part1(data: str) -> str:
    points = parse_input(data)
    constellations = count_constellations(points)
    return str(constellations)


def solve_part2(data: str) -> str:
    """
    В официальном AoC 2018 Day 25 Part 2 нет — это финальная задача.
    Чтобы start.py был доволен, вернём тот же ответ, что и в Part 1.
    """
    return solve_part1(data)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
