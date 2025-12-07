def solve_part1(data: str) -> str:
    total = 0

    for line in data.splitlines():
        if not line.strip():
            continue

        left, right = line.split(":")[1].split("|")

        winners = set(left.split())
        numbers = right.split()

        matches = sum(1 for x in numbers if x in winners)

        if matches > 0:
            total += 2 ** (matches - 1)

    return str(total)


def solve_part2(data: str) -> str:
    lines = [line for line in data.splitlines() if line.strip()]
    n = len(lines)

    matches = [0] * n

    # сначала считаем количество совпадений в каждой карточке
    for i, line in enumerate(lines):
        left, right = line.split(":")[1].split("|")
        winners = set(left.split())
        numbers = right.split()
        matches[i] = sum(1 for x in numbers if x in winners)

    # теперь считаем количество копий
    copies = [1] * n  # каждая карточка есть минимум 1 раз

    for i in range(n):
        k = matches[i]
        for j in range(1, k + 1):
            if i + j < n:
                copies[i + j] += copies[i]

    return str(sum(copies))


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip("\n")
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
