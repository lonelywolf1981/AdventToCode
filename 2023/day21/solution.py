from pathlib import Path
from collections import deque


DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def parse(data: str):
    grid = [list(line) for line in data.splitlines() if line.strip()]
    R = len(grid)
    C = len(grid[0])

    start = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                start = (r, c)
    return grid, R, C, start


# ----------------- Part 1: конечное поле -----------------


def reachable_exact_steps(grid, R, C, sr, sc, steps: int) -> int:
    """
    Возвращает количество позиций, достижимых ровно за `steps` шагов
    на конечной карте (границы = стены).
    """
    current = {(sr, sc)}
    for _ in range(steps):
        nxt = set()
        for r, c in current:
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#":
                    nxt.add((nr, nc))
        current = nxt
    return len(current)


def solve_part1(data: str) -> str:
    grid, R, C, (sr, sc) = parse(data)
    # В реальном AoC 2023 Day 21 для части 1 нужно ровно 64 шага.
    steps = 64
    return str(reachable_exact_steps(grid, R, C, sr, sc, steps))


# ----------------- Part 2: бесконечное поле -----------------


def bfs_dist_infinite(grid, R, C, sr, sc, max_steps: int) -> dict[tuple[int, int], int]:
    """
    BFS на бесконечной тайловой карте.
    возвращает dist[(r, c)] = минимальное количество шагов до клетки (r, c),
    но только для dist <= max_steps.
    Координаты (r, c) в бесконечной решётке Z^2.
    """
    dist = {(sr, sc): 0}
    q = deque()
    q.append((sr, sc))

    while q:
        r, c = q.popleft()
        d = dist[(r, c)]
        if d == max_steps:
            continue

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            # проверяем тайл по модулю
            rr = nr % R
            cc = nc % C
            if grid[rr][cc] == "#":
                continue
            if (nr, nc) not in dist:
                dist[(nr, nc)] = d + 1
                q.append((nr, nc))

    return dist


def count_reachable_with_parity(dist_map: dict[tuple[int, int], int], steps: int) -> int:
    """
    Считает количество клеток, достижимых ровно за `steps` шагов
    на бесконечной карте, по уже посчитанным dist (минимальным расстояниям).
    Если до клетки расстояние d, то она достижима на шаге steps,
    если steps >= d и (steps - d) чётное.
    """
    cnt = 0
    for d in dist_map.values():
        if d <= steps and (steps - d) % 2 == 0:
            cnt += 1
    return cnt


def solve_part2(data: str) -> str:
    grid, R, C, (sr, sc) = parse(data)

    # В реальной задаче размер квадрата R == C, S по центру
    assert R == C

    STEPS = 26_501_365  # из условия

    # offset = расстояние от старта до границы (S в центре => sr == R//2)
    offset = sr  # равно R//2 для реального инпута

    # Проверяем, что формула деления корректна
    if (STEPS - offset) % R != 0:
        # На реальном инпуте этого не будет, но чтобы не делить криво:
        raise ValueError("STEPS - offset не кратно размеру карты, проверь входные данные.")

    k = (STEPS - offset) // R

    # Нам нужны три точки: t0, t1, t2
    t0 = offset + 0 * R
    t1 = offset + 1 * R
    t2 = offset + 2 * R

    max_t = t2

    # BFS по бесконечной карте до max_t
    dist_map = bfs_dist_infinite(grid, R, C, sr, sc, max_t)

    f0 = count_reachable_with_parity(dist_map, t0)
    f1 = count_reachable_with_parity(dist_map, t1)
    f2 = count_reachable_with_parity(dist_map, t2)

    # Восстанавливаем квадратику f(n) = a*n^2 + b*n + c по n = 0,1,2
    # f(0) = c = f0
    # f(1) = a + b + c = f1
    # f(2) = 4a + 2b + c = f2
    c = f0
    a_plus_b = f1 - c
    four_a_plus_two_b = f2 - c

    # 4a + 2b - 2(a + b) = 2a => a = (f2 - 2*f1 + f0) / 2
    a = (f2 - 2 * f1 + f0) // 2
    b = a_plus_b - a

    # Ищем f(k)
    result = a * k * k + b * k + c
    return str(result)


# ----------------- Точка входа -----------------

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
