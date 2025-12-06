from math import gcd, atan2
from typing import List, Tuple, Optional


Point = Tuple[int, int]


def parse_asteroids(data: str) -> List[Point]:
    """
    Парсим карту: '#' — астероид, '.' — пусто.
    Возвращаем список координат (x, y), где x — колонка, y — строка.
    """
    asteroids: List[Point] = []
    for y, line in enumerate(data.splitlines()):
        line = line.strip()
        if not line:
            continue
        for x, ch in enumerate(line):
            if ch == "#":
                asteroids.append((x, y))
    return asteroids


def count_visible_from(asteroids: List[Point], sx: int, sy: int) -> int:
    """
    Сколько астероидов видно из точки (sx, sy).
    Видимость считаем по уникальным направлениям (dx, dy), приведённым к НОД.
    """
    directions = set()
    for (x, y) in asteroids:
        if x == sx and y == sy:
            continue
        dx = x - sx
        dy = y - sy
        g = gcd(dx, dy)
        dx //= g
        dy //= g
        directions.add((dx, dy))
    return len(directions)


def find_best_station(asteroids: List[Point]) -> Tuple[Optional[Point], int]:
    """
    Ищем астероид, с которого видно максимум других.
    Возвращаем (координата_станции_или_None, количество_видимых).
    """
    best_pos: Optional[Point] = None
    best_count = 0
    for (sx, sy) in asteroids:
        visible = count_visible_from(asteroids, sx, sy)
        if visible > best_count:
            best_count = visible
            best_pos = (sx, sy)
    return best_pos, best_count


def vaporization_order(asteroids: List[Point], station: Point) -> List[Point]:
    """
    Строим порядок испарения астероидов лазером.
    Лазер стоит в station и смотрит вверх, вращаясь по часовой.
    Возвращаем список координат астероидов в порядке испарения.
    """
    sx, sy = station

    # Список всех целей, кроме самой станции
    targets: List[Tuple[float, int, int, int]] = []  # (angle, dist2, x, y)

    for (x, y) in asteroids:
        if (x, y) == station:
            continue
        dx = x - sx
        dy = y - sy
        # Угол: 0 — вверх, дальше по часовой
        angle = atan2(dx, -dy)  # хитрый трюк: (dx, -dy), чтобы 0 было сверху
        if angle < 0:
            angle += 2.0 * 3.141592653589793
        dist2 = dx * dx + dy * dy
        targets.append((angle, dist2, x, y))

    # Группируем по углу: на каждом угле несколько астероидов на разных дистанциях
    from collections import defaultdict

    by_angle = defaultdict(list)
    for angle, dist2, x, y in targets:
        by_angle[angle].append((dist2, x, y))

    # В каждом списке сортируем по расстоянию (ближайший первый)
    for angle in by_angle:
        by_angle[angle].sort(key=lambda t: t[0])

    # Список всех углов в порядке вращения
    angles = sorted(by_angle.keys())

    result: List[Point] = []
    # Пока есть что испарять
    while True:
        removed_any = False
        for angle in angles:
            lst = by_angle[angle]
            if lst:
                dist2, x, y = lst.pop(0)
                result.append((x, y))
                removed_any = True
        if not removed_any:
            break

    return result


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    asteroids = parse_asteroids(data)
    if not asteroids:
        return "0"
    _, best_count = find_best_station(asteroids)
    return str(best_count)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    asteroids = parse_asteroids(data)
    if not asteroids:
        return ""

    station, _ = find_best_station(asteroids)
    if station is None:
        return ""

    order = vaporization_order(asteroids, station)

    # По условию нужен 200-й испарённый. Индексация с 1.
    idx = 200 - 1
    if idx >= len(order):
        # На всякий случай, если астероидов меньше 200.
        return ""

    x, y = order[idx]
    answer = 100 * x + y
    return str(answer)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
