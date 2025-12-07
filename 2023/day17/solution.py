from pathlib import Path
import heapq


DIRS = [
    (0, 1),   # 0: right
    (1, 0),   # 1: down
    (0, -1),  # 2: left
    (-1, 0),  # 3: up
]


def parse_grid(data: str):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    grid = [[int(ch) for ch in line] for line in lines]
    return grid, len(grid), len(grid[0]) if grid else 0


def dijkstra_with_constraints(grid, rows, cols, min_turn_run, max_run, require_min_run_on_stop):
    """
    Общий решатель для обеих частей.

    min_turn_run:
        - минимальная длина прямого участка, после которой можно ПОВЕРНУТЬ.
        (для part1 = 1, для part2 = 4)

    max_run:
        - максимум подряд шагов в одном направлении (3 или 10).

    require_min_run_on_stop:
        - нужно ли, чтобы при финише последний прямой сегмент был >= min_turn_run
          (False для part1, True для part2).
    """
    end_r, end_c = rows - 1, cols - 1

    # dist[(r, c, dir, run)] = минимальная стоимость
    dist = {}

    heap = []

    # Стартуем из (0,0), делаем первый шаг вправо и вниз (остальные движения заведомо хуже).
    start_r, start_c = 0, 0
    for dir_idx in (0, 1):  # right, down
        dr, dc = DIRS[dir_idx]
        nr, nc = start_r + dr, start_c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            cost = grid[nr][nc]
            state = (nr, nc, dir_idx, 1)
            dist[state] = cost
            heapq.heappush(heap, (cost, nr, nc, dir_idx, 1))

    INF = 10**18
    best_answer = INF

    while heap:
        cost, r, c, dir_idx, run = heapq.heappop(heap)

        # Если это состояние хуже уже найденного — пропускаем
        if dist.get((r, c, dir_idx, run), INF) < cost:
            continue

        # Проверка финиша
        if r == end_r and c == end_c:
            if not require_min_run_on_stop or run >= min_turn_run:
                best_answer = cost
                break

        for ndir in range(4):
            # Нельзя разворачиваться на 180°
            if ndir == (dir_idx + 2) % 4:
                continue

            dr, dc = DIRS[ndir]
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            if ndir == dir_idx:
                # продолжаем прямо
                if run >= max_run:
                    continue
                nrun = run + 1
            else:
                # поворачиваем, проверяем минимальную длину предыдущего сегмента
                if run < min_turn_run:
                    continue
                nrun = 1

            new_cost = cost + grid[nr][nc]
            state = (nr, nc, ndir, nrun)
            if new_cost < dist.get(state, INF):
                dist[state] = new_cost
                heapq.heappush(heap, (new_cost, nr, nc, ndir, nrun))

    return best_answer


def solve_part1(data: str) -> str:
    grid, rows, cols = parse_grid(data)
    if not grid:
        return "0"

    # part1: не больше 3 подряд, поворачивать можно всегда (после хотя бы 1 шага),
    # останавливаться можно в любой момент
    ans = dijkstra_with_constraints(
        grid,
        rows,
        cols,
        min_turn_run=1,
        max_run=3,
        require_min_run_on_stop=False,
    )
    return str(ans)


def solve_part2(data: str) -> str:
    grid, rows, cols = parse_grid(data)
    if not grid:
        return "0"

    # part2: минимум 4 подряд до поворота/остановки, максимум 10 подряд
    ans = dijkstra_with_constraints(
        grid,
        rows,
        cols,
        min_turn_run=4,
        max_run=10,
        require_min_run_on_stop=True,
    )
    return str(ans)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
