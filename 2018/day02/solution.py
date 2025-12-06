from collections import Counter
from itertools import combinations
from pathlib import Path


def parse_input(data: str) -> list[str]:
    """
    Разбирает содержимое input.txt в список ID коробок (строки без пустых).
    """
    ids: list[str] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        ids.append(line)
    return ids


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    box_ids = parse_input(data)

    twos = 0   # строк с буквой, встречающейся ровно 2 раза
    threes = 0 # строк с буквой, встречающейся ровно 3 раза

    for s in box_ids:
        cnt = Counter(s)
        has_two = any(v == 2 for v in cnt.values())
        has_three = any(v == 3 for v in cnt.values())
        if has_two:
            twos += 1
        if has_three:
            threes += 1

    checksum = twos * threes
    return str(checksum)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    box_ids = parse_input(data)

    # Брутфорс по всем парам строк: ищем те, что отличаются ровно в одной позиции.
    for a, b in combinations(box_ids, 2):
        if len(a) != len(b):
            continue

        diff_count = 0
        diff_index = -1

        for i, (ca, cb) in enumerate(zip(a, b)):
            if ca != cb:
                diff_count += 1
                diff_index = i
                if diff_count > 1:
                    break

        if diff_count == 1:
            # Общие буквы: всё, кроме отличающегося символа
            common = a[:diff_index] + a[diff_index + 1 :]
            return common

    # На всякий случай, если пара не найдена (по условию AoC она есть)
    return ""


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
