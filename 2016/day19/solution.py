# Advent of Code 2016 - Day 19
# An Elephant Named Joseph
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — одно число N: количество эльфов.

from pathlib import Path


def _get_n(data: str) -> int:
    """
    Берём первое непустое целое число из входа как N.
    """
    for line in data.splitlines():
        line = line.strip()
        if line:
            return int(line)
    raise ValueError("Elf count N not found in input")


# ---------------- Part 1: классический Josephus (шаг 2) ---------------- #

def solve_part1(data: str) -> int:
    """
    Part 1:
    Классический круг, каждый эльф забирает подарки у соседа справа.
    Возвращаем номер победившего эльфа.
    Формула: J(N) = 2 * (N - 2^⌊log2(N)⌋) + 1
    """
    n = _get_n(data)
    if n <= 0:
        return 0

    # наибольшая степень двойки <= n
    p = 1
    while p * 2 <= n:
        p *= 2

    winner = 2 * (n - p) + 1
    return winner


# ---------------- Part 2: "через противоположного" (step across) ---------------- #

def solve_part2(data: str) -> int:
    """
    Part 2:
    Каждый эльф забирает подарки у эльфа напротив (через floor(N/2)).
    Используем известную формулу через степени тройки:

      Пусть p = 3^k — наибольшая степень 3, не превосходящая N.

      Если N == p:        ответ = N
      Если p < N <= 2p:   ответ = N - p
      Если 2p < N <= 3p:  ответ = 2N - 3p

    Возвращаем номер победившего эльфа.
    """
    n = _get_n(data)
    if n <= 0:
        return 0

    # наибольшая степень тройки <= n
    p = 1
    while p * 3 <= n:
        p *= 3

    if n == p:
        return n
    elif n <= 2 * p:
        return n - p
    else:
        return 2 * n - 3 * p


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
