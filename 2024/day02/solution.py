def parse(data: str):
    return [list(map(int, line.split())) for line in data.strip().splitlines()]


def is_safe(seq):
    """Проверка правила для Part1."""
    diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]

    # либо все >0 (возрастают), либо все <0 (убывают)
    if all(d > 0 for d in diffs):
        pass
    elif all(d < 0 for d in diffs):
        pass
    else:
        return False

    # разница в пределах 1..3
    return all(1 <= abs(d) <= 3 for d in diffs)


def is_safe_with_removal(seq):
    """Part2: можно удалить один элемент."""
    # если и так безопасно
    if is_safe(seq):
        return True

    # пробуем удалить каждый элемент
    for i in range(len(seq)):
        new_seq = seq[:i] + seq[i+1:]
        if is_safe(new_seq):
            return True

    return False


def solve_part1(data: str) -> str:
    # Day 2 Part1 кратко:
    # Строка безопасна, если монотонна (вверх/вниз) и разницы 1..3.

    reports = parse(data)
    ans = sum(is_safe(rep) for rep in reports)
    return str(ans)


def solve_part2(data: str) -> str:
    # Day 2 Part2 кратко:
    # Разрешено удалить один элемент, если после удаления строка становится безопасной.

    reports = parse(data)
    ans = sum(is_safe_with_removal(rep) for rep in reports)
    return str(ans)


if __name__ == "__main__":
    from pathlib import Path
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
