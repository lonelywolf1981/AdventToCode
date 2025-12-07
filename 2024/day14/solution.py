import re
from typing import List, Tuple, Set

# Размеры поля для реального инпута AoC 2024 Day 14
WIDTH = 101
HEIGHT = 103


def parse(data: str) -> List[Tuple[int, int, int, int]]:
    """
    Парсим строки вида:
    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    ...
    Возвращаем список кортежей (x, y, vx, vy).
    """
    robots = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        nums = list(map(int, re.findall(r"-?\d+", line)))
        if len(nums) != 4:
            continue
        x, y, vx, vy = nums
        robots.append((x, y, vx, vy))
    return robots


def simulate_position(x: int, y: int, vx: int, vy: int, t: int) -> Tuple[int, int]:
    """
    Позиция робота через t секунд с учётом тороидального поля.
    """
    nx = (x + vx * t) % WIDTH
    ny = (y + vy * t) % HEIGHT
    return nx, ny


def solve_part1(data: str) -> str:
    # Day 14 Part 1:
    # Считаем позиции через 100 секунд и safety factor по квадрантам.

    robots = parse(data)
    t = 100

    mid_x = WIDTH // 2
    mid_y = HEIGHT // 2

    ul = ur = ll = lr = 0  # upper-left, upper-right, lower-left, lower-right

    for x, y, vx, vy in robots:
        nx, ny = simulate_position(x, y, vx, vy, t)

        # Игнорируем роботов на разделяющих линиях
        if nx == mid_x or ny == mid_y:
            continue

        if nx < mid_x and ny < mid_y:
            ul += 1
        elif nx > mid_x and ny < mid_y:
            ur += 1
        elif nx < mid_x and ny > mid_y:
            ll += 1
        elif nx > mid_x and ny > mid_y:
            lr += 1

    safety_factor = ul * ur * ll * lr
    return str(safety_factor)


def solve_part2(data: str) -> str:
    """
    Day 14 Part 2:
    Ищем момент времени, когда роботы образуют "картинку".
    Вместо минимального bounding box ищем момент, когда
    наибольшая связная компонента (по 4-соседству) максимальна.
    """

    robots = parse(data)
    if not robots:
        return "0"

    period = WIDTH * HEIGHT  # полный период конфигураций (101 * 103)

    best_t = 0
    best_cluster = -1

    # 4-соседство
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for t in range(period):
        # Считаем позиции всех роботов в момент t
        positions: Set[Tuple[int, int]] = set()
        for x, y, vx, vy in robots:
            nx = (x + vx * t) % WIDTH
            ny = (y + vy * t) % HEIGHT
            positions.add((nx, ny))

        # Находим размер наибольшей связной компоненты
        seen: Set[Tuple[int, int]] = set()
        max_comp = 0

        for pos in positions:
            if pos in seen:
                continue

            # DFS/BFS из этой точки
            stack = [pos]
            seen.add(pos)
            size = 0

            while stack:
                r, c = stack.pop()
                size += 1
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in positions and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        stack.append((nr, nc))

            if size > max_comp:
                max_comp = size

        # Обновляем лучший момент
        if max_comp > best_cluster:
            best_cluster = max_comp
            best_t = t

    return str(best_t)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
