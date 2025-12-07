from pathlib import Path


def parse_input(data: str):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    out = []
    for line in lines:
        a, b, c = line.split()
        steps = int(b)
        color = c[2:-1]  # режем "#xxxxxx)"
        out.append((a, steps, color))
    return out


# Направления для part 1
DIR1 = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}

# Направления для part 2 (из последнего хекса)
DIR2 = {
    0: (0, 1),   # R
    1: (1, 0),   # D
    2: (0, -1),  # L
    3: (-1, 0),  # U
}


def solve_generic(instructions, mode: int) -> int:
    """
    mode = 1  → Part 1 (направления из первой колонки)
    mode = 2  → Part 2 (направления и длины из hex-кода)
    """

    x = 0
    y = 0
    border = 0  # количество граничных шагов (B)
    area2 = 0   # удвоенная ориентированная площадь (по формуле шнурка)

    for d1, steps1, color in instructions:
        if mode == 1:
            dx, dy = DIR1[d1]
            steps = steps1
        else:
            # hex-код: первые 5 символов — длина, последний — направление
            steps = int(color[:5], 16)
            dir_id = int(color[5], 16)
            dx, dy = DIR2[dir_id]

        nx = x + dx * steps
        ny = y + dy * steps

        # shoelace: суммируем x_i * y_{i+1} - x_{i+1} * y_i
        area2 += x * ny - nx * y

        border += steps  # каждая единица шага добавляет граничную точку (ребро)
        x, y = nx, ny

    # площадь должна быть положительной: берём модуль
    area2 = abs(area2)

    # Pick's theorem:
    # Area = I + B/2 - 1
    # I = Area - B/2 + 1
    # Area = area2 / 2
    # I = area2/2 - B/2 + 1
    #
    # Но нас в AoC интересует количество клеток внутри + граничные,
    # и стандартный ответ дня 18 считается как:
    #   inside + border = area2/2 + border/2 + 1
    #
    # Поэтому возвращаем именно это:
    lagoon = area2 // 2 + border // 2 + 1
    return lagoon


def solve_part1(data: str) -> str:
    instructions = parse_input(data)
    return str(solve_generic(instructions, mode=1))


def solve_part2(data: str) -> str:
    instructions = parse_input(data)
    return str(solve_generic(instructions, mode=2))


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
