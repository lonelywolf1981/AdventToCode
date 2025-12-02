def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    # TODO: реализовать
    total = 0
    for line in data.strip().splitlines():
        l, w, h = map(int, line.split("x"))
        s1 = l * w
        s2 = w * h
        s3 = h * l
        total += 2 * (s1 + s2 + s3) + min(s1, s2, s3)
    return str(total)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    # TODO: реализовать
    total = 0
    for line in data.strip().splitlines():
        l, w, h = map(int, line.split("x"))
        # Лента = самый маленький периметр стороны
        perim = min(2 * (l + w), 2 * (w + h), 2 * (h + l))
        # Бантик = объем
        bow = l * w * h
        total += perim + bow
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
