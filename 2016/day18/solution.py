# Advent of Code 2016 - Day 18
# Like a Rogue
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — одна строка: начальный ряд из '.' и '^'.

from pathlib import Path


def _get_first_row(data: str) -> str:
    """
    Берём первую непустую строку как исходный ряд.
    """
    for line in data.splitlines():
        line = line.strip()
        if line:
            return line
    raise ValueError("First row not found in input")


def _count_safe_tiles(first_row: str, total_rows: int) -> int:
    """
    Считает общее количество безопасных плиток за total_rows строк,
    начиная с first_row (которая уже входит в количество).
    """
    row = first_row
    width = len(row)

    # считаем безопасные в первой строке
    safe_count = row.count(".")

    for _ in range(1, total_rows):
        prev = row
        new_row_chars = []

        for i in range(width):
            left = prev[i - 1] if i > 0 else "."
            center = prev[i]
            right = prev[i + 1] if i < width - 1 else "."

            l_trap = (left == "^")
            c_trap = (center == "^")
            r_trap = (right == "^")

            # правила ловушек из условия
            is_trap = (
                (l_trap and c_trap and not r_trap) or  # ^^.
                (c_trap and r_trap and not l_trap) or  # .^^
                (l_trap and not c_trap and not r_trap) or  # ^..
                (r_trap and not l_trap and not c_trap)     # ..^
            )

            new_row_chars.append("^" if is_trap else ".")

        row = "".join(new_row_chars)
        safe_count += row.count(".")

    return safe_count


def solve_part1(data: str) -> int:
    """
    Part 1:
    40 строк, вернуть количество безопасных плиток.
    """
    first_row = _get_first_row(data)
    return _count_safe_tiles(first_row, 40)


def solve_part2(data: str) -> int:
    """
    Part 2:
    400000 строк, вернуть количество безопасных плиток.
    """
    first_row = _get_first_row(data)
    return _count_safe_tiles(first_row, 400000)


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
