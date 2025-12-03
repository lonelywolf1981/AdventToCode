# Advent of Code 2016 - Day 6
# Signals and Noise
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> str
#   solve_part2(raw_input: str) -> str
#
# В файле input.txt — много строк одинаковой длины.

from pathlib import Path
from collections import Counter


def _parse_lines(data: str):
    """
    Берём все непустые строки, обрезая пробелы по краям.
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return []

    # Можно проверить, что все одной длины (как в AoC)
    length = len(lines[0])
    for line in lines:
        if len(line) != length:
            raise ValueError("Все строки должны быть одной длины")
    return lines


def _decode(lines, *, most_common: bool) -> str:
    """
    Собирает сообщение по столбцам:
      - если most_common=True: берём самый частый символ в колонке
      - если most_common=False: берём самый редкий символ в колонке
    """
    if not lines:
        return ""

    length = len(lines[0])
    result_chars = []

    for col in range(length):
        column_chars = [line[col] for line in lines]
        counts = Counter(column_chars)

        if most_common:
            # максимум по частоте, при равенстве — по символу (для стабильности)
            ch = max(counts.items(), key=lambda kv: (kv[1], -ord(kv[0])))[0]
        else:
            # минимум по частоте, при равенстве — по символу
            ch = min(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]

        result_chars.append(ch)

    return "".join(result_chars)


def solve_part1(data: str) -> str:
    """
    Part 1:
    Сообщение, собранное из самых частых символов в каждой колонке.
    """
    lines = _parse_lines(data)
    return _decode(lines, most_common=True)


def solve_part2(data: str) -> str:
    """
    Part 2:
    Сообщение, собранное из самых редких символов в каждой колонке.
    """
    lines = _parse_lines(data)
    return _decode(lines, most_common=False)


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
