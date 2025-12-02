def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    # TODO: реализовать
    floor = 0
    for ch in data:
        if ch == "(":
            floor += 1
        elif ch == ")":
            floor -= 1
    return str(floor)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    # TODO: реализовать
    floor = 0
    # Позиции в задаче считаются с 1
    for i, ch in enumerate(data, start=1):
        if ch == "(":
            floor += 1
        elif ch == ")":
            floor -= 1

        if floor == -1:
            return str(i)

    # На случай, если подвал ни разу не достигнут
    return "not reached"


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
