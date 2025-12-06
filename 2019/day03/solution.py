from __future__ import annotations

from typing import Dict, Tuple


Point = Tuple[int, int]


def parse_input(data: str) -> tuple[list[str], list[str]]:
    """
    Ожидается две строки:
    R8,U5,L5,D3
    U7,R6,D4,L4
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if len(lines) != 2:
        raise ValueError(f"Ожидается 2 строки с проводами, а получено: {len(lines)}")

    wire1 = [cmd.strip() for cmd in lines[0].split(",") if cmd.strip()]
    wire2 = [cmd.strip() for cmd in lines[1].split(",") if cmd.strip()]
    return wire1, wire2


def trace_wire(wire: list[str]) -> Dict[Point, int]:
    """
    Проходим по проводу шаг за шагом.
    Возвращаем словарь:
        точка -> минимальное количество шагов до неё.
    """
    x, y = 0, 0
    steps = 0
    visited: Dict[Point, int] = {}

    directions = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    for cmd in wire:
        direction = cmd[0]
        length = int(cmd[1:])
        dx, dy = directions[direction]

        for _ in range(length):
            x += dx
            y += dy
            steps += 1
            pt = (x, y)
            # Сохраняем только первое достижение точки
            if pt not in visited:
                visited[pt] = steps

    return visited


def solve_part1(data: str) -> str:
    """
    Находим минимальное манхэттенское расстояние от (0,0)
    до любой общей точки двух проводов.
    """
    wire1, wire2 = parse_input(data)

    wire1_steps = trace_wire(wire1)

    # Для второго провода идём на лету, не храним все точки
    x, y = 0, 0
    steps = 0
    best_distance = None

    directions = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    for cmd in wire2:
        direction = cmd[0]
        length = int(cmd[1:])
        dx, dy = directions[direction]

        for _ in range(length):
            x += dx
            y += dy
            steps += 1
            pt = (x, y)

            if pt in wire1_steps:
                dist = abs(x) + abs(y)
                if best_distance is None or dist < best_distance:
                    best_distance = dist

    if best_distance is None:
        raise RuntimeError("Провода не пересекаются (кроме точки (0,0)).")

    return str(best_distance)


def solve_part2(data: str) -> str:
    """
    Находим минимальное суммарное количество шагов двух проводов
    до любой общей точки.
    """
    wire1, wire2 = parse_input(data)

    wire1_steps = trace_wire(wire1)

    x, y = 0, 0
    steps = 0
    best_steps = None

    directions = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    for cmd in wire2:
        direction = cmd[0]
        length = int(cmd[1:])
        dx, dy = directions[direction]

        for _ in range(length):
            x += dx
            y += dy
            steps += 1
            pt = (x, y)

            if pt in wire1_steps:
                total = steps + wire1_steps[pt]
                if best_steps is None or total < best_steps:
                    best_steps = total

    if best_steps is None:
        raise RuntimeError("Провода не пересекаются (кроме точки (0,0)).")

    return str(best_steps)


if __name__ == "__main__":
    import pathlib
    import sys

    input_path = pathlib.Path("input.txt")
    data = input_path.read_text(encoding="utf-8").strip("\n")

    part = sys.argv[1] if len(sys.argv) > 1 else "both"

    if part in ("1", "one", "part1", "both"):
        print("Part 1:", solve_part1(data))
    if part in ("2", "two", "part2", "both"):
        print("Part 2:", solve_part2(data))
