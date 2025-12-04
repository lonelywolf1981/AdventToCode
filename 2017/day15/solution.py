from pathlib import Path
from typing import Tuple


MOD = 2147483647
FACTOR_A = 16807
FACTOR_B = 48271
MASK_16 = (1 << 16) - 1  # 0xFFFF


def _parse_input(data: str) -> Tuple[int, int]:
    """
    Ожидаем две строки вида:
      Generator A starts with 65
      Generator B starts with 8921
    Возвращаем начальные значения (start_a, start_b).
    """
    start_a = None
    start_b = None

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        # Последнее слово — стартовое значение
        val = int(parts[-1])
        if "Generator" in parts and "A" in parts:
            start_a = val
        elif "Generator" in parts and "B" in parts:
            start_b = val

    if start_a is None or start_b is None:
        raise ValueError("Не удалось распарсить стартовые значения A и B")

    return start_a, start_b


def solve_part1(data: str) -> int:
    """
    Day 15, Part 1:
    40_000_000 пар значений A и B, считаем совпадения нижних 16 бит.
    """
    start_a, start_b = _parse_input(data)

    a = start_a
    b = start_b
    matches = 0

    for _ in range(40_000_000):
        a = (a * FACTOR_A) % MOD
        b = (b * FACTOR_B) % MOD

        if (a & MASK_16) == (b & MASK_16):
            matches += 1

    return matches


def solve_part2(data: str) -> int:
    """
    Day 15, Part 2:
    Генератор A -> берём только значения, кратные 4.
    Генератор B -> берём только значения, кратные 8.
    Считаем совпадения нижних 16 бит на первых 5_000_000 парах.
    """
    start_a, start_b = _parse_input(data)

    a = start_a
    b = start_b
    matches = 0
    pairs = 0

    while pairs < 5_000_000:
        # Генерируем A до кратного 4
        while True:
            a = (a * FACTOR_A) % MOD
            if a % 4 == 0:
                break

        # Генерируем B до кратного 8
        while True:
            b = (b * FACTOR_B) % MOD
            if b % 8 == 0:
                break

        if (a & MASK_16) == (b & MASK_16):
            matches += 1

        pairs += 1

    return matches


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
