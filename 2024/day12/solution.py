from collections import deque
from typing import List, Tuple, Set


def parse_grid(data: str) -> List[str]:
    return [line.strip() for line in data.splitlines() if line.strip()]


DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def bfs_region(grid: List[str], sr: int, sc: int, visited: List[List[bool]]) -> Tuple[str, List[Tuple[int, int]], Tuple[int, int, int, int]]:
    """
    Обходит один регион (BFS) и возвращает:
    - символ растения,
    - список клеток региона,
    - bounding box (min_r, max_r, min_c, max_c).
    """
    R, C = len(grid), len(grid[0])
    plant = grid[sr][sc]
    q = deque([(sr, sc)])
    visited[sr][sc] = True
    cells: List[Tuple[int, int]] = []

    min_r = max_r = sr
    min_c = max_c = sc

    while q:
        r, c = q.popleft()
        cells.append((r, c))
        if r < min_r: min_r = r
        if r > max_r: max_r = r
        if c < min_c: min_c = c
        if c > max_c: max_c = c

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and not visited[nr][nc] and grid[nr][nc] == plant:
                visited[nr][nc] = True
                q.append((nr, nc))

    return plant, cells, (min_r, max_r, min_c, max_c)


def region_perimeter(grid: List[str], cells: List[Tuple[int, int]]) -> int:
    """
    Периметр региона: для каждой клетки считаем,
    сколько её сторон граничат с «чужим» или вне карты.
    """
    R, C = len(grid), len(grid[0])
    plant = grid[cells[0][0]][cells[0][1]]
    cell_set: Set[Tuple[int, int]] = set(cells)

    per = 0
    for r, c in cells:
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < R and 0 <= nc < C) or grid[nr][nc] != plant:
                per += 1
    return per


def region_sides(grid: List[str], cells: List[Tuple[int, int]], bbox: Tuple[int, int, int, int]) -> int:
    """
    Считает количество прямых сторон по границе региона.
    Идея:
      - соберём множества граничных рёбер (top, bottom, left, right),
      - затем в bounding box пробежимся по строкам/столбцам и посчитаем
        количество непрерывных серий рёбер каждого типа.
    """
    R, C = len(grid), len(grid[0])
    plant = grid[cells[0][0]][cells[0][1]]
    cell_set: Set[Tuple[int, int]] = set(cells)

    min_r, max_r, min_c, max_c = bbox

    top_edges: Set[Tuple[int, int]] = set()
    bottom_edges: Set[Tuple[int, int]] = set()
    left_edges: Set[Tuple[int, int]] = set()
    right_edges: Set[Tuple[int, int]] = set()

    # Определяем, где есть граничные рёбра
    for r, c in cells:
        # вверх
        nr, nc = r - 1, c
        if not (0 <= nr < R and 0 <= nc < C) or grid[nr][nc] != plant:
            top_edges.add((r, c))
        # вниз
        nr, nc = r + 1, c
        if not (0 <= nr < R and 0 <= nc < C) or grid[nr][nc] != plant:
            bottom_edges.add((r, c))
        # влево
        nr, nc = r, c - 1
        if not (0 <= nr < R and 0 <= nc < C) or grid[nr][nc] != plant:
            left_edges.add((r, c))
        # вправо
        nr, nc = r, c + 1
        if not (0 <= nr < R and 0 <= nc < C) or grid[nr][nc] != plant:
            right_edges.add((r, c))

    sides = 0

    # Горизонтальные стороны: top и bottom
    for r in range(min_r, max_r + 1):
        # top
        prev = False
        for c in range(min_c, max_c + 1):
            has_edge = (r, c) in top_edges
            if has_edge and not prev:
                sides += 1
            prev = has_edge

        # bottom
        prev = False
        for c in range(min_c, max_c + 1):
            has_edge = (r, c) in bottom_edges
            if has_edge and not prev:
                sides += 1
            prev = has_edge

    # Вертикальные стороны: left и right
    for c in range(min_c, max_c + 1):
        # left
        prev = False
        for r in range(min_r, max_r + 1):
            has_edge = (r, c) in left_edges
            if has_edge and not prev:
                sides += 1
            prev = has_edge

        # right
        prev = False
        for r in range(min_r, max_r + 1):
            has_edge = (r, c) in right_edges
            if has_edge and not prev:
                sides += 1
            prev = has_edge

    return sides


def solve_part1(data: str) -> str:
    # Day 12 Part 1: цена = площадь * периметр.
    grid = parse_grid(data)
    if not grid:
        return "0"

    R, C = len(grid), len(grid[0])
    visited = [[False] * C for _ in range(R)]

    total_price = 0

    for r in range(R):
        for c in range(C):
            if not visited[r][c]:
                plant, cells, bbox = bfs_region(grid, r, c, visited)
                area = len(cells)
                per = region_perimeter(grid, cells)
                total_price += area * per

    return str(total_price)


def solve_part2(data: str) -> str:
    # Day 12 Part 2: цена = площадь * количество сторон (прямых сегментов).
    grid = parse_grid(data)
    if not grid:
        return "0"

    R, C = len(grid), len(grid[0])
    visited = [[False] * C for _ in range(R)]

    total_price = 0

    for r in range(R):
        for c in range(C):
            if not visited[r][c]:
                plant, cells, bbox = bfs_region(grid, r, c, visited)
                area = len(cells)
                sides = region_sides(grid, cells, bbox)
                total_price += area * sides

    return str(total_price)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
