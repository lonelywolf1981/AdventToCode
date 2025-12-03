# Advent of Code 2016 - Day 3
# Squares With Three Sides
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — строки вида:
#  566  477  376

from pathlib import Path


def _parse_rows(data: str):
    """
    Парсит вход в список строк, где каждая строка -> [a, b, c] (int).
    Игнорирует пустые строки.
    """
    rows = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        # split() без аргументов схлопывает любые пробелы
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(f"Ожидалось 3 числа в строке, получено {len(parts)}: {line!r}")
        a, b, c = map(int, parts)
        rows.append((a, b, c))
    return rows


def _is_valid_triangle(a: int, b: int, c: int) -> bool:
    """
    Проверяет неравенство треугольника:
    сумма любых двух сторон должна быть больше третьей.
    """
    sides = sorted((a, b, c))
    return sides[0] + sides[1] > sides[2]


def solve_part1(data: str) -> int:
    """
    Part 1:
    Каждая строка входа — один треугольник.
    Возвращает количество корректных треугольников.
    """
    rows = _parse_rows(data)
    count = 0
    for a, b, c in rows:
        if _is_valid_triangle(a, b, c):
            count += 1
    return count


def solve_part2(data: str) -> int:
    """
    Part 2:
    Треугольники читаются по столбцам блоками по 3 строки.
    Для каждой тройки строк:
      (r0[0], r1[0], r2[0])
      (r0[1], r1[1], r2[1])
      (r0[2], r1[2], r2[2])
    Возвращает количество корректных треугольников.
    """
    rows = _parse_rows(data)

    if len(rows) % 3 != 0:
        raise ValueError("Количество строк должно быть кратно 3 для part 2")

    count = 0

    for i in range(0, len(rows), 3):
        r0 = rows[i]
        r1 = rows[i + 1]
        r2 = rows[i + 2]

        # три треугольника по столбцам
        for col in range(3):
            a = r0[col]
            b = r1[col]
            c = r2[col]
            if _is_valid_triangle(a, b, c):
                count += 1

    return count


def main():
    # Локальный запуск: читаем input.txt из текущей папки
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()

