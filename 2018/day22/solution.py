from __future__ import annotations

from pathlib import Path
import heapq


# --------------------------------------------------------------------
#   PARSING
# --------------------------------------------------------------------

def parse(data: str):
    depth = 0
    tx = ty = 0
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("depth"):
            depth = int(line.split(":")[1].strip())
        elif line.startswith("target"):
            t = line.split(":")[1].strip()
            tx, ty = map(int, t.split(","))
    return depth, tx, ty


# --------------------------------------------------------------------
#   GEOLOGICAL INDEX / EROSION / REGION TYPE
# --------------------------------------------------------------------

def compute_maps(depth: int, tx: int, ty: int):
    """
    Создаём таблицы geologic index, erosion level, region type.
    Для Part 2 нужно расширение поля (обычно хватает x: tx+100, y: ty+100).
    """
    W = tx + 100
    H = ty + 100

    geo = [[0] * (W + 1) for _ in range(H + 1)]
    erosion = [[0] * (W + 1) for _ in range(H + 1)]
    region = [[0] * (W + 1) for _ in range(H + 1)]

    for y in range(H + 1):
        for x in range(W + 1):
            if (x, y) == (0, 0):
                gi = 0
            elif (x, y) == (tx, ty):
                gi = 0
            elif y == 0:
                gi = x * 16807
            elif x == 0:
                gi = y * 48271
            else:
                gi = erosion[y][x - 1] * erosion[y - 1][x]

            geo[y][x] = gi
            el = (gi + depth) % 20183
            erosion[y][x] = el
            region[y][x] = el % 3

    return region


# region types:
# 0 = rocky  → allowed: torch, climb
# 1 = wet    → allowed: climb, none
# 2 = narrow → allowed: torch, none

TOOLS = {
    0: ("torch", "climb"),
    1: ("climb", "none"),
    2: ("torch", "none"),
}


# --------------------------------------------------------------------
#  PART 1
# --------------------------------------------------------------------

def solve_part1(data: str) -> str:
    depth, tx, ty = parse(data)
    region = compute_maps(depth, tx, ty)

    s = 0
    for y in range(ty + 1):
        for x in range(tx + 1):
            s += region[y][x]
    return str(s)


# --------------------------------------------------------------------
#  PART 2 = DIJKSTRA (x, y, tool)
# --------------------------------------------------------------------

def solve_part2(data: str) -> str:
    depth, tx, ty = parse(data)
    region = compute_maps(depth, tx, ty)

    # Dijkstra priority queue
    pq = []
    heapq.heappush(pq, (0, 0, 0, "torch"))  # cost, x, y, tool

    visited = {}  # (x, y, tool) -> best_cost

    while pq:
        cost, x, y, tool = heapq.heappop(pq)

        if (x, y, tool) in visited and visited[(x, y, tool)] <= cost:
            continue
        visited[(x, y, tool)] = cost

        # цель: достичь (tx, ty) с инструментом torch
        if (x, y) == (tx, ty) and tool == "torch":
            return str(cost)

        # смена инструмента
        for new_tool in TOOLS[region[y][x]]:
            if new_tool != tool:
                ncost = cost + 7
                if visited.get((x, y, new_tool), 10**15) > ncost:
                    heapq.heappush(pq, (ncost, x, y, new_tool))

        # движение
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0 or ny >= len(region) or nx >= len(region[0]):
                continue
            # можно идти, если tool разрешён в соседней клетке
            if tool in TOOLS[region[ny][nx]]:
                ncost = cost + 1
                if visited.get((nx, ny, tool), 10**15) > ncost:
                    heapq.heappush(pq, (ncost, nx, ny, tool))

    return "ERROR"  # не должно произойти


# --------------------------------------------------------------------
#   MAIN
# --------------------------------------------------------------------

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
