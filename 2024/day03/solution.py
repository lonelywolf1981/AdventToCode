import re


def solve_part1(data: str) -> str:
    # Day 3 Part 1: найти все mul(X,Y) и просуммировать X*Y.
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    total = 0
    for x, y in pattern.findall(data):
        total += int(x) * int(y)
    return str(total)


def solve_part2(data: str) -> str:
    # Day 3 Part 2:
    # Учитываем состояние enable/disable через do() и don't().

    mul_pat = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    do_pat = re.compile(r"do\(\)")
    dont_pat = re.compile(r"don't\(\)")

    i = 0
    total = 0
    enabled = True
    n = len(data)

    while i < n:
        # Проверяем все управляющие токены
        if data.startswith("don't()", i):
            enabled = False
            i += len("don't()")
            continue
        if data.startswith("do()", i):
            enabled = True
            i += len("do()")
            continue

        # Проверяем mul(...)
        m = mul_pat.match(data, i)
        if m:
            if enabled:
                x, y = m.groups()
                total += int(x) * int(y)
            i = m.end()
            continue

        # Иначе просто идём дальше
        i += 1

    return str(total)


if __name__ == "__main__":
    from pathlib import Path
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
