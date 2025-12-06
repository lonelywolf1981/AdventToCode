from pathlib import Path
from typing import Set, Tuple


def parse_input(data: str) -> Tuple[Set[int], Set[str]]:
    """
    Парсим вход:
    initial state: #..#.#..

    ..... => .
    ...## => #
    и т.п.

    Возвращаем:
    - множество позиций, где есть растения
    - множество паттернов длины 5, которые дают '#'
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return set(), set()

    # первая строка — initial state
    first = lines[0]
    if not first.startswith("initial state:"):
        raise ValueError("Ожидалась строка 'initial state:' в первой строке")

    state_str = first.split(":", 1)[1].strip()
    state: Set[int] = {i for i, ch in enumerate(state_str) if ch == "#"}

    rules_hash: Set[str] = set()
    for line in lines[1:]:
        if "=>" not in line:
            continue
        pattern, result = [s.strip() for s in line.split("=>", 1)]
        if result == "#" and len(pattern) == 5:
            rules_hash.add(pattern)

    return state, rules_hash


def step(state: Set[int], rules_hash: Set[str]) -> Set[int]:
    """
    Делаем один шаг эволюции.
    Для каждого потенциального горшка смотрим окно из 5 позиций
    и проверяем, есть ли оно в rules_hash.
    """
    if not state:
        return set()

    new_state: Set[int] = set()
    min_i = min(state)
    max_i = max(state)

    # С запасом по 2 горшка в каждую сторону
    for i in range(min_i - 2, max_i + 3):
        pattern = []
        for pos in range(i - 2, i + 3):
            pattern.append("#" if pos in state else ".")
        pattern_str = "".join(pattern)
        if pattern_str in rules_hash:
            new_state.add(i)

    return new_state


def pots_sum(state: Set[int]) -> int:
    return sum(state)


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    state, rules_hash = parse_input(data)
    generations = 20

    for _ in range(generations):
        state = step(state, rules_hash)

    return str(pots_sum(state))


def solve_part2(data: str) -> str:
    """
    Решение части 2. Нужно 50_000_000_000 поколений.

    На практике рисунок быстро стабилизируется: форма остаётся той же,
    а сумма индексов растёт линейно (каждое поколение прибавляется одно и то же).
    Мы:
    - идём по поколениям
    - отслеживаем разницу сумм (delta)
    - как только delta несколько десятков/сотен поколений подряд одинаковая,
      считаем, что достигнута линейная фаза и экстраполируем.
    """
    TARGET = 50_000_000_000
    state, rules_hash = parse_input(data)

    if not state:
        return "0"

    prev_sum = pots_sum(state)
    prev_delta = None
    same_delta_count = 0

    # Верхний предел для "ручной" симуляции — с большим запасом
    MAX_STEPS = 5000

    for gen in range(1, MAX_STEPS + 1):
        state = step(state, rules_hash)
        curr_sum = pots_sum(state)
        delta = curr_sum - prev_sum

        if delta == prev_delta:
            same_delta_count += 1
        else:
            same_delta_count = 1
            prev_delta = delta

        # Если дельта держится достаточно долго — считаем, что стабилизировалось
        if same_delta_count >= 100:
            remaining = TARGET - gen
            final_sum = curr_sum + remaining * delta
            return str(final_sum)

        prev_sum = curr_sum

    # На случай, если не увидели стабилизацию (маловероятно для AoC-входов),
    # просто возвращаем сумму после MAX_STEPS.
    return str(prev_sum)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
