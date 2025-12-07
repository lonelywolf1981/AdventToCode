from functools import lru_cache
from typing import List, Tuple


def parse(data: str) -> Tuple[List[str], List[str]]:
    """
    Формат:
        r, wr, b, g, bwu, rb, gb, br

        brwrr
        bggr
        ...
    """
    blocks = data.strip().split("\n\n")
    if len(blocks) < 2:
        return [], []

    patterns_line = blocks[0].strip()
    designs_block = blocks[1]

    patterns = [p.strip() for p in patterns_line.split(",") if p.strip()]
    designs = [line.strip() for line in designs_block.splitlines() if line.strip()]

    return patterns, designs


def solve_part1(data: str) -> str:
    # Day 19 Part 1:
    # Для каждого дизайна проверяем, можно ли его набрать из паттернов.
    patterns, designs = parse(data)
    if not patterns or not designs:
        return "0"

    # Для ускорения: максимальная длина паттерна
    max_len = max(len(p) for p in patterns) if patterns else 0

    @lru_cache(maxsize=None)
    def can_build(design: str) -> bool:
        if design == "":
            return True

        # Ограничим перебор длиной максимального паттерна
        # (всё равно дальше смысла нет)
        for p in patterns:
            if design.startswith(p):
                if can_build(design[len(p):]):
                    return True
        return False

    count = 0
    for d in designs:
        if can_build(d):
            count += 1

    return str(count)


def solve_part2(data: str) -> str:
    # Day 19 Part 2:
    # Для каждого дизайна считаем количество способов его собрать
    # и суммируем.
    patterns, designs = parse(data)
    if not patterns or not designs:
        return "0"

    max_len = max(len(p) for p in patterns) if patterns else 0

    @lru_cache(maxsize=None)
    def ways(design: str) -> int:
        # Кол-во способов собрать строку design из паттернов
        if design == "":
            return 1  # один способ: ничего не добавлять

        total = 0
        for p in patterns:
            if design.startswith(p):
                total += ways(design[len(p):])
        return total

    total_sum = 0
    for d in designs:
        total_sum += ways(d)

    return str(total_sum)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
