from pathlib import Path
from typing import Dict, Tuple, Set


Coord = Tuple[int, int]


def _parse_input(data: str) -> Set[Coord]:
    """
    Парсим карту в множество заражённых узлов для Part 1.
    Центр карты считаем (0,0).
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Пустой input для Day 22")

    h = len(lines)
    w = len(lines[0])

    infected: Set[Coord] = set()

    # Сдвиг, чтобы центр был (0,0)
    offset_y = h // 2
    offset_x = w // 2

    for y, line in enumerate(lines):
        if len(line) != w:
            raise ValueError("Строки карты должны быть одинаковой длины")
        for x, ch in enumerate(line):
            if ch == "#":
                ix = x - offset_x
                iy = y - offset_y
                infected.add((ix, iy))

    return infected


def _turn_left(dx: int, dy: int) -> Tuple[int, int]:
    """
    Поворот налево:
    (dx, dy) -> (dy, -dx)

    Пример:
      вверх (0, -1) -> налево (-1, 0)
    """
    return dy, -dx


def _turn_right(dx: int, dy: int) -> Tuple[int, int]:
    """
    Поворот направо:
    (dx, dy) -> (-dy, dx)

    Пример:
      вверх (0, -1) -> направо (1, 0)
    """
    return -dy, dx


def _reverse(dx: int, dy: int) -> Tuple[int, int]:
    """
    Разворот на 180°.
    """
    return -dx, -dy


def solve_part1(data: str) -> int:
    """
    Day 22, Part 1:
    - стартуем в центре, смотрим вверх
    - 10_000 burst'ов
    - считаем, сколько раз узел стал infected
    """
    infected = _parse_input(data)

    x, y = 0, 0
    dx, dy = 0, -1  # смотрим вверх
    infections = 0

    for _ in range(10_000):
        if (x, y) in infected:
            # infected: поворот направо, теперь clean
            dx, dy = _turn_right(dx, dy)
            infected.remove((x, y))
        else:
            # clean: поворот налево, заражаем
            dx, dy = _turn_left(dx, dy)
            infected.add((x, y))
            infections += 1

        # шаг вперёд
        x += dx
        y += dy

    return infections


def solve_part2(data: str) -> int:
    """
    Day 22, Part 2:
    То же поле, но узлы имеют 4 состояния:
      0 = clean (по умолчанию)
      1 = weakened
      2 = infected
      3 = flagged

    10_000_000 burst'ов, считаем, сколько раз узел стал infected.
    """
    # Начальное состояние: '#' -> infected (2), остальные clean (0)
    initial_infected = _parse_input(data)
    states: Dict[Coord, int] = {coord: 2 for coord in initial_infected}

    x, y = 0, 0
    dx, dy = 0, -1  # вверх
    infections = 0

    for _ in range(10_000_000):
        state = states.get((x, y), 0)  # по умолчанию clean

        if state == 0:
            # clean: поворот налево, -> weakened
            dx, dy = _turn_left(dx, dy)
            states[(x, y)] = 1
        elif state == 1:
            # weakened: прямо, -> infected
            states[(x, y)] = 2
            infections += 1
        elif state == 2:
            # infected: поворот направо, -> flagged
            dx, dy = _turn_right(dx, dy)
            states[(x, y)] = 3
        elif state == 3:
            # flagged: разворот, -> clean
            dx, dy = _reverse(dx, dy)
            if (x, y) in states:
                del states[(x, y)]
        else:
            raise RuntimeError(f"Неизвестное состояние узла: {state}")

        # шаг вперёд
        x += dx
        y += dy

    return infections


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
