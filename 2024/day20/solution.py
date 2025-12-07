from collections import deque


DIRS4 = [(1,0), (-1,0), (0,1), (0,-1)]


def parse(data: str):
    grid = [list(line) for line in data.splitlines() if line.strip()]
    R, C = len(grid), len(grid[0])
    S = E = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                S = (r,c)
            elif grid[r][c] == "E":
                E = (r,c)
    return grid, R, C, S, E


def bfs_from(start, grid, R, C):
    dist = [[None]*C for _ in range(R)]
    rq, cq = start
    q = deque([(rq,cq)])
    dist[rq][cq] = 0

    while q:
        r, c = q.popleft()
        d = dist[r][c]
        for dr, dc in DIRS4:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#" and dist[nr][nc] is None:
                dist[nr][nc] = d+1
                q.append((nr,nc))
    return dist


# --------- PART 1 Jump Deltas (exactly manhattan=2) ----------
def gen_part1_jumps():
    moves = []
    for dr in range(-2,3):
        for dc in range(-2,3):
            if abs(dr) + abs(dc) == 2:
                moves.append((dr,dc))
    return moves


# --------- PART 2 Jump Deltas (2..20 manhattan) ----------
def gen_part2_jumps():
    moves = []
    for dr in range(-20,21):
        for dc in range(-20,21):
            md = abs(dr) + abs(dc)
            if 2 <= md <= 20:
                moves.append((dr,dc))
    return moves


PART1_JUMPS = gen_part1_jumps()
PART2_JUMPS = gen_part2_jumps()


def solve_generic(data: str, jumps, threshold: int) -> str:
    grid, R, C, S, E = parse(data)
    if S is None or E is None:
        return "0"

    distS = bfs_from(S, grid, R, C)
    distE = bfs_from(E, grid, R, C)

    normal = distS[E[0]][E[1]]
    if normal is None:
        return "0"

    count = 0

    for r in range(R):
        for c in range(C):
            if distS[r][c] is None:
                continue
            d1 = distS[r][c]

            for dr, dc in jumps:
                nr, nc = r+dr, c+dc
                if not (0 <= nr < R and 0 <= nc < C):
                    continue
                if distE[nr][nc] is None:
                    continue
                if grid[nr][nc] == "#":
                    continue

                jump_cost = abs(dr) + abs(dc)
                total = d1 + jump_cost + distE[nr][nc]
                saved = normal - total

                if saved >= threshold:
                    count += 1

    return str(count)


def solve_part1(data: str) -> str:
    # threshold для реального инпута = 100
    return solve_generic(data, PART1_JUMPS, 100)


def solve_part2(data: str) -> str:
    return solve_generic(data, PART2_JUMPS, 100)


if __name__ == "__main__":
    from pathlib import Path
    here = Path(__file__).resolve().parent
    raw = (here/"input.txt").read_text() if (here/"input.txt").exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
