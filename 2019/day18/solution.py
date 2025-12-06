from __future__ import annotations
from typing import List, Tuple, Dict, Deque
from collections import deque
import heapq


def solve_part1(data: str) -> str:
    grid = [list(line) for line in data.splitlines() if line.strip()]
    h = len(grid)
    w = len(grid[0])

    # Находим старт и ключи
    keys = {}
    start = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '@':
                start = (x, y)
            if 'a' <= grid[y][x] <= 'z':
                keys[grid[y][x]] = (x, y)

    all_keys = ''.join(sorted(keys))
    key_to_bit = {k: i for i, k in enumerate(all_keys)}
    target_mask = (1 << len(all_keys)) - 1

    # BFS между всеми важными точками
    points = {'@': start}
    points.update(keys)

    # precomputed graph: name -> list[(target_key, dist, required_doors_mask)]
    graph = {k: [] for k in points}

    def bfs_from(label: str):
        (sx, sy) = points[label]
        dq = deque()
        dq.append((sx, sy, 0, 0))  # x,y,dist, doors_mask
        seen = {(sx, sy)}

        while dq:
            x, y, d, doors_mask = dq.popleft()

            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                if (nx, ny) in seen:
                    continue
                c = grid[ny][nx]
                if c == '#':
                    continue
                ndm = doors_mask
                if 'A' <= c <= 'Z':
                    ndm |= 1 << key_to_bit[c.lower()]
                seen.add((nx, ny))
                if 'a' <= c <= 'z' and c != label:
                    # нашли ключ
                    graph[label].append((c, d+1, ndm))
                dq.append((nx, ny, d+1, ndm))

    for lbl in points:
        bfs_from(lbl)

    # Dijkstra: (dist, current_label, keys_mask)
    pq = [(0, '@', 0)]
    dist = {( '@', 0 ): 0}

    while pq:
        cur_d, cur_lbl, cur_mask = heapq.heappop(pq)
        if cur_mask == target_mask:
            return str(cur_d)
        if dist.get((cur_lbl, cur_mask), 10**15) < cur_d:
            continue

        for nxt_lbl, ndist, doors_mask in graph[cur_lbl]:
            # Чтобы пройти - должны иметь ключи от всех дверей
            if (doors_mask & ~cur_mask) != 0:
                continue
            nm = cur_mask | (1 << key_to_bit[nxt_lbl])
            nd = cur_d + ndist
            if dist.get((nxt_lbl, nm), 10**15) > nd:
                dist[(nxt_lbl, nm)] = nd
                heapq.heappush(pq, (nd, nxt_lbl, nm))

    return "0"


def solve_part2(data: str) -> str:
    grid = [list(line) for line in data.splitlines() if line.strip()]
    h = len(grid)
    w = len(grid[0])

    # Находим старт(ы) и ключи
    starts = []
    keys = {}

    # Модифицируем карту по правилам Part 2:
    # Заменяем '@' на:
    #   @#@
    #   ###
    #   @#@
    # С четырьмя стартами
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '@':
                sx, sy = x, y
                grid[sy][sx] = '#'
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    grid[sy+dy][sx+dx] = '#'
                starts = [
                    (sx-1, sy-1),
                    (sx+1, sy-1),
                    (sx-1, sy+1),
                    (sx+1, sy+1),
                ]
    # Собираем ключи
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if 'a' <= c <= 'z':
                keys[c] = (x,y)

    all_keys = ''.join(sorted(keys))
    key_to_bit = {k: i for i, k in enumerate(all_keys)}
    target_mask = (1 << len(all_keys)) - 1

    # Точки: 4 старта + ключи
    points = {f'@{i}': pos for i,pos in enumerate(starts)}
    points.update(keys)

    graph = {k: [] for k in points}

    # BFS для каждой точки
    def bfs_from(label: str):
        (sx, sy) = points[label]
        dq = deque()
        dq.append((sx, sy, 0, 0))
        seen = {(sx, sy)}
        while dq:
            x,y,d,doors_mask = dq.popleft()
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx,ny = x+dx,y+dy
                if not (0<=nx<w and 0<=ny<h): continue
                if (nx,ny) in seen: continue
                c = grid[ny][nx]
                if c=='#': continue
                ndm=doors_mask
                if 'A'<=c<='Z':
                    ndm |= 1<< key_to_bit[c.lower()]
                seen.add((nx,ny))
                if 'a'<=c<='z' and c!=label:
                    graph[label].append((c, d+1, ndm))
                dq.append((nx,ny,d+1,ndm))

    for lbl in points:
        bfs_from(lbl)

    # Dijkstra: state = (positions_of_4, mask)
    # positions_of_4 = tuple of 4 current labels (@0..@3 or keys)
    start_state = (('@0','@1','@2','@3'), 0)
    pq = [(0, start_state)]
    dist = {start_state: 0}

    while pq:
        cur_d, (pos_tuple, cur_mask) = heapq.heappop(pq)
        if cur_mask == target_mask:
            return str(cur_d)
        if dist.get((pos_tuple,cur_mask), 10**15) < cur_d:
            continue

        # выбираем одного из 4 роботов
        for i in range(4):
            cur_lbl = pos_tuple[i]
            for nxt_lbl, ndist, doors_mask in graph[cur_lbl]:
                if (doors_mask & ~cur_mask)!=0:
                    continue
                nm = cur_mask | (1<< key_to_bit[nxt_lbl])
                new_positions = list(pos_tuple)
                new_positions[i] = nxt_lbl
                new_positions = tuple(new_positions)
                nd = cur_d + ndist
                if dist.get((new_positions,nm),10**15) > nd:
                    dist[(new_positions,nm)] = nd
                    heapq.heappush(pq, (nd, (new_positions,nm)))

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
