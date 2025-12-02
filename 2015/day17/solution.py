from typing import List


TARGET = 150  # по условию AoC 2015 Day 17


def parse(data: str) -> List[int]:
    return [int(line.strip()) for line in data.strip().splitlines() if line.strip()]


def solve_part1(data: str) -> str:
    containers = parse(data)
    n = len(containers)

    count = 0
    # Перебираем все подмножества
    for mask in range(1 << n):
        total = 0
        for i in range(n):
            if mask & (1 << i):
                total += containers[i]
        if total == TARGET:
            count += 1

    return str(count)


def solve_part2(data: str) -> str:
    containers = parse(data)
    n = len(containers)

    solutions = []

    # Собираем все решения
    for mask in range(1 << n):
        total = 0
        used = 0
        for i in range(n):
            if mask & (1 << i):
                total += containers[i]
                used += 1
        if total == TARGET:
            solutions.append(used)

    # выбираем минимальное число контейнеров
    min_used = min(solutions)

    # считаем сколько наборов имеют это минимальное количество
    count_min = sum(1 for x in solutions if x == min_used)

    return str(count_min)


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
