def parse(data: str):
    reindeers = []
    for line in data.strip().splitlines():
        parts = line.split()
        name = parts[0]
        speed = int(parts[3])
        fly_time = int(parts[6])
        rest_time = int(parts[13])
        reindeers.append((name, speed, fly_time, rest_time))
    return reindeers


def distance_after(seconds: int, speed: int, fly_time: int, rest_time: int) -> int:
    cycle = fly_time + rest_time
    full_cycles = seconds // cycle
    remain = seconds % cycle
    active = full_cycles * fly_time + min(fly_time, remain)
    return active * speed


def solve_part1(data: str) -> str:
    reindeers = parse(data)
    T = 2503

    best = 0
    for _, speed, fly, rest in reindeers:
        d = distance_after(T, speed, fly, rest)
        if d > best:
            best = d

    return str(best)


def solve_part2(data: str) -> str:
    reindeers = parse(data)
    T = 2503

    # очки за лидерство
    scores = {name: 0 for name, *_ in reindeers}

    # текущее расстояние каждого
    distances = {name: 0 for name, *_ in reindeers}

    # моделируем поминутно
    for t in range(1, T + 1):
        # обновляем расстояния
        for name, speed, fly_time, rest_time in reindeers:
            cycle = fly_time + rest_time
            if (t - 1) % cycle < fly_time:  # олень летит
                distances[name] += speed

        # определяем максимальное расстояние в данный момент
        lead = max(distances.values())

        # все лидеры получают по 1 очку
        for name in distances:
            if distances[name] == lead:
                scores[name] += 1

    return str(max(scores.values()))


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
