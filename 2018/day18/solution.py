from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Dict


def parse_input(data: str) -> List[List[str]]:
    """
    Превращаем input.txt в сетку символов '.', '|' и '#'.
    Пустые строки игнорируем.
    """
    grid: List[List[str]] = []
    for line in data.splitlines():
        line = line.rstrip("\n")
        if not line:
            continue
        grid.append(list(line))
    return grid


def count_adjacent(grid: List[List[str]], y: int, x: int) -> Tuple[int, int, int]:
    """
    Подсчитываем, сколько вокруг клетки (y,x) символов '.', '|', '#'
    среди 8 соседей.
    """
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0

    dots = trees = yards = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            ny = y + dy
            nx = x + dx
            if 0 <= ny < h and 0 <= nx < w:
                ch = grid[ny][nx]
                if ch == ".":
                    dots += 1
                elif ch == "|":
                    trees += 1
                elif ch == "#":
                    yards += 1
    return dots, trees, yards


def step(grid: List[List[str]]) -> List[List[str]]:
    """
    Делаем один "тик" автомата.
    """
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0

    new_grid: List[List[str]] = [row[:] for row in grid]

    for y in range(h):
        for x in range(w):
            ch = grid[y][x]
            _, trees, yards = count_adjacent(grid, y, x)

            if ch == ".":
                # An open acre will become filled with trees if three or more
                # adjacent acres contained trees. Otherwise, nothing happens.
                if trees >= 3:
                    new_grid[y][x] = "|"
            elif ch == "|":
                # An acre filled with trees will become a lumberyard if
                # three or more adjacent acres were lumberyards.
                if yards >= 3:
                    new_grid[y][x] = "#"
            elif ch == "#":
                # A lumberyard will remain a lumberyard if it was adjacent to
                # at least one other lumberyard and at least one acre of trees.
                # Otherwise, it becomes open.
                if not (yards >= 1 and trees >= 1):
                    new_grid[y][x] = "."

    return new_grid


def resource_value(grid: List[List[str]]) -> int:
    """
    Вычисляет "resource value" = (#деревьев) * (#лесопилок).
    """
    trees = sum(row.count("|") for row in grid)
    yards = sum(row.count("#") for row in grid)
    return trees * yards


def simulate_minutes(grid: List[List[str]], minutes: int) -> List[List[str]]:
    """
    Наивная симуляция "minutes" шагов без цикла (для Part 1 / небольших T).
    """
    current = grid
    for _ in range(minutes):
        current = step(current)
    return current


def simulate_with_cycle(grid: List[List[str]], target_minute: int) -> List[List[str]]:
    """
    Симуляция с детекцией цикла для больших T (Part 2).
    Идея:
      - сохраняем строковое представление состояния -> номер минуты
      - когда состояние повторилось, вычисляем длину цикла
      - перескакиваем вперёд по модулю длины цикла
    """
    seen: Dict[str, int] = {}         # state_str -> minute
    states: List[str] = []            # список состояний по минутам
    grids: List[List[List[str]]] = [] # реальные сетки для восстановления

    current = grid
    minute = 0

    while minute < target_minute:
        state_str = "\n".join("".join(row) for row in current)

        if state_str in seen:
            # цикл найден
            first = seen[state_str]
            cycle_len = minute - first

            # сколько минут осталось пройти
            remaining = target_minute - minute
            # на какой итоговой минуте в рамках цикла мы окажемся
            offset = remaining % cycle_len
            final_minute = minute + offset

            # если offset == 0, значит итоговое состояние такое же, как сейчас
            if offset == 0:
                return current

            # иначе можем восстановить состояние через states/grids
            # states[first] соответствует минуте first, мы уже хранили grid для каждого minute
            idx = first + offset
            return grids[idx]

        # ещё не видели это состояние — запоминаем
        seen[state_str] = minute
        states.append(state_str)
        grids.append(current)

        # делаем шаг
        current = step(current)
        minute += 1

    return current


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    grid = parse_input(data)
    if not grid:
        return "0"

    final = simulate_minutes(grid, 10)
    value = resource_value(final)
    return str(value)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    grid = parse_input(data)
    if not grid:
        return "0"

    TARGET = 1_000_000_000
    final = simulate_with_cycle(grid, TARGET)
    value = resource_value(final)
    return str(value)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
