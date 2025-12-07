from pathlib import Path
from collections import deque


# направления (dr, dc)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def parse_input(data: str):
    grid = [list(line) for line in data.splitlines() if line.strip()]
    return grid, len(grid), len(grid[0])


def simulate_beam(grid, n, m, start_r, start_c, start_dir):
    """
    Запускает один луч из (start_r, start_c) в направлении start_dir.
    Возвращает количество "заряженных" клеток.
    """
    # visited[(r,c,dir)] = True
    visited = set()
    energized = set()

    queue = deque()
    queue.append((start_r, start_c, start_dir))

    while queue:
        r, c, direction = queue.popleft()

        dr, dc = direction
        nr, nc = r + dr, c + dc

        # Вышли за карту — конец луча
        if nr < 0 or nr >= n or nc < 0 or nc >= m:
            continue

        state = (nr, nc, direction)
        if state in visited:
            continue
        visited.add(state)
        energized.add((nr, nc))

        tile = grid[nr][nc]

        if tile == ".":
            queue.append((nr, nc, direction))

        elif tile == "/":
            # отражение
            if direction == UP:
                queue.append((nr, nc, RIGHT))
            elif direction == DOWN:
                queue.append((nr, nc, LEFT))
            elif direction == LEFT:
                queue.append((nr, nc, DOWN))
            elif direction == RIGHT:
                queue.append((nr, nc, UP))

        elif tile == "\\":
            if direction == UP:
                queue.append((nr, nc, LEFT))
            elif direction == DOWN:
                queue.append((nr, nc, RIGHT))
            elif direction == LEFT:
                queue.append((nr, nc, UP))
            elif direction == RIGHT:
                queue.append((nr, nc, DOWN))

        elif tile == "|":
            if direction in (UP, DOWN):
                # проходит прямо
                queue.append((nr, nc, direction))
            else:
                # раздваивается вверх/вниз
                queue.append((nr, nc, UP))
                queue.append((nr, nc, DOWN))

        elif tile == "-":
            if direction in (LEFT, RIGHT):
                queue.append((nr, nc, direction))
            else:
                # раздваивается вправо/влево
                queue.append((nr, nc, LEFT))
                queue.append((nr, nc, RIGHT))

    return len(energized)


def solve_part1(data: str) -> str:
    grid, n, m = parse_input(data)
    result = simulate_beam(grid, n, m, 0, -1, RIGHT)  # старт за пределами (0,-1) → вход в (0,0)
    return str(result)


def solve_part2(data: str) -> str:
    grid, n, m = parse_input(data)
    best = 0

    # Запуски с левой и правой границы
    for r in range(n):
        best = max(best, simulate_beam(grid, n, m, r, -1, RIGHT))
        best = max(best, simulate_beam(grid, n, m, r, m, LEFT))

    # Запуски с верхней и нижней границы
    for c in range(m):
        best = max(best, simulate_beam(grid, n, m, -1, c, DOWN))
        best = max(best, simulate_beam(grid, n, m, n, c, UP))

    return str(best)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
