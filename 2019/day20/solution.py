from __future__ import annotations
from collections import deque, defaultdict
from typing import Tuple, List, Dict


def parse_map(data: str) -> Tuple[List[str], Dict[str, List[Tuple[int,int]]]]:
    grid = data.splitlines()
    h = len(grid)
    w = max(len(row) for row in grid)

    # Выравниваем строки
    grid = [row.ljust(w) for row in grid]

    portals: Dict[str, List[Tuple[int,int]]] = defaultdict(list)

    def is_letter(c: str) -> bool:
        return 'A' <= c <= 'Z'

    # ищем пары букв с проходом рядом
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if not is_letter(c):
                continue

            # горизонтальные: [A][B][.]
            if x+1 < w and is_letter(grid[y][x+1]):
                name = c + grid[y][x+1]
                # слева проход?
                if x-1 >= 0 and grid[y][x-1] == '.':
                    portals[name].append((x-1, y))
                # справа проход?
                if x+2 < w and grid[y][x+2] == '.':
                    portals[name].append((x+2, y))

            # вертикальные: [A] / [B] / [.]
            if y+1 < h and is_letter(grid[y+1][x]):
                name = c + grid[y+1][x]
                # сверху проход?
                if y-1 >= 0 and grid[y-1][x] == '.':
                    portals[name].append((x, y-1))
                # снизу проход?
                if y+2 < h and grid[y+2][x] == '.':
                    portals[name].append((x, y+2))

    return grid, portals


def solve_part1(data: str) -> str:
    grid, portals = parse_map(data)
    h = len(grid)
    w = len(grid[0])

    start = portals["AA"][0]
    end = portals["ZZ"][0]

    # Создаём карту переходов портал -> портал
    portal_edges = {}
    for name, pts in portals.items():
        if len(pts) == 2:
            portal_edges[pts[0]] = pts[1]
            portal_edges[pts[1]] = pts[0]

    # BFS по 2D-лабиринту
    dq = deque()
    dq.append((*start, 0))  # x, y, dist
    seen = {start}

    while dq:
        x, y, d = dq.popleft()
        if (x, y) == end:
            return str(d)

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == '.' and (nx,ny) not in seen:
                seen.add((nx,ny))
                dq.append((nx,ny,d+1))

        # переход через портал
        if (x,y) in portal_edges:
            nx, ny = portal_edges[(x,y)]
            if (nx,ny) not in seen:
                seen.add((nx,ny))
                dq.append((nx,ny,d+1))

    return "0"


def solve_part2(data: str) -> str:
    grid, portals = parse_map(data)
    h = len(grid)
    w = len(grid[0])

    start = portals["AA"][0]
    end = portals["ZZ"][0]

    # Определяем, внутренний или внешний портал
    portal_edges = {}
    portal_type = {}  # pos -> +1 (inner) или -1 (outer)

    for name, pts in portals.items():
        if len(pts) == 2:
            (x1, y1), (x2, y2) = pts

            # Определяем inner/outer по расположению
            def is_outer(x, y):
                return x < 3 or y < 3 or x > w-4 or y > h-4

            if is_outer(x1,y1):
                portal_type[(x1,y1)] = -1
                portal_type[(x2,y2)] = +1
            else:
                portal_type[(x1,y1)] = +1
                portal_type[(x2,y2)] = -1

            portal_edges[(x1,y1)] = (x2,y2)
            portal_edges[(x2,y2)] = (x1,y1)

    # BFS: состояние (x, y, level)
    dq = deque()
    dq.append((*start, 0, 0))  # x,y,level,dist
    seen = {(*start, 0)}

    while dq:
        x, y, lvl, d = dq.popleft()

        # достижение ZZ возможно ТОЛЬКО на уровне 0
        if lvl == 0 and (x, y) == end:
            return str(d)

        # обычные шаги
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == '.':
                state = (nx, ny, lvl)
                if state not in seen:
                    seen.add(state)
                    dq.append((nx, ny, lvl, d+1))

        # переход через портал
        if (x,y) in portal_edges:
            ndir = portal_type[(x,y)]
            nlvl = lvl + ndir
            if nlvl >= 0:  # нельзя ниже нуля
                nx, ny = portal_edges[(x,y)]
                state = (nx, ny, nlvl)
                if state not in seen:
                    seen.add(state)
                    dq.append((nx, ny, nlvl, d+1))

    return "0"


# ================== TEMPLATE ==================

if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
