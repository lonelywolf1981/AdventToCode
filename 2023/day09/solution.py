from pathlib import Path


def parse_input(data: str):
    lines = [line for line in data.splitlines() if line.strip()]
    histories = []
    for line in lines:
        nums = list(map(int, line.split()))
        histories.append(nums)
    return histories


def build_levels(seq):
    """Строит уровни разностей до строки из нулей."""
    levels = [seq]
    while any(x != 0 for x in levels[-1]):
        prev = levels[-1]
        diff = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        levels.append(diff)
    return levels


def solve_part1(data: str) -> str:
    histories = parse_input(data)
    total = 0

    for seq in histories:
        levels = build_levels(seq)

        # расширяем снизу вверх справа
        next_val = 0
        for level in reversed(levels):
            next_val = level[-1] + next_val

        total += next_val

    return str(total)


def solve_part2(data: str) -> str:
    histories = parse_input(data)
    total = 0

    for seq in histories:
        levels = build_levels(seq)

        # расширяем снизу вверх слева
        prev_val = 0
        for level in reversed(levels):
            prev_val = level[0] - prev_val

        total += prev_val

    return str(total)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
