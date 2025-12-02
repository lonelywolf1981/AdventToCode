from itertools import permutations
from typing import Dict, Set, Tuple


def parse(data: str) -> Tuple[Set[str], Dict[Tuple[str, str], int]]:
    people: Set[str] = set()
    happiness: Dict[Tuple[str, str], int] = {}

    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        # Пример строки:
        # "Alice would gain 54 happiness units by sitting next to Bob."
        parts = line.rstrip(".").split()
        a = parts[0]
        sign = 1 if parts[2] == "gain" else -1
        amount = int(parts[3]) * sign
        b = parts[-1]

        people.add(a)
        people.add(b)
        happiness[(a, b)] = amount

    return people, happiness


def total_happiness(order, happiness: Dict[Tuple[str, str], int]) -> int:
    n = len(order)
    total = 0
    for i in range(n):
        a = order[i]
        b = order[(i + 1) % n]  # круглый стол
        total += happiness.get((a, b), 0)
        total += happiness.get((b, a), 0)
    return total


def best_arrangement(people: Set[str], happiness: Dict[Tuple[str, str], int]) -> int:
    # Чтобы не считать циклические перестановки как разные,
    # фиксируем одного человека и переставляем остальных.
    people = list(people)
    first = people[0]
    others = people[1:]

    best = float("-inf")
    for perm in permutations(others):
        order = (first,) + perm
        score = total_happiness(order, happiness)
        if score > best:
            best = score

    return best


def solve_part1(data: str) -> str:
    people, happiness = parse(data)
    ans = best_arrangement(people, happiness)
    return str(ans)


def solve_part2(data: str) -> str:
    people, happiness = parse(data)

    # Добавляем "Me" с 0 счастья в обе стороны для всех
    me = "Me"
    for p in list(people):
        happiness[(p, me)] = 0
        happiness[(me, p)] = 0
    people.add(me)

    ans = best_arrangement(people, happiness)
    return str(ans)


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

