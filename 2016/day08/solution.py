# Advent of Code 2016 - Day 8
# Two-Factor Authentication
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> str
#
# В файле input.txt — строки вида:
# rect 3x2
# rotate column x=1 by 1
# rotate row y=0 by 4
# ...

from pathlib import Path
import re


WIDTH = 50
HEIGHT = 6


def _empty_screen():
    """Создаём пустой экран WIDTH x HEIGHT (False = пиксель выключен)."""
    return [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]


def _apply_rect(screen, a, b):
    """rect AxB — включаем прямоугольник шириной a, высотой b."""
    for y in range(b):
        for x in range(a):
            screen[y][x] = True


def _apply_rotate_row(screen, y, shift):
    """rotate row y=Y by N — сдвиг строки вправо на shift."""
    shift %= WIDTH
    row = screen[y]
    # циклический сдвиг вправо
    screen[y] = row[-shift:] + row[:-shift]


def _apply_rotate_column(screen, x, shift):
    """rotate column x=X by N — сдвиг колонки вниз на shift."""
    shift %= HEIGHT
    col = [screen[y][x] for y in range(HEIGHT)]
    col = col[-shift:] + col[:-shift]
    for y in range(HEIGHT):
        screen[y][x] = col[y]


def _parse_and_execute(screen, line: str):
    """Разбираем одну строку и применяем операцию к экрану."""
    line = line.strip()
    if not line:
        return

    if line.startswith("rect"):
        # rect AxB
        m = re.match(r"rect (\d+)x(\d+)", line)
        if not m:
            raise ValueError(f"Не могу разобрать rect: {line!r}")
        a, b = map(int, m.groups())
        _apply_rect(screen, a, b)
    elif line.startswith("rotate row"):
        # rotate row y=A by B
        m = re.match(r"rotate row y=(\d+) by (\d+)", line)
        if not m:
            raise ValueError(f"Не могу разобрать rotate row: {line!r}")
        y, shift = map(int, m.groups())
        _apply_rotate_row(screen, y, shift)
    elif line.startswith("rotate column"):
        # rotate column x=A by B
        m = re.match(r"rotate column x=(\d+) by (\d+)", line)
        if not m:
            raise ValueError(f"Не могу разобрать rotate column: {line!r}")
        x, shift = map(int, m.groups())
        _apply_rotate_column(screen, x, shift)
    else:
        raise ValueError(f"Неизвестная команда: {line!r}")


def _build_screen(data: str):
    """Применяет все команды и возвращает готовый экран (матрица bool)."""
    screen = _empty_screen()
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        _parse_and_execute(screen, line)
    return screen


def solve_part1(data: str) -> int:
    """
    Part 1:
    Вернуть количество включённых пикселей после выполнения всех команд.
    """
    screen = _build_screen(data)
    return sum(1 for row in screen for px in row if px)


def solve_part2(data: str) -> str:
    """
    Part 2:
    Вернуть строку, описывающую экран.
    Используем:
      '#' — включённый пиксель,
      ' ' (пробел) — выключенный пиксель.
    Строки разделены '\n'.
    Буквы нужно прочитать глазами.
    """
    screen = _build_screen(data)
    lines = []
    for row in screen:
        line = "".join("#" if px else " " for px in row)
        lines.append(line)
    return "\n".join(lines)


def main():
    # Локальный запуск: читаем input.txt из текущей папки
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:")
    print(part2)


if __name__ == "__main__":
    main()

