from __future__ import annotations
from typing import List, Dict


# ==========================
#   PART 1
# ==========================

def rating(grid: List[str]) -> int:
    """Считаем biodiversity rating."""
    r = 0
    p = 1
    for y in range(5):
        for x in range(5):
            if grid[y][x] == '#':
                r += p
            p <<= 1
    return r


def neighbors_part1(grid: List[str], x: int, y: int) -> int:
    """Счёт соседей-жуков для части 1."""
    cnt = 0
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < 5 and 0 <= ny < 5 and grid[ny][nx] == '#':
            cnt += 1
    return cnt


def step_part1(grid: List[str]) -> List[str]:
    """Один шаг клеточного автомата."""
    new = []
    for y in range(5):
        row = []
        for x in range(5):
            c = grid[y][x]
            n = neighbors_part1(grid, x, y)
            if c == '#' and n != 1:
                row.append('.')
            elif c == '.' and (n == 1 or n == 2):
                row.append('#')
            else:
                row.append(c)
        new.append(''.join(row))
    return new


def solve_part1(data: str) -> str:
    grid = [line.strip() for line in data.splitlines() if line.strip()]
    seen = set()
    while True:
        r = rating(grid)
        if r in seen:
            return str(r)
        seen.add(r)
        grid = step_part1(grid)


# ==========================
#   PART 2  (recursive)
# ==========================

def empty_level() -> List[str]:
    """Пустой уровень 5x5, с центральной ячейкой как '?'."""
    return [".....", ".....", "..?..", ".....", "....."]


def count_neighbors(levels: Dict[int, List[str]], z: int, x: int, y: int) -> int:
    """
    Соседи на рекурсивных уровнях согласно правилам AoC:
    - (2,2) не существует — переход в уровень z+1
    - внешние края — обращаются к уровню z-1
    """
    cnt = 0
    cur = levels.get(z, empty_level())

    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy

        # Вход во внутренний уровень (через центр)
        if nx == 2 and ny == 2:
            inner = levels.get(z + 1)
            if not inner:
                continue
            # Мы двигаемся в сторону центра, значит в inner берём либо всю строку, либо весь столбец
            if x == 1 and y == 2:
                # слева от центра -> весь левый столбец inner
                for iy in range(5):
                    if inner[iy][0] == '#':
                        cnt += 1
            elif x == 3 and y == 2:
                # справа от центра -> правый столбец inner
                for iy in range(5):
                    if inner[iy][4] == '#':
                        cnt += 1
            elif x == 2 and y == 1:
                # сверху от центра -> верхняя строка inner
                for ix in range(5):
                    if inner[0][ix] == '#':
                        cnt += 1
            elif x == 2 and y == 3:
                # снизу от центра -> нижняя строка inner
                for ix in range(5):
                    if inner[4][ix] == '#':
                        cnt += 1

        # Выход во внешний уровень
        elif nx < 0:
            outer = levels.get(z - 1)
            if outer and outer[2][1] == '#':
                cnt += 1
        elif nx > 4:
            outer = levels.get(z - 1)
            if outer and outer[2][3] == '#':
                cnt += 1
        elif ny < 0:
            outer = levels.get(z - 1)
            if outer and outer[1][2] == '#':
                cnt += 1
        elif ny > 4:
            outer = levels.get(z - 1)
            if outer and outer[3][2] == '#':
                cnt += 1

        # Обычный сосед в том же уровне
        else:
            if cur[ny][nx] == '#':
                cnt += 1

    return cnt


def step_part2(levels: Dict[int, List[str]]) -> Dict[int, List[str]]:
    """Один шаг рекурсивного автомата."""
    new_levels: Dict[int, List[str]] = {}

    if not levels:
        return {}

    zs = list(levels.keys())
    lo = min(zs) - 1
    hi = max(zs) + 1

    for z in range(lo, hi + 1):
        cur = levels.get(z, empty_level())
        new_level_rows: List[str] = []

        for y in range(5):
            row_chars: List[str] = []
            for x in range(5):
                if x == 2 and y == 2:
                    row_chars.append('?')
                    continue

                c = cur[y][x]
                n = count_neighbors(levels, z, x, y)

                if c == '#' and n != 1:
                    row_chars.append('.')
                elif c == '.' and (n == 1 or n == 2):
                    row_chars.append('#')
                else:
                    row_chars.append(c)

            new_level_rows.append(''.join(row_chars))

        # Записываем уровень только если там есть хотя бы один жук
        if any('#' in row for row in new_level_rows):
            new_levels[z] = new_level_rows

    return new_levels


def solve_part2(data: str) -> str:
    # читаем начальную сетку
    raw_grid = [line.strip() for line in data.splitlines() if line.strip()]
    grid0 = [list(row) for row in raw_grid]
    # центр превращаем в '?'
    grid0[2][2] = '?'
    grid0 = ["".join(row) for row in grid0]

    levels: Dict[int, List[str]] = {0: grid0}

    # симулируем 200 минут
    for _ in range(200):
        levels = step_part2(levels)

    # считаем жуков на всех уровнях
    total_bugs = 0
    for lvl in levels.values():
        for row in lvl:
            total_bugs += row.count('#')

    return str(total_bugs)


# ==========================
#   TEMPLATE
# ==========================

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
