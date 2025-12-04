from pathlib import Path
from typing import List, Tuple


def _parse_input(data: str) -> List[int]:
    """
    Преобразуем содержимое input.txt в список int.
    Обычно это одна строка с числами через пробел/таб.
    """
    # Соберём все числа из всех непустых строк на всякий случай
    nums: List[int] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        nums.extend(int(x) for x in line.split())
    if not nums:
        raise ValueError("Пустой input для Day 6")
    return nums


def _reallocate(banks: List[int]) -> None:
    """
    Один шаг перераспределения памяти.
    Модифицирует список banks на месте.
    """
    n = len(banks)
    # Находим индекс максимального элемента (минимальный индекс при равенстве)
    max_blocks = max(banks)
    idx = banks.index(max_blocks)

    banks[idx] = 0
    i = idx
    # Раздаём блоки по одному
    while max_blocks > 0:
        i = (i + 1) % n
        banks[i] += 1
        max_blocks -= 1


def _run_cycle(data: str) -> Tuple[int, int]:
    """
    Общая логика для обеих частей:
    Возвращает (steps_before_repeat, loop_size).

    steps_before_repeat — сколько перераспределений до первого повторения конфигурации.
    loop_size          — длина цикла (между первым и вторым появлением конфигурации).
    """
    banks = _parse_input(data)
    seen: dict[Tuple[int, ...], int] = {}
    steps = 0

    while True:
        config = tuple(banks)
        if config in seen:
            first_seen_step = seen[config]
            loop_size = steps - first_seen_step
            return steps, loop_size
        seen[config] = steps
        _reallocate(banks)
        steps += 1


def solve_part1(data: str) -> int:
    """
    Day 6, Part 1:
    Количество перераспределений до первого повторения конфигурации.
    """
    steps, _ = _run_cycle(data)
    return steps


def solve_part2(data: str) -> int:
    """
    Day 6, Part 2:
    Длина цикла между повторениями конфигурации.
    """
    _, loop_size = _run_cycle(data)
    return loop_size


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
