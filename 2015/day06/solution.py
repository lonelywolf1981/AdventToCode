def parse_instruction(line: str):
    """
    Разбираем строку команды.
    Возвращаем (cmd, x1, y1, x2, y2),
    где cmd ∈ {"on", "off", "toggle"}.
    """
    parts = line.strip().split()
    if not parts:
        return None

    if parts[0] == "toggle":
        cmd = "toggle"
        coord1 = parts[1]
        coord2 = parts[3]
    else:
        # "turn on" или "turn off"
        cmd = parts[1]  # "on" или "off"
        coord1 = parts[2]
        coord2 = parts[4]

    x1, y1 = map(int, coord1.split(","))
    x2, y2 = map(int, coord2.split(","))

    # Гарантируем, что x1<=x2 и y1<=y2 на всякий случай
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    return cmd, x1, y1, x2, y2


def solve_part1(data: str) -> str:
    # 1000x1000 лампочек, False = выключена, True = включена
    size = 1000
    grid = [[False] * size for _ in range(size)]

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        parsed = parse_instruction(line)
        if parsed is None:
            continue

        cmd, x1, y1, x2, y2 = parsed

        # Перебираем прямоугольник включительно
        for x in range(x1, x2 + 1):
            row = grid[x]
            if cmd == "on":
                for y in range(y1, y2 + 1):
                    row[y] = True
            elif cmd == "off":
                for y in range(y1, y2 + 1):
                    row[y] = False
            elif cmd == "toggle":
                for y in range(y1, y2 + 1):
                    row[y] = not row[y]

    # Считаем, сколько лампочек включено
    total_on = sum(1 for x in range(size) for y in range(size) if grid[x][y])
    return str(total_on)


def solve_part2(data: str) -> str:
    # Здесь brightness (яркость) — целое число >= 0
    # "turn on"  -> brightness += 1
    # "turn off" -> brightness -= 1 (но не ниже 0)
    # "toggle"   -> brightness += 2
    size = 1000
    grid = [[0] * size for _ in range(size)]

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        parsed = parse_instruction(line)
        if parsed is None:
            continue

        cmd, x1, y1, x2, y2 = parsed

        for x in range(x1, x2 + 1):
            row = grid[x]
            if cmd == "on":
                for y in range(y1, y2 + 1):
                    row[y] += 1
            elif cmd == "off":
                for y in range(y1, y2 + 1):
                    if row[y] > 0:
                        row[y] -= 1
            elif cmd == "toggle":
                for y in range(y1, y2 + 1):
                    row[y] += 2

    total_brightness = sum(grid[x][y] for x in range(size) for y in range(size))
    return str(total_brightness)


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

