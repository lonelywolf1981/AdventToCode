from __future__ import annotations


def parse_masses(data: str) -> list[int]:
    """
    Разбор входных данных: одна масса на строку.
    Пустые строки игнорируем.
    """
    return [int(line) for line in data.splitlines() if line.strip()]


def fuel_for_mass(mass: int) -> int:
    """
    Топливо для одной массы по формуле из части 1.
    Если результат отрицательный — возвращаем 0 (на всякий случай).
    """
    fuel = mass // 3 - 2
    return fuel if fuel > 0 else 0


def fuel_for_mass_recursive(mass: int) -> int:
    """
    Топливо с учётом массы самого топлива (часть 2).
    """
    total = 0
    extra = fuel_for_mass(mass)
    while extra > 0:
        total += extra
        extra = fuel_for_mass(extra)
    return total


def solve_part1(data: str) -> str:
    """
    Part 1: сумма требуемого топлива для всех модулей.
    """
    masses = parse_masses(data)
    total_fuel = sum(fuel_for_mass(m) for m in masses)
    return str(total_fuel)


def solve_part2(data: str) -> str:
    """
    Part 2: сумма топлива с учётом топлива для топлива.
    """
    masses = parse_masses(data)
    total_fuel = sum(fuel_for_mass_recursive(m) for m in masses)
    return str(total_fuel)


if __name__ == "__main__":
    import pathlib
    import sys

    input_path = pathlib.Path("input.txt")
    data = input_path.read_text(encoding="utf-8").strip("\n")

    part = sys.argv[1] if len(sys.argv) > 1 else "both"

    if part in ("1", "one", "part1", "both"):
        print("Part 1:", solve_part1(data))
    if part in ("2", "two", "part2", "both"):
        print("Part 2:", solve_part2(data))
