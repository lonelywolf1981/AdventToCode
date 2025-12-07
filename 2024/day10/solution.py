def parse(data: str):
    grid = [list(map(int, line.strip())) for line in data.splitlines() if line.strip()]
    return grid


# Четыре направления
DIRS = [(1,0), (-1,0), (0,1), (0,-1)]


def solve_part1(data: str) -> str:
    grid = parse(data)
    R, C = len(grid), len(grid[0])

    # memo_endpoints[(r,c)] = множество финишных (r9,c9) достижимых отсюда
    memo_endpoints = {}

    def dfs(r, c):
        # если уже есть в мемо — возвращаем
        if (r, c) in memo_endpoints:
            return memo_endpoints[(r, c)]

        h = grid[r][c]
        if h == 9:
            # достигли вершины, единственный финиш — текущая точка
            memo_endpoints[(r, c)] = {(r, c)}
            return memo_endpoints[(r, c)]

        res = set()
        nh = h + 1
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == nh:
                res |= dfs(nr, nc)

        memo_endpoints[(r, c)] = res
        return res

    total = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 0:
                total += len(dfs(r, c))

    return str(total)


def solve_part2(data: str) -> str:
    grid = parse(data)
    R, C = len(grid), len(grid[0])

    # memo_paths[(r,c)] = количество всех возможных путей 0→...→9 из этой точки
    memo_paths = {}

    def dfs_paths(r, c):
        if (r, c) in memo_paths:
            return memo_paths[(r, c)]

        h = grid[r][c]
        if h == 9:
            memo_paths[(r, c)] = 1
            return 1

        total_paths = 0
        nh = h + 1

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == nh:
                total_paths += dfs_paths(nr, nc)

        memo_paths[(r, c)] = total_paths
        return total_paths

    total = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 0:
                total += dfs_paths(r, c)

    return str(total)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
