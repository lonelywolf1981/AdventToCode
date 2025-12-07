from pathlib import Path
from math import gcd


def parse_input(data: str):
    lines = [line for line in data.splitlines() if line.strip() or line == ""]
    if not lines:
        return "", {}

    directions = lines[0].strip()
    graph = {}

    for line in lines[2:]:  # пропускаем строку с направлениями и пустую
        line = line.strip()
        if not line:
            continue
        # Формат: AAA = (BBB, CCC)
        left, right = line.split("=", 1)
        node = left.strip()
        rest = right.strip()
        # убираем скобки и пробелы
        rest = rest.strip()
        # ожидаем "(BBB, CCC)"
        rest = rest.strip("()")
        l_str, r_str = rest.split(",")
        l_str = l_str.strip()
        r_str = r_str.strip()
        graph[node] = (l_str, r_str)

    return directions, graph


def solve_part1(data: str) -> str:
    directions, graph = parse_input(data)
    if not directions or not graph:
        return "0"

    pos = "AAA"
    steps = 0
    n = len(directions)

    while pos != "ZZZ":
        d = directions[steps % n]
        left, right = graph[pos]
        pos = left if d == "L" else right
        steps += 1

    return str(steps)


def steps_to_first_Z(start: str, directions: str, graph: dict) -> int:
    """Считает, через сколько шагов из start впервые попадём в узел, заканчивающийся на 'Z'."""
    pos = start
    steps = 0
    n = len(directions)

    # По условию AoC для реального ввода цикл существует и достижим
    while not pos.endswith("Z"):
        d = directions[steps % n]
        left, right = graph[pos]
        pos = left if d == "L" else right
        steps += 1

    return steps


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def solve_part2(data: str) -> str:
    directions, graph = parse_input(data)
    if not directions or not graph:
        return "0"

    # стартовые узлы: все, что оканчиваются на 'A'
    starts = [node for node in graph.keys() if node.endswith("A")]
    if not starts:
        return "0"

    # для каждого стартового узла считаем длину цикла до первой 'Z'
    lengths = []
    for s in starts:
        length = steps_to_first_Z(s, directions, graph)
        lengths.append(length)

    # берём НОК всех длин
    cur_lcm = lengths[0]
    for x in lengths[1:]:
        cur_lcm = lcm(cur_lcm, x)

    return str(cur_lcm)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
