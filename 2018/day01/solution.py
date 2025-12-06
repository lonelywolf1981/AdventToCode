def parse_input(data: str) -> list[int]:
    """
    Разбирает содержимое input.txt в список целых чисел (изменений частоты).
    Поддерживает строки вида '+1', '-2', '3', с пробелами и пустыми строками.
    """
    changes: list[int] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        changes.append(int(line))
    return changes


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    changes = parse_input(data)
    total = sum(changes)
    return str(total)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    changes = parse_input(data)

    seen = set()
    freq = 0
    seen.add(freq)

    # крутим список по кругу, пока не найдём первую повторяющуюся частоту
    # т.к. изменения конечны, просто ходим по ним в бесконечном цикле
    from itertools import cycle

    for delta in cycle(changes):
        freq += delta
        if freq in seen:
            return str(freq)
        seen.add(freq)


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
