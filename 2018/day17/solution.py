from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Set, Tuple

# Увеличиваем глубину рекурсии — без фанатизма, но с запасом
sys.setrecursionlimit(20000)

Coord = Tuple[int, int]


def parse_input(data: str):
    """
    Парсим строки вида:
      x=495, y=2..7
      y=7, x=495..501

    Возвращаем:
      clay   — множество координат (x, y) с глиной
      y_min  — минимальный y глины
      y_max  — максимальный y глины
    """
    clay: Set[Coord] = set()
    pat = re.compile(r"([xy])=(\d+),\s*([xy])=(\d+)\.\.(\d+)")

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        m = pat.match(line)
        if not m:
            continue
        a1, v1, a2, s, e = m.groups()
        v1 = int(v1)
        s = int(s)
        e = int(e)

        if a1 == "x":
            x = v1
            for y in range(s, e + 1):
                clay.add((x, y))
        else:
            y = v1
            for x in range(s, e + 1):
                clay.add((x, y))

    ys = [y for (_, y) in clay]
    y_min = min(ys)
    y_max = max(ys)
    return clay, y_min, y_max


def simulate(data: str):
    """
    Основная симуляция.
    Возвращает (part1, part2):
      part1 — клетки с водой ('|' или '~') между y_min и y_max
      part2 — клетки только со стоячей водой '~' между y_min и y_max
    """
    clay, y_min, y_max = parse_input(data)

    flowing: Set[Coord] = set()  # текущая вода '|'
    still: Set[Coord] = set()    # стоячая вода '~'

    def has_support(x: int, y: int) -> bool:
        """Есть ли в клетке (x, y) опора (глина или стоячая вода)."""
        return (x, y) in clay or (x, y) in still

    def flow(x: int, y: int) -> None:
        """
        Классический DFS:
        1) Падаем вниз, пока можем.
        2) Как только внизу опора — пытаемся растечься влево/вправо.
        3) Если слева и справа всё стенками ограничено — строку заполняем '~'
           и поднимаемся на уровень выше.
        4) Если есть утечки — остаётся текущая вода '|' и рекурсивно льём вниз.
        """
        # Если ушли ниже интересующей области — дальше нам не важно.
        if y > y_max:
            return

        # Если тут уже глина/вода — повторно не льём.
        if (x, y) in clay or (x, y) in flowing or (x, y) in still:
            return

        # Шаг 1: падаем вниз, пока под нами нет опоры
        while True:
            if y > y_max:
                return
            flowing.add((x, y))
            if not has_support(x, y + 1):
                y += 1
                continue
            break  # внизу опора

        # Шаг 2: пытаемся растечься по уровню
        while True:
            # Влево
            left = x
            left_leak = None
            while True:
                # если снизу нет опоры — утечка
                if not has_support(left, y + 1):
                    left_leak = left
                    break
                # если упёрлись в стенку — стоп
                if (left - 1, y) in clay:
                    break
                left -= 1

            # Вправо
            right = x
            right_leak = None
            while True:
                if not has_support(right, y + 1):
                    right_leak = right
                    break
                if (right + 1, y) in clay:
                    break
                right += 1

            # Если нет утечек ни слева, ни справа — бассейн, всё становится '~'
            if left_leak is None and right_leak is None:
                for xx in range(left, right + 1):
                    still.add((xx, y))
                    # текущая вода там больше не нужна
                    if (xx, y) in flowing:
                        flowing.remove((xx, y))
                # Поднимаемся уровнем выше, пытаясь заполнить вверх
                y -= 1
                if y < 0:
                    return
                # и повторяем попытку растекания наверху
                continue
            else:
                # Есть утечки — клетки по уровню отмечаем как текущую воду
                for xx in range(left, right + 1):
                    flowing.add((xx, y))

                # Сами утечки — новые точки "падения" вниз
                if left_leak is not None:
                    flow(left_leak, y + 1)
                if right_leak is not None:
                    flow(right_leak, y + 1)
                return

    # Запускаем поток от источника (500, 0)
    flow(500, 0)

    # Подсчёт результата
    part1 = sum(1 for (x, y) in flowing | still if y_min <= y <= y_max)
    part2 = sum(1 for (x, y) in still if y_min <= y <= y_max)
    return part1, part2


def solve_part1(data: str) -> str:
    if not data.strip():
        return "0"
    p1, _ = simulate(data)
    return str(p1)


def solve_part2(data: str) -> str:
    if not data.strip():
        return "0"
    _, p2 = simulate(data)
    return str(p2)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
