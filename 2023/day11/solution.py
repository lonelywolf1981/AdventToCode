from pathlib import Path


def parse_input(data: str):
    grid = [list(line) for line in data.splitlines() if line.strip()]
    n = len(grid)
    m = len(grid[0])
    return grid, n, m


def find_galaxies(grid, n, m):
    """Возвращает список координат всех галактик (#)."""
    g = []
    for r in range(n):
        for c in range(m):
            if grid[r][c] == "#":
                g.append((r, c))
    return g


def expanded_positions(galaxies, empty_rows, empty_cols, growth):
    """
    Применяет "расширение" карты к координатам галактик.
    growth = 2 для Part 1,
    growth = 1_000_000 для Part 2.
    """
    result = []
    for (r, c) in galaxies:
        # количество пустых строк/столбцов ДО этой позиции
        add_r = sum(1 for x in empty_rows if x < r)
        add_c = sum(1 for x in empty_cols if x < c)

        new_r = r + add_r * (growth - 1)
        new_c = c + add_c * (growth - 1)

        result.append((new_r, new_c))
    return result


def solve(data: str, growth: int) -> int:
    grid, n, m = parse_input(data)
    galaxies = find_galaxies(grid, n, m)

    # Находим полностью пустые строки
    empty_rows = []
    for r in range(n):
        if all(grid[r][c] == "." for c in range(m)):
            empty_rows.append(r)

    # Находим полностью пустые столбцы
    empty_cols = []
    for c in range(m):
        if all(grid[r][c] == "." for r in range(n)):
            empty_cols.append(c)

    # Применяем расширение
    expanded = expanded_positions(galaxies, empty_rows, empty_cols, growth)

    # Считаем попарные манхэттенские расстояния
    total = 0
    for i in range(len(expanded)):
        r1, c1 = expanded[i]
        for j in range(i + 1, len(expanded)):
            r2, c2 = expanded[j]
            total += abs(r1 - r2) + abs(c1 - c2)

    return total


def solve_part1(data: str) -> str:
    return str(solve(data, growth=2))


def solve_part2(data: str) -> str:
    return str(solve(data, growth=1_000_000))


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
