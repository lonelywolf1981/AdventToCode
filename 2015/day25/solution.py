import re


MOD = 33554393
MULT = 252533
START = 20151125


def parse_row_col(data: str) -> tuple[int, int]:
    """
    Парсим номер строки и столбца из текста вида:
    'Enter the code at row 3010, column 3019.'
    """
    # Сначала пробуем красивый шаблон
    m = re.search(r"row\s+(\d+),\s*column\s+(\d+)", data, re.IGNORECASE)
    if m:
        row = int(m.group(1))
        col = int(m.group(2))
        return row, col

    # На всякий случай: просто возьмем последние две цифры в тексте
    nums = re.findall(r"\d+", data)
    if len(nums) >= 2:
        row, col = map(int, nums[-2:])
        return row, col

    raise ValueError("Не удалось распознать row/column в input.txt")


def index_in_sequence(row: int, col: int) -> int:
    """
    Возвращает порядковый номер ячейки (начиная с 1) в последовательности
    генерации кодов по диагоналям.

    Диагонали:
      d = row + col - 1
      diag 1: (1,1)
      diag 2: (2,1),(1,2)
      diag 3: (3,1),(2,2),(1,3)
      ...

    Первый элемент диагонали d:
      first_d = 1 + (d-1)*d/2

    Положение внутри диагонали для (row, col):
      offset = d - row

    Итоговый индекс:
      n = first_d + offset
    """
    d = row + col - 1
    first_d = 1 + (d - 1) * d // 2
    offset = d - row
    return first_d + offset


def code_at(row: int, col: int) -> int:
    """
    Считаем код в ячейке (row, col).

    code_n = START * MULT^(n-1) mod MOD
    """
    n = index_in_sequence(row, col)
    # n-я позиция: START * MULT^(n-1) mod MOD
    factor = pow(MULT, n - 1, MOD)
    return (START * factor) % MOD


def solve_part1(data: str) -> str:
    row, col = parse_row_col(data)
    value = code_at(row, col)
    return str(value)


def solve_part2(data: str) -> str:
    # В AoC 2015 Day 25 нет второй части — просто вернем пояснение
    return "No part 2 for Day 25 in AoC 2015"


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
