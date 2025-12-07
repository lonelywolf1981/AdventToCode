from pathlib import Path
from collections import deque

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]
DIR_CH = {(1,0):"v", (-1,0):"^", (0,1):">", (0,-1):"<"}


def parse(data: str):
    grid = [list(line) for line in data.splitlines() if line.strip()]
    R = len(grid)
    C = len(grid[0])
    return grid, R, C


# ---------------------------------------------------------
# PART 1 — учитываем склоны
# ---------------------------------------------------------
def solve_part1(data: str) -> str:
    grid, R, C = parse(data)

    # старт = первая '.' в первой строке
    start = (0, grid[0].index('.'))
    # финиш = первая '.' в последней строке
    goal = (R - 1, grid[-1].index('.'))

    best = 0
    stack = [(start[0], start[1], 0, set([start]))]

    while stack:
        r, c, dist, used = stack.pop()

        if (r, c) == goal:
            if dist > best:
                best = dist
            continue

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc

            if not (0 <= nr < R and 0 <= nc < C):
                continue
            ch = grid[nr][nc]
            if ch == "#":
                continue

            # проверка уклона
            if ch in DIR_CH.values():
                # slope points away: must match movement direction
                if DIR_CH[(dr, dc)] != ch:
                    continue

            if (nr, nc) in used:
                continue

            stack.append((nr, nc, dist + 1, used | {(nr, nc)}))

    return str(best)


# ---------------------------------------------------------
# PART 2 — игнорируем склоны, строим граф перекрёстков
# ---------------------------------------------------------

def neighbors_no_slopes(grid, R, C, r, c):
    out = []
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#":
            out.append((nr, nc))
    return out


def compress_graph(grid, R, C, start, goal):
    """
    Строим граф:
    - junctions = перекрёстки (≥3 соседей), плюс start/goal.
    - между ними прокладываем целые коридоры (без разветвлений).
    """
    # 1. Найдём все важные узлы
    junctions = set([start, goal])
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "#":
                continue
            nbrs = neighbors_no_slopes(grid, R, C, r, c)
            if len(nbrs) >= 3:
                junctions.add((r, c))

    # 2. Для каждого узла строим связи
    graph = {j: {} for j in junctions}

    for jr, jc in junctions:
        for (dr, dc) in DIRS:
            # идём по коридору в направлении (dr,dc)
            r, c = jr + dr, jc + dc
            if not (0 <= r < R and 0 <= c < C) or grid[r][c] == "#":
                continue

            dist = 1
            pr, pc = jr, jc
            cr, cc = r, c

            # идём пока не встретим другой узел
            while True:
                if (cr, cc) in junctions:
                    graph[(jr, jc)][(cr, cc)] = dist
                    break

                # проверяем, что это коридор (ровно 2 соседа)
                nbrs = neighbors_no_slopes(grid, R, C, cr, cc)
                if len(nbrs) != 2:
                    # значит, это тоже junction (случайно пропущенный)
                    junctions.add((cr, cc))
                    graph.setdefault((cr, cc), {})
                    graph[(jr, jc)][(cr, cc)] = dist
                    break

                # продолжаем по коридору: в соседе, который не parent
                for nr, nc in nbrs:
                    if (nr, nc) != (pr, pc):
                        pr, pc = cr, cc
                        cr, cc = nr, nc
                        dist += 1
                        break

    return graph


def dfs_longest(graph, start, goal):
    best = 0
    stack = [(start, 0, set([start]))]

    while stack:
        node, dist, used = stack.pop()
        if node == goal:
            best = max(best, dist)
            continue

        for nxt, w in graph[node].items():
            if nxt not in used:
                stack.append((nxt, dist + w, used | {nxt}))

    return best


def solve_part2(data: str) -> str:
    grid, R, C = parse(data)

    start = (0, grid[0].index('.'))
    goal = (R - 1, grid[-1].index('.'))

    graph = compress_graph(grid, R, C, start, goal)
    best = dfs_longest(graph, start, goal)
    return str(best)


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
