import heapq


DIRS = [(0,1), (1,0), (0,-1), (-1,0)]   # R, D, L, U


def parse(data: str):
    grid = [list(line) for line in data.splitlines() if line.strip()]
    R, C = len(grid), len(grid[0])
    start = end = None

    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)

    return grid, start, end, R, C


def solve_part1(data: str) -> str:
    grid, start, end, R, C = parse(data)

    # dist[r][c][dir]
    INF = 10**30
    dist = [[[INF]*4 for _ in range(C)] for __ in range(R)]

    sr, sc = start
    er, ec = end

    # стартуем, направлены вправо (0) — это условие задачи
    pq = []
    dist[sr][sc][0] = 0
    heapq.heappush(pq, (0, sr, sc, 0))

    while pq:
        cost, r, c, d = heapq.heappop(pq)
        if cost != dist[r][c][d]:
            continue

        # поворот вправо
        nd = (d + 1) % 4
        ncost = cost + 1000
        if ncost < dist[r][c][nd]:
            dist[r][c][nd] = ncost
            heapq.heappush(pq, (ncost, r, c, nd))

        # поворот влево
        nd = (d - 1) % 4
        ncost = cost + 1000
        if ncost < dist[r][c][nd]:
            dist[r][c][nd] = ncost
            heapq.heappush(pq, (ncost, r, c, nd))

        # шаг вперёд
        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#":
            ncost = cost + 1
            if ncost < dist[nr][nc][d]:
                dist[nr][nc][d] = ncost
                heapq.heappush(pq, (ncost, nr, nc, d))

    # Минимум among all directions
    ans = min(dist[er][ec])
    return str(ans)


def solve_part2(data: str) -> str:
    grid, start, end, R, C = parse(data)

    INF = 10**30
    dist = [[[INF]*4 for _ in range(C)] for __ in range(R)]
    sr, sc = start
    er, ec = end

    # ---------- Dijkstra ----------
    pq = []
    dist[sr][sc][0] = 0
    heapq.heappush(pq, (0, sr, sc, 0))

    while pq:
        cost, r, c, d = heapq.heappop(pq)
        if cost != dist[r][c][d]:
            continue

        # turn right
        nd = (d + 1) % 4
        ncost = cost + 1000
        if ncost < dist[r][c][nd]:
            dist[r][c][nd] = ncost
            heapq.heappush(pq, (ncost, r, c, nd))

        # turn left
        nd = (d - 1) % 4
        ncost = cost + 1000
        if ncost < dist[r][c][nd]:
            dist[r][c][nd] = ncost
            heapq.heappush(pq, (ncost, r, c, nd))

        # forward
        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#":
            ncost = cost + 1
            if ncost < dist[nr][nc][d]:
                dist[nr][nc][d] = ncost
                heapq.heappush(pq, (ncost, nr, nc, d))

    best = min(dist[er][ec])

    # ---------- строим обратные рёбра минимальных путей ----------
    from collections import deque

    good = set()  # множество (r,c,dir)
    q = deque()

    # начинаем из всех направлений в E, где dist = best
    for d in range(4):
        if dist[er][ec][d] == best:
            good.add((er, ec, d))
            q.append((er, ec, d))

    while q:
        r, c, d = q.popleft()
        cost = dist[r][c][d]

        # 1. Пришли сюда поворотом справа?
        pd = (d - 1) % 4
        if dist[r][c][pd] == cost - 1000:
            if (r,c,pd) not in good:
                good.add((r,c,pd))
                q.append((r,c,pd))

        # 2. Пришли сюда поворотом слева?
        pd = (d + 1) % 4
        if dist[r][c][pd] == cost - 1000:
            if (r,c,pd) not in good:
                good.add((r,c,pd))
                q.append((r,c,pd))

        # 3. Пришли шагом вперёд?
        dr, dc = DIRS[d]
        pr, pc = r - dr, c - dc
        if 0 <= pr < R and 0 <= pc < C and grid[pr][pc] != "#":
            if dist[pr][pc][d] == cost - 1:
                if (pr,pc,d) not in good:
                    good.add((pr,pc,d))
                    q.append((pr,pc,d))

    # ---------- считаем клетки ----------
    cells = {(r,c) for (r,c,d) in good}
    return str(len(cells))


# ========== RUNNER ==========
if __name__ == "__main__":
    from pathlib import Path
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
