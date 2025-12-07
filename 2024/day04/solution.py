def parse_grid(data: str) -> list[str]:
    # Убираем пустые строки и переводим в список строк-строчек поля
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    return lines


def solve_part1(data: str) -> str:
    # Day 4 Part 1:
    # В сетке букв посчитать все вхождения слова "XMAS"
    # по 8 направлениям (горизонталь, вертикаль, диагонали).

    grid = parse_grid(data)
    if not grid:
        return "0"

    rows = len(grid)
    cols = len(grid[0])
    target = "XMAS"
    tlen = len(target)

    # 8 направлений: (dr, dc)
    directions = [
        (-1, 0),  # вверх
        (1, 0),   # вниз
        (0, -1),  # влево
        (0, 1),   # вправо
        (-1, -1), # диагональ вверх-влево
        (-1, 1),  # диагональ вверх-вправо
        (1, -1),  # диагональ вниз-влево
        (1, 1),   # диагональ вниз-вправо
    ]

    total = 0

    for r in range(rows):
        for c in range(cols):
            # пробуем стартовать слово из клетки (r, c)
            for dr, dc in directions:
                rr, cc = r, c
                ok = True
                for i in range(tlen):
                    # выход за границы
                    if not (0 <= rr < rows and 0 <= cc < cols):
                        ok = False
                        break
                    if grid[rr][cc] != target[i]:
                        ok = False
                        break
                    rr += dr
                    cc += dc
                if ok:
                    total += 1

    return str(total)


def solve_part2(data: str) -> str:
    # Day 4 Part 2:
    # Считаем количество "X-образных MAS":
    #   - центр 'A'
    #   - обе диагонали: "MAS" или "SAM".

    grid = parse_grid(data)
    if not grid:
        return "0"

    rows = len(grid)
    cols = len(grid[0])

    total = 0

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != 'A':
                continue

            # Первая диагональ: (r-1,c-1), (r,c), (r+1,c+1)
            d1 = grid[r - 1][c - 1] + grid[r][c] + grid[r + 1][c + 1]
            # Вторая диагональ: (r-1,c+1), (r,c), (r+1,c-1)
            d2 = grid[r - 1][c + 1] + grid[r][c] + grid[r + 1][c - 1]

            if d1 in ("MAS", "SAM") and d2 in ("MAS", "SAM"):
                total += 1

    return str(total)


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
