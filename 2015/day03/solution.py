def solve_part1(data: str) -> str:
    # Движения Санты по сетке, считаем уникальные дома с подарками
    moves = data.strip()
    x = y = 0
    visited = {(x, y)}  # стартовый дом

    for ch in moves:
        if ch == "^":
            y += 1
        elif ch == "v":
            y -= 1
        elif ch == ">":
            x += 1
        elif ch == "<":
            x -= 1
        # остальные символы игнорируем (если вдруг есть переводы строки и т.п.)
        visited.add((x, y))

    return str(len(visited))


def solve_part2(data: str) -> str:
    # Санта и Робо-Санта ходят по очереди
    moves = data.strip()

    # координаты Санты и Робо-Санты
    sx = sy = 0
    rx = ry = 0
    visited = {(0, 0)}  # стартовый дом

    for i, ch in enumerate(moves):
        # чётный ход — Санта, нечётный — Робо
        if i % 2 == 0:
            if ch == "^":
                sy += 1
            elif ch == "v":
                sy -= 1
            elif ch == ">":
                sx += 1
            elif ch == "<":
                sx -= 1
            visited.add((sx, sy))
        else:
            if ch == "^":
                ry += 1
            elif ch == "v":
                ry -= 1
            elif ch == ">":
                rx += 1
            elif ch == "<":
                rx -= 1
            visited.add((rx, ry))

    return str(len(visited))


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
