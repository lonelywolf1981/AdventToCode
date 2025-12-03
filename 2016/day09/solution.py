# Advent of Code 2016 - Day 9
# Explosives in Cyberspace
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — сжатая строка с маркерами вида (AxB).

from pathlib import Path


def _clean_data(data: str) -> str:
    """
    Превращаем вход в одну строку без пробелов и переводов строк.
    Для AoC 2016 Day 9 это корректно: значимы только буквы и скобки.
    """
    # Склеиваем строки, убирая пробелы по краям.
    s = "".join(line.strip() for line in data.splitlines())
    return s


def _decompressed_length_v1(s: str) -> int:
    """
    Part 1:
    Считаем длину распакованной строки, НЕ раскручивая вложенные маркеры.
    Логика:
      - при встрече (AxB): берём следующие A символов как "сырой блок"
        (маркеры внутри не рассматриваем) и просто добавляем A * B к длине.
    """
    i = 0
    total_len = 0
    n = len(s)

    while i < n:
        if s[i] == "(":
            # читаем маркер (AxB)
            end = s.index(")", i)
            marker = s[i + 1:end]  # A x B
            a_str, b_str = marker.lower().split("x")
            a = int(a_str)
            b = int(b_str)

            # добавляем длину блока
            total_len += a * b

            # пропускаем маркер и A символов
            i = end + 1 + a
        else:
            # обычный символ
            total_len += 1
            i += 1

    return total_len


def _decompressed_length_v2(s: str, start: int, end: int) -> int:
    """
    Part 2:
    Рекурсивный подсчёт длины распакованной строки на участке s[start:end].
    Внутри маркера (AxB) считаем длину повторяемого блока тоже рекурсивно.
    """
    i = start
    total_len = 0

    while i < end:
        if s[i] == "(":
            # читаем маркер (AxB)
            close = s.index(")", i)
            marker = s[i + 1:close]  # A x B
            a_str, b_str = marker.lower().split("x")
            a = int(a_str)
            b = int(b_str)

            block_start = close + 1
            block_end = block_start + a

            # рекурсивно считаем длину блока
            inner_len = _decompressed_length_v2(s, block_start, block_end)
            total_len += inner_len * b

            i = block_end
        else:
            # обычный символ
            total_len += 1
            i += 1

    return total_len


def solve_part1(data: str) -> int:
    """
    Part 1:
    Возвращаем длину распакованной строки без учёта вложенности маркеров.
    """
    s = _clean_data(data)
    if not s:
        return 0
    return _decompressed_length_v1(s)


def solve_part2(data: str) -> int:
    """
    Part 2:
    Возвращаем длину распакованной строки с учётом вложенных маркеров.
    """
    s = _clean_data(data)
    if not s:
        return 0
    return _decompressed_length_v2(s, 0, len(s))


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
