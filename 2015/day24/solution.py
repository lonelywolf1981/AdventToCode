from itertools import combinations
from math import prod
from typing import List


def parse_weights(data: str) -> List[int]:
    return [int(line.strip()) for line in data.strip().splitlines() if line.strip()]


def find_best_group(weights: List[int], groups: int) -> int:
    """
    Ищем минимальный quantum entanglement (произведение группы)
    среди наименьших по размеру групп с нужной суммой.
    """
    target = sum(weights) // groups
    weights = sorted(weights, reverse=True)  # ускоряет поиск

    # 1. Ищем минимальное кол-во элементов, которые могут дать target
    for size in range(1, len(weights) + 1):
        valid_groups = []
        for combo in combinations(weights, size):
            if sum(combo) == target:
                valid_groups.append(combo)

        if valid_groups:
            # Найдены группы минимального размера — выбираем QE
            return min(prod(c) for c in valid_groups)

    return -1  # не должно происходить для валидного input


def solve_part1(data: str) -> str:
    weights = parse_weights(data)
    result = find_best_group(weights, groups=3)
    return str(result)


def solve_part2(data: str) -> str:
    weights = parse_weights(data)
    result = find_best_group(weights, groups=4)
    return str(result)


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
