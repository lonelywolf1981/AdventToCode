# Advent of Code 2016 - Day 16
# Dragon Checksum
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> str
#   solve_part2(raw_input: str) -> str
#
# В файле input.txt — одна строка: начальные данные из 0 и 1.
#
# Part 1: длина диска 272
# Part 2: длина диска 35651584

from pathlib import Path


def _get_initial_state(data: str) -> str:
    """
    Берём первую непустую строку как исходное состояние.
    """
    for line in data.splitlines():
        line = line.strip()
        if line:
            return line
    raise ValueError("Initial state not found in input")


def _fill_disk(initial: str, disk_length: int) -> str:
    """
    Заполняет диск по правилу 'драконьих данных' до нужной длины
    и обрезает до disk_length.
    Реализация через список символов для эффективности.
    """
    arr = list(initial)

    while len(arr) < disk_length:
        # b = reverse(arr) с инвертированными битами
        b = ['1' if c == '0' else '0' for c in reversed(arr)]
        arr.append('0')
        arr.extend(b)

    # отрезаем до нужной длины
    return ''.join(arr[:disk_length])


def _checksum(data: str) -> str:
    """
    Считает контрольную сумму, пока длина строки чётная.
    Возвращает итоговую строку checksum (нечётной длины).
    """
    s = data
    while len(s) % 2 == 0:
        # собираем новую строку из пар
        out = []
        for i in range(0, len(s), 2):
            a = s[i]
            b = s[i + 1]
            out.append('1' if a == b else '0')
        s = ''.join(out)
    return s


def _solve_for_length(raw_input: str, disk_length: int) -> str:
    """
    Общая логика для обеих частей: нужная длина диска задаётся параметром.
    """
    initial = _get_initial_state(raw_input)
    filled = _fill_disk(initial, disk_length)
    return _checksum(filled)


def solve_part1(data: str) -> str:
    """
    Part 1:
    Длина диска 272, вернуть checksum в виде строки из 0 и 1.
    """
    return _solve_for_length(data, 272)


def solve_part2(data: str) -> str:
    """
    Part 2:
    Длина диска 35651584, вернуть checksum.
    """
    return _solve_for_length(data, 35651584)


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
