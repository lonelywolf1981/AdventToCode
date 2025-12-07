import re


def parse(data: str):
    """
    Парсит блоки вида:
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    i = 0
    machines = []

    while i < len(lines):
        # Button A
        m = re.match(r"Button A: X\+(\d+), Y\+(\d+)", lines[i])
        Ax, Ay = int(m.group(1)), int(m.group(2))
        i += 1

        # Button B
        m = re.match(r"Button B: X\+(\d+), Y\+(\d+)", lines[i])
        Bx, By = int(m.group(1)), int(m.group(2))
        i += 1

        # Prize
        m = re.match(r"Prize: X=(\d+), Y=(\d+)", lines[i])
        Tx, Ty = int(m.group(1)), int(m.group(2))
        i += 1

        machines.append((Ax, Ay, Bx, By, Tx, Ty))

    return machines


def solve_machine(Ax, Ay, Bx, By, Tx, Ty):
    """
    Возвращает (a, b) или None, если нет целочисленного решения.
    """
    D = Ax * By - Ay * Bx
    if D == 0:
        return None

    # Формулы Крамера
    a_num = Tx * By - Ty * Bx
    b_num = Ax * Ty - Ay * Tx

    if a_num % D != 0 or b_num % D != 0:
        return None

    a = a_num // D
    b = b_num // D

    if a < 0 or b < 0:
        return None

    return a, b


def solve_part1(data: str) -> str:
    # Part 1: ищем точное решение, считаем стоимость.
    machines = parse(data)
    total = 0

    for Ax, Ay, Bx, By, Tx, Ty in machines:
        sol = solve_machine(Ax, Ay, Bx, By, Tx, Ty)
        if sol is not None:
            a, b = sol
            total += a * 3 + b * 1

    return str(total)


def solve_part2(data: str) -> str:
    # Part 2: цели огромные — добавляем 10^13 к каждой координате цели.
    machines = parse(data)
    total = 0
    OFFSET = 10000000000000

    for Ax, Ay, Bx, By, Tx, Ty in machines:
        Tx2 = Tx + OFFSET
        Ty2 = Ty + OFFSET

        sol = solve_machine(Ax, Ay, Bx, By, Tx2, Ty2)
        if sol is not None:
            a, b = sol
            total += a * 3 + b * 1

    return str(total)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
