from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Dict, Set


Point = Tuple[int, int]


def parse_input(data: str) -> List[Point]:
    """
    Разбор входных координат.
    Формат строк: 'x, y'
    """
    points: List[Point] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        # поддержка форматов "1, 2" и "1,2"
        if "," in line:
            left, right = line.split(",", 1)
            x = int(left.strip())
            y = int(right.strip())
            points.append((x, y))
        else:
            # на всякий случай, если формат другой
            parts = line.replace(";", " ").split()
            if len(parts) >= 2:
                x = int(parts[0])
                y = int(parts[1])
                points.append((x, y))
    return points


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bounding_box(points: List[Point]) -> Tuple[int, int, int, int]:
    """
    Возвращает (min_x, max_x, min_y, max_y) для списка точек.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    points = parse_input(data)
    if not points:
        return "0"

    min_x, max_x, min_y, max_y = bounding_box(points)

    # area_count[i] — количество клеток, принадлежащих точке i
    area_count: Dict[int, int] = {i: 0 for i in range(len(points))}
    # infinite — индексы точек, области которых уходят в бесконечность
    infinite: Set[int] = set()

    # Проходим по всем клеткам bounding box
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            dists = []
            for idx, p in enumerate(points):
                d = manhattan((x, y), p)
                dists.append((d, idx))
            dists.sort(key=lambda x: x[0])

            # Проверяем, есть ли единственный ближайший
            if len(dists) >= 2 and dists[0][0] == dists[1][0]:
                # ничья, клетка никому не принадлежит
                continue

            closest_idx = dists[0][1]
            area_count[closest_idx] += 1

            # Если клетка на границе bounding box — область этой точки бесконечна
            if x == min_x or x == max_x or y == min_y or y == max_y:
                infinite.add(closest_idx)

    # Максимальная конечная область
    best = 0
    for idx, cnt in area_count.items():
        if idx in infinite:
            continue
        if cnt > best:
            best = cnt

    return str(best)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    points = parse_input(data)
    if not points:
        return "0"

    min_x, max_x, min_y, max_y = bounding_box(points)

    # Порог для суммы расстояний по условию AoC 2018 Day 6
    THRESHOLD = 10000

    # Чтобы не пропустить область за пределами bounding box,
    # расширим прямоугольник на небольшой отступ, зависящий от порога и числа точек.
    padding = THRESHOLD // len(points) + 2
    min_x_ext = min_x - padding
    max_x_ext = max_x + padding
    min_y_ext = min_y - padding
    max_y_ext = max_y + padding

    region_size = 0

    for y in range(min_y_ext, max_y_ext + 1):
        for x in range(min_x_ext, max_x_ext + 1):
            total_dist = 0
            for p in points:
                total_dist += manhattan((x, y), p)
                if total_dist >= THRESHOLD:
                    break
            if total_dist < THRESHOLD:
                region_size += 1

    return str(region_size)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
