from typing import List


def parse_grid(data: str) -> List[List[bool]]:
    grid = []
    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        row = [c == "#" for c in line]
        grid.append(row)
    return grid


def count_on_neighbors(grid: List[List[bool]], x: int, y: int) -> int:
    h = len(grid)
    w = len(grid[0])
    cnt = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if 0 <= nx < h and 0 <= ny < w:
                if grid[nx][ny]:
                    cnt += 1
    return cnt


def step(grid: List[List[bool]], stuck_corners: bool = False) -> List[List[bool]]:
    h = len(grid)
    w = len(grid[0])
    new_grid = [[False] * w for _ in range(h)]

    for i in range(h):
        for j in range(w):
            neighbors = count_on_neighbors(grid, i, j)
            if grid[i][j]:
                new_grid[i][j] = neighbors in (2, 3)
            else:
                new_grid[i][j] = neighbors == 3

    if stuck_corners:
        # углы всегда включены
        new_grid[0][0] = True
        new_grid[0][w - 1] = True
        new_grid[h - 1][0] = True
        new_grid[h - 1][w - 1] = True

    return new_grid


def solve_part1(data: str) -> str:
    grid = parse_grid(data)
    steps = 100
    for _ in range(steps):
        grid = step(grid, stuck_corners=False)
    # считаем включённые
    total_on = sum(cell for row in grid for cell in row)
    return str(total_on)


def solve_part2(data: str) -> str:
    grid = parse_grid(data)
    h = len(grid)
    w = len(grid[0])

    # изначально фиксируем углы включёнными
    grid[0][0] = True
    grid[0][w - 1] = True
    grid[h - 1][0] = True
    grid[h - 1][w - 1] = True

    steps = 100
    for _ in range(steps):
        grid = step(grid, stuck_corners=True)

    total_on = sum(cell for row in grid for cell in row)
    return str(total_on)


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
