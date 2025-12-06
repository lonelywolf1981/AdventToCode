import re
from pathlib import Path
from typing import List, Tuple


Point = Tuple[int, int, int, int]  # x, y, vx, vy


def parse_input(data: str) -> List[Point]:
    """
    Разбираем строки вида:
    position=< 9,  1> velocity=< 0,  2>
    """
    points: List[Point] = []
    pattern = re.compile(
        r"position=<\s*(-?\d+),\s*(-?\d+)>\s+velocity=<\s*(-?\d+),\s*(-?\d+)>"
    )

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if m:
            x = int(m.group(1))
            y = int(m.group(2))
            vx = int(m.group(3))
            vy = int(m.group(4))
            points.append((x, y, vx, vy))

    return points


def tick(points: List[Point]) -> List[Point]:
    """
    Двигает все точки на один шаг.
    """
    return [(x + vx, y + vy, vx, vy) for (x, y, vx, vy) in points]


def bounding_box(points: List[Point]):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def render(points: List[Point]) -> str:
    """
    Рисуем ASCII картинку по текущему расположению точек.
    """
    min_x, max_x, min_y, max_y = bounding_box(points)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    grid = [["."] * width for _ in range(height)]

    for x, y, vx, vy in points:
        grid[y - min_y][x - min_x] = "#"

    return "\n".join("".join(row) for row in grid)


def solve(data: str):
    points = parse_input(data)

    # Ищем момент, когда bounding box минимален
    best_area = None
    best_time = 0
    best_points = points

    time = 0
    current = points

    # Перебираем разумный диапазон (обычно решение достигается быстро).
    # Если input очень большой — можно искать до роста bounding box.
    for t in range(200000):  # безопасный верхний предел
        min_x, max_x, min_y, max_y = bounding_box(current)
        area = (max_x - min_x) * (max_y - min_y)

        if best_area is None or area < best_area:
            best_area = area
            best_time = t
            best_points = current
        else:
            # bounding box начал расти → предыдущий момент был оптимальным
            break

        current = tick(current)

    return best_points, best_time


def solve_part1(data: str) -> str:
    best_points, best_time = solve(data)
    return render(best_points)


def solve_part2(data: str) -> str:
    best_points, best_time = solve(data)
    return str(best_time)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""

    print("Part 1:")
    print(solve_part1(raw))
    print("\nPart 2:", solve_part2(raw))
