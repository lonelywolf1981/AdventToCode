def parse(data: str):
    left = []
    right = []
    for line in data.strip().splitlines():
        a, b = map(int, line.split())
        left.append(a)
        right.append(b)
    return left, right


def solve_part1(data: str) -> str:
    # Краткое описание Day 1 перед решением:
    # Даны два списка чисел. Требуется отсортировать каждый список
    # и суммировать разницу по позициям.

    left, right = parse(data)
    left.sort()
    right.sort()

    total = sum(abs(a - b) for a, b in zip(left, right))
    return str(total)


def solve_part2(data: str) -> str:
    # Краткое описание Day 1 Part 2:
    # Для каждого значения из левого списка умножить его на количество
    # появлений этого значения в правом списке.

    left, right = parse(data)

    # Подсчёт частот правых значений
    from collections import Counter
    cnt = Counter(right)

    total = sum(x * cnt[x] for x in left)
    return str(total)


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
