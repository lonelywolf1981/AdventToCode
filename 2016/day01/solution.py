# Advent of Code 2016 - Day 1
# Решение для обеих частей (Part 1 и Part 2)
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — вся строка с инструкциями, например:
# R2, L3, R2, R4, L2, L1

from pathlib import Path
import re


def parse_instructions(data: str):
    """
    Преобразует строку вида 'R2, L3, R2' или с переносами строк
    в список кортежей ('R', 2), ('L', 3), ...
    """
    data = data.strip()
    if not data:
        return []

    # Разбиваем по запятым и любым пробельным символам
    tokens = re.split(r"[,\s]+", data)
    res = []
    for t in tokens:
        t = t.strip()
        if not t:
            continue
        turn = t[0]
        steps_str = t[1:]
        if not steps_str:
            raise ValueError(f"Нет числа шагов в токене: {t!r}")
        steps = int(steps_str)
        res.append((turn, steps))
    return res


def _ensure_parsed(instructions):
    """
    Вспомогательная функция:
    если на вход пришла строка – распарсить,
    если уже список – вернуть как есть.
    """
    if isinstance(instructions, str):
        return parse_instructions(instructions)
    return instructions


def solve_part1(instructions):
    """
    Part 1:
    Идём по всем инструкциям и считаем конечные координаты.
    Возвращаем манхэттенское расстояние от (0, 0).
    """
    instructions = _ensure_parsed(instructions)

    # направления в порядке: север, восток, юг, запад
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_idx = 0  # 0 - север

    x, y = 0, 0

    for turn, steps in instructions:
        if turn == "R":
            dir_idx = (dir_idx + 1) % 4
        elif turn == "L":
            dir_idx = (dir_idx - 1) % 4
        else:
            raise ValueError(f"Unknown turn: {turn!r}")

        dx, dy = dirs[dir_idx]
        x += dx * steps
        y += dy * steps

    return abs(x) + abs(y)


def solve_part2(instructions):
    """
    Part 2:
    Идём по шагам по одному, запоминая все посещённые клетки.
    Как только попадаем в клетку второй раз – возвращаем её манхэттенское расстояние.
    Если такой клетки нет, возвращаем None.
    """
    instructions = _ensure_parsed(instructions)

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_idx = 0  # 0 - север

    x, y = 0, 0
    visited = set()
    visited.add((x, y))

    for turn, steps in instructions:
        if turn == "R":
            dir_idx = (dir_idx + 1) % 4
        elif turn == "L":
            dir_idx = (dir_idx - 1) % 4
        else:
            raise ValueError(f"Unknown turn: {turn!r}")

        dx, dy = dirs[dir_idx]

        for _ in range(steps):
            x += dx
            y += dy
            if (x, y) in visited:
                return abs(x) + abs(y)
            visited.add((x, y))

    return None


def main():
    # Локальный запуск: читаем input.txt из текущей папки
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:", part2 if part2 is not None else "no repeated location")


if __name__ == "__main__":
    main()


