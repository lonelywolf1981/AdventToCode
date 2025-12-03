# Advent of Code 2016 - Day 2
# Bathroom Security
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> str
#   solve_part2(raw_input: str) -> str
#
# В файле input.txt — несколько строк с символами UDLR.

from pathlib import Path


def _parse_lines(data: str):
    """
    Разбивает вход на непустые строки.
    """
    return [line.strip() for line in data.splitlines() if line.strip()]


def solve_part1(data: str) -> str:
    """
    Part 1: обычная клавиатура 3x3.
    Возвращает код в виде строки, например '1985'.
    """
    lines = _parse_lines(data)

    # координаты: (x, y) — x по горизонтали, y по вертикали
    # пусть (0,0) — верхний левый угол, (2,2) — нижний правый
    keypad = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]

    # стартуем с кнопки '5' -> координаты (1,1)
    x, y = 1, 1

    code = []

    for line in lines:
        for ch in line:
            if ch == "U":
                y = max(0, y - 1)
            elif ch == "D":
                y = min(2, y + 1)
            elif ch == "L":
                x = max(0, x - 1)
            elif ch == "R":
                x = min(2, x + 1)
            else:
                # игнорируем любые левые символы
                continue

        code.append(keypad[y][x])

    return "".join(code)


def solve_part2(data: str) -> str:
    """
    Part 2: ромбовидная клавиатура.
    Возвращает код в виде строки, например '5DB3'.
    """
    lines = _parse_lines(data)

    # Опишем клавиатуру как словарь: (x,y) -> символ
    # С координатной сеткой, где некоторые клетки пустые.
    keypad = {
        (2, 0): "1",
        (1, 1): "2", (2, 1): "3", (3, 1): "4",
        (0, 2): "5", (1, 2): "6", (2, 2): "7", (3, 2): "8", (4, 2): "9",
        (1, 3): "A", (2, 3): "B", (3, 3): "C",
        (2, 4): "D",
    }

    # Стартовая позиция — '5' -> (0,2)
    x, y = 0, 2
    code = []

    moves = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    for line in lines:
        for ch in line:
            if ch not in moves:
                continue

            dx, dy = moves[ch]
            nx, ny = x + dx, y + dy

            # Двигаемся только если новая позиция существует на клавиатуре
            if (nx, ny) in keypad:
                x, y = nx, ny

        code.append(keypad[(x, y)])

    return "".join(code)


def main():
    # Локальный запуск: читаем input.txt из текущей папки
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()

