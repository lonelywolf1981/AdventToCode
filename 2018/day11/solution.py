from pathlib import Path
from typing import List, Tuple


GRID_SIZE = 300


def parse_input(data: str) -> int:
    """
    В input.txt лежит один номер (serial number), например:
    6878
    """
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        return int(line)
    return 0


def power_level(x: int, y: int, serial: int) -> int:
    """
    Формула AoC 2018 Day 11:
    - rack_id = x + 10
    - power = rack_id * y
    - power += serial
    - power *= rack_id
    - digit = сотни power (если нет — 0)
    - level = digit - 5
    """
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    # берём сотни
    digit = (power // 100) % 10
    return digit - 5


def build_grid(serial: int) -> List[List[int]]:
    """
    Строим сетку уровней мощности 1..300 по x и y.
    grid[y][x] (делаем 1-based, а 0-я строка/столбец — заглушка).
    """
    grid = [[0] * (GRID_SIZE + 1) for _ in range(GRID_SIZE + 1)]
    for y in range(1, GRID_SIZE + 1):
        row = grid[y]
        for x in range(1, GRID_SIZE + 1):
            row[x] = power_level(x, y, serial)
    return grid


def build_summed_area(grid: List[List[int]]) -> List[List[int]]:
    """
    Строим summed-area table (интегральную сумму):
    sat[y][x] = сумма grid по прямоугольнику (1,1)-(x,y)
    """
    sat = [[0] * (GRID_SIZE + 1) for _ in range(GRID_SIZE + 1)]
    for y in range(1, GRID_SIZE + 1):
        row_sat = sat[y]
        row_grid = grid[y]
        for x in range(1, GRID_SIZE + 1):
            row_sat[x] = (
                row_grid[x]
                + sat[y - 1][x]
                + row_sat[x - 1]
                - sat[y - 1][x - 1]
            )
    return sat


def square_sum(sat: List[List[int]], x: int, y: int, size: int) -> int:
    """
    Быстро считаем сумму по квадрату (x,y)-(x+size-1,y+size-1) через summed-area.
    """
    x2 = x + size - 1
    y2 = y + size - 1
    return (
        sat[y2][x2]
        - sat[y - 1][x2]
        - sat[y2][x - 1]
        + sat[y - 1][x - 1]
    )


def find_best_fixed_size(sat: List[List[int]], size: int) -> Tuple[int, int, int]:
    """
    Ищем квадрат фиксированного размера size с максимальной суммой.
    Возвращаем (best_x, best_y, best_sum).
    """
    best_sum = None
    best_x = 1
    best_y = 1
    limit = GRID_SIZE - size + 1

    for y in range(1, limit + 1):
        for x in range(1, limit + 1):
            total = square_sum(sat, x, y, size)
            if best_sum is None or total > best_sum:
                best_sum = total
                best_x = x
                best_y = y

    return best_x, best_y, best_sum if best_sum is not None else 0


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    serial = parse_input(data)
    if serial == 0:
        return "0,0"

    grid = build_grid(serial)
    sat = build_summed_area(grid)

    best_x, best_y, _ = find_best_fixed_size(sat, 3)

    # Формат ответа AoC: "x,y"
    return f"{best_x},{best_y}"


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    serial = parse_input(data)
    if serial == 0:
        return "0,0,0"

    grid = build_grid(serial)
    sat = build_summed_area(grid)

    best_sum = None
    best_x = 1
    best_y = 1
    best_size = 1

    # Перебираем все размеры 1..GRID_SIZE
    for size in range(1, GRID_SIZE + 1):
        x, y, total = find_best_fixed_size(sat, size)
        if best_sum is None or total > best_sum:
            best_sum = total
            best_x = x
            best_y = y
            best_size = size

    # Формат ответа AoC: "x,y,size"
    return f"{best_x},{best_y},{best_size}"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
