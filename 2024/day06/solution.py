from __future__ import annotations


def parse_map(data: str):
    grid = [list(line.rstrip("\n")) for line in data.splitlines() if line.strip()]
    if not grid:
        return [], None, None, None

    rows = len(grid)
    cols = len(grid[0])

    start_r = start_c = None
    start_dir = None

    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch in "^v<>":
                start_r, start_c = r, c
                start_dir = ch
                grid[r][c] = "."  # дальше считаем эту клетку как пустую

    return grid, start_r, start_c, start_dir


# направления: символ → (dr, dc)
DIRS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

# поворот направо
TURN_RIGHT = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
}


def walk_once(grid, sr, sc, sdir):
    """
    Симуляция пути для Part 1.
    Возвращает множество посещённых клеток (r, c).
    """
    rows = len(grid)
    cols = len(grid[0])

    r, c, d = sr, sc, sdir
    visited = set()

    while True:
        visited.add((r, c))
        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc

        # выходим за карту — патруль закончен
        if not (0 <= nr < rows and 0 <= nc < cols):
            break

        # перед нами препятствие — поворот направо, остаёмся на месте
        if grid[nr][nc] == "#":
            d = TURN_RIGHT[d]
            continue

        # иначе двигаемся вперёд
        r, c = nr, nc

    return visited


def causes_loop(grid, sr, sc, sdir, br, bc):
    """
    Проверяет, приведёт ли добавление стены в (br, bc)
    к бесконечному циклу.
    """
    rows = len(grid)
    cols = len(grid[0])

    # нельзя ставить стену на старт или поверх уже существующей
    if (br, bc) == (sr, sc):
        return False
    if grid[br][bc] == "#":
        return False

    # состояние: (r, c, dir)
    seen_states = set()
    r, c, d = sr, sc, sdir

    while True:
        state = (r, c, d)
        if state in seen_states:
            # вернулись в то же положение с тем же направлением — цикл
            return True
        seen_states.add(state)

        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc

        # выход за карту — цикла нет
        if not (0 <= nr < rows and 0 <= nc < cols):
            return False

        # с учётом новой стены
        is_blocked = (nr == br and nc == bc) or (grid[nr][nc] == "#")
        if is_blocked:
            d = TURN_RIGHT[d]
            continue

        r, c = nr, nc


def solve_part1(data: str) -> str:
    # Day 6 Part 1: симулируем маршрут и считаем число уникальных посещённых клеток.

    grid, sr, sc, sdir = parse_map(data)
    if not grid or sr is None:
        return "0"

    visited = walk_once(grid, sr, sc, sdir)
    return str(len(visited))


def solve_part2(data: str) -> str:
    # Day 6 Part 2:
    # Добавляем одну стену в пустую клетку так, чтобы маршрут стал бесконечным.
    # Считаем количество таких позиций.

    grid, sr, sc, sdir = parse_map(data)
    if not grid or sr is None:
        return "0"

    rows = len(grid)
    cols = len(grid[0])

    # Оптимизация: стена, поставленная вне исходного пути, ничего не изменит.
    # Поэтому сначала получаем множество клеток, по которым реально ходит охранник.
    path_cells = walk_once(grid, sr, sc, sdir)

    count = 0
    for (r, c) in path_cells:
        # старт уже отфильтруем в causes_loop
        if causes_loop(grid, sr, sc, sdir, r, c):
            count += 1

    return str(count)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
