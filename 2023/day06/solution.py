import re
from pathlib import Path


def parse_input(data: str):
    lines = [line for line in data.splitlines() if line.strip()]
    if len(lines) < 2:
        return [], []

    # Первая строка: "Time: 7 15 30"
    times = list(map(int, re.findall(r"\d+", lines[0])))
    # Вторая строка: "Distance: 9 40 200"
    dists = list(map(int, re.findall(r"\d+", lines[1])))

    return times, dists


def count_ways(time: int, dist: int) -> int:
    """
    Считает, для скольких целых h выполняется:
        h * (time - h) > dist
    Используем чистый целочисленный бинарный поиск (без float).
    """
    # Поиск минимального h, который побеждает рекорд
    lo, hi = 0, time
    first = None
    while lo <= hi:
        mid = (lo + hi) // 2
        traveled = mid * (time - mid)
        if traveled > dist:
            first = mid
            hi = mid - 1
        else:
            lo = mid + 1

    if first is None:
        return 0  # ни одно h не побеждает рекорд

    # Поиск максимального h, который побеждает рекорд
    lo, hi = 0, time
    last = None
    while lo <= hi:
        mid = (lo + hi) // 2
        traveled = mid * (time - mid)
        if traveled > dist:
            last = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return last - first + 1


def solve_part1(data: str) -> str:
    times, dists = parse_input(data)
    if not times:
        return "0"

    result = 1
    for t, d in zip(times, dists):
        ways = count_ways(t, d)
        result *= ways

    return str(result)


def solve_part2(data: str) -> str:
    times, dists = parse_input(data)
    if not times:
        return "0"

    # Склеиваем числа: [7, 15, 30] -> 71530
    big_time = int("".join(str(x) for x in times))
    big_dist = int("".join(str(x) for x in dists))

    ways = count_ways(big_time, big_dist)
    return str(ways)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
