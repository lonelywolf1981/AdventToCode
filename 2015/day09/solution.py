from itertools import permutations


def parse(data: str):
    distances = {}
    cities = set()

    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        # Формат: A to B = N
        lhs, dist = line.split(" = ")
        a, _, b = lhs.split()
        d = int(dist)

        cities.add(a)
        cities.add(b)

        distances[(a, b)] = d
        distances[(b, a)] = d

    return cities, distances


def path_length(path, distances):
    total = 0
    for i in range(len(path) - 1):
        total += distances[(path[i], path[i + 1])]
    return total


def solve_part1(data: str) -> str:
    cities, distances = parse(data)
    best = float("inf")

    for perm in permutations(cities):
        dist = path_length(perm, distances)
        if dist < best:
            best = dist

    return str(best)


def solve_part2(data: str) -> str:
    cities, distances = parse(data)
    best = 0

    for perm in permutations(cities):
        dist = path_length(perm, distances)
        if dist > best:
            best = dist

    return str(best)


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
