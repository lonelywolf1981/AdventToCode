from typing import List, Tuple
from collections import deque


DIRS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


# ========================= PARSE =========================

def parse(data: str):
    grid_part, moves_part = data.strip("\n").split("\n\n")
    grid = [list(row) for row in grid_part.splitlines()]
    moves = "".join(moves_part.splitlines())
    return grid, moves


# ========================= PART 1 ========================

def can_push_chain(grid: List[List[str]], r: int, c: int, dr: int, dc: int) -> bool:
    R, C = len(grid), len(grid[0])

    while True:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < R and 0 <= nc < C):
            return False
        if grid[nr][nc] == "#":
            return False
        if grid[nr][nc] == ".":
            return True
        # ещё один ящик
        r, c = nr, nc


def push_chain(grid: List[List[str]], r: int, c: int, dr: int, dc: int):
    R, C = len(grid), len(grid[0])
    chain = []

    cr, cc = r, c
    while True:
        chain.append((cr, cc))
        nr, nc = cr + dr, cc + dc
        if not (0 <= nr < R and 0 <= nc < C) or grid[nr][nc] != "O":
            break
        cr, cc = nr, nc

    # двигаем с конца
    for cr, cc in reversed(chain):
        nr, nc = cr + dr, cc + dc
        grid[nr][nc] = "O"
        grid[cr][cc] = "."


def solve_part1(data: str) -> str:
    grid, moves = parse(data)
    R, C = len(grid), len(grid[0])

    # ищем робота
    rr = cc = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "@":
                rr, cc = r, c
                break
        if rr is not None:
            break

    for m in moves:
        dr, dc = DIRS[m]
        nr, nc = rr + dr, cc + dc
        cell = grid[nr][nc]

        if cell == "#":
            continue

        if cell == ".":
            grid[rr][cc] = "."
            grid[nr][nc] = "@"
            rr, cc = nr, nc
            continue

        if cell == "O":
            if can_push_chain(grid, nr, nc, dr, dc):
                push_chain(grid, nr, nc, dr, dc)
                grid[rr][cc] = "."
                grid[nr][nc] = "@"
                rr, cc = nr, nc

    ans = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "O":
                ans += r * 100 + c
    return str(ans)


# ========================= PART 2 ========================

def expand_grid_for_part2(grid: List[List[str]]) -> List[List[str]]:
    """
    Расширяем карту:
      . -> ..
      # -> ##
      @ -> @.
      O -> []
    """
    new_grid = []
    for row in grid:
        new_row = []
        for ch in row:
            if ch == ".":
                new_row += [".", "."]
            elif ch == "#":
                new_row += ["#", "#"]
            elif ch == "@":
                new_row += ["@", "."]
            elif ch == "O":
                new_row += ["[", "]"]
        new_grid.append(new_row)
    return new_grid


def find_robot(grid: List[List[str]]) -> Tuple[int, int]:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "@":
                return r, c
    raise RuntimeError("Robot '@' not found")


def solve_part2(data: str) -> str:
    grid0, moves = parse(data)
    grid = expand_grid_for_part2(grid0)

    R, C = len(grid), len(grid[0])
    rr, cc = find_robot(grid)

    def box_left(r: int, c: int) -> Tuple[int, int]:
        """Вернуть координату левой скобки ящика по любой его клетке ('[' или ']')."""
        ch = grid[r][c]
        if ch == "[":
            return r, c
        elif ch == "]":
            return r, c - 1
        else:
            raise RuntimeError("box_left called on non-box cell")

    for m in moves:
        dr, dc = DIRS[m]
        nr, nc = rr + dr, cc + dc
        cell = grid[nr][nc]

        if cell == "#":
            continue

        if cell == ".":
            # просто шаг
            grid[rr][cc] = "."
            grid[nr][nc] = "@"
            rr, cc = nr, nc
            continue

        if cell in "[]":
            # BFS по ящикам (по левой скобке каждого ящика)
            start_left = box_left(nr, nc)
            seen_left = {start_left}
            q = deque([start_left])
            can_move = True

            while q and can_move:
                br, bc = q.popleft()
                # две клетки этого ящика
                for cr, cc2 in ((br, bc), (br, bc + 1)):
                    tr, tc = cr + dr, cc2 + dc

                    if not (0 <= tr < R and 0 <= tc < C):
                        can_move = False
                        break
                    if grid[tr][tc] == "#":
                        can_move = False
                        break

                    if grid[tr][tc] in "[]":
                        nl = box_left(tr, tc)
                        if nl not in seen_left:
                            seen_left.add(nl)
                            q.append(nl)

            if not can_move:
                continue

            # собираем все клетки '[' и ']' для всех ящиков, которые нужно двигать
            cells = set()
            for br, bc in seen_left:
                cells.add((br, bc))
                cells.add((br, bc + 1))

            # порядок движения, чтобы не перетирать источники
            if dr == -1:      # вверх
                ordered = sorted(cells, key=lambda p: p[0])         # сверху вниз
            elif dr == 1:     # вниз
                ordered = sorted(cells, key=lambda p: -p[0])        # снизу вверх
            elif dc == -1:    # влево
                ordered = sorted(cells, key=lambda p: p[1])         # слева направо
            elif dc == 1:     # вправо
                ordered = sorted(cells, key=lambda p: -p[1])        # справа налево
            else:
                ordered = list(cells)

            # двигаем все ячейки ящиков
            for r, c in ordered:
                tr, tc = r + dr, c + dc
                ch = grid[r][c]
                grid[r][c] = "."
                grid[tr][tc] = ch

            # двигаем робота
            grid[rr][cc] = "."
            rr, cc = rr + dr, cc + dc
            grid[rr][cc] = "@"

    # считаем GPS по левым '['
    ans = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "[":
                ans += r * 100 + c
    return str(ans)


# ========================= RUNNER ========================

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
