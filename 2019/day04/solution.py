from __future__ import annotations


def parse_range(data: str) -> tuple[int, int]:
    """
    Ожидается одна строка вида:
    172930-683082
    """
    line = data.strip()
    lo, hi = line.split("-")
    return int(lo), int(hi)


def is_valid_part1(n: int) -> bool:
    """
    Условия Part 1:
    - есть двойная цифра
    - цифры не убывают
    """
    s = str(n)

    # Неубывание
    if any(s[i] > s[i+1] for i in range(5)):
        return False

    # Есть двойная цифра
    if not any(s[i] == s[i+1] for i in range(5)):
        return False

    return True


def is_valid_part2(n: int) -> bool:
    """
    Условия Part 2:
    - цифры не убывают
    - есть группа ровно из двух одинаковых цифр
    """
    s = str(n)

    # Неубывание
    if any(s[i] > s[i+1] for i in range(5)):
        return False

    # Подсчёт групп подряд
    groups = []
    cur = s[0]
    count = 1

    for i in range(1, 6):
        if s[i] == cur:
            count += 1
        else:
            groups.append(count)
            cur = s[i]
            count = 1
    groups.append(count)

    # Ищем ровно двойку
    return 2 in groups


def solve_part1(data: str) -> str:
    lo, hi = parse_range(data)
    count = sum(1 for n in range(lo, hi + 1) if is_valid_part1(n))
    return str(count)


def solve_part2(data: str) -> str:
    lo, hi = parse_range(data)
    count = sum(1 for n in range(lo, hi + 1) if is_valid_part2(n))
    return str(count)


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
