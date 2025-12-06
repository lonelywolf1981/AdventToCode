from pathlib import Path
from typing import List, Tuple

# Тип тележки: [x, y, dx, dy, turn_state, alive]
# turn_state: 0 = налево, 1 = прямо, 2 = направо
Cart = List[int]


def parse_input(data: str):
    """
    Читаем карту.
    Возвращаем:
      grid — сетка рельсов (без тележек)
      carts — список тележек
    """
    lines = data.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines) if lines else 0

    grid = [list(line.ljust(width)) for line in lines]
    carts: List[Cart] = []

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch in "<>^v":
                if ch == "<":
                    dx, dy = -1, 0
                    under = "-"
                elif ch == ">":
                    dx, dy = 1, 0
                    under = "-"
                elif ch == "^":
                    dx, dy = 0, -1
                    under = "|"
                else:  # "v"
                    dx, dy = 0, 1
                    under = "|"

                carts.append([x, y, dx, dy, 0, 1])  # x,y,dx,dy,turn_state,alive
                grid[y][x] = under

    return grid, carts


def turn_left(dx: int, dy: int) -> Tuple[int, int]:
    # (dx, dy) -> налево
    return dy, -dx


def turn_right(dx: int, dy: int) -> Tuple[int, int]:
    # (dx, dy) -> направо
    return -dy, dx


def move_cart(cart: Cart, grid) -> None:
    """
    Двигаем одну тележку на 1 шаг и обновляем её направление по типу рельса.
    """
    x, y, dx, dy, turn_state, alive = cart

    x += dx
    y += dy
    cart[0], cart[1] = x, y

    track = grid[y][x]

    if track == "/":
        # / меняет направление:
        if dx == 0:  # шли вверх/вниз
            dx, dy = turn_right(dx, dy)
        else:        # шли влево/вправо
            dx, dy = turn_left(dx, dy)

    elif track == "\\":
        # \ меняет направление:
        if dx == 0:  # вверх/вниз
            dx, dy = turn_left(dx, dy)
        else:        # влево/вправо
            dx, dy = turn_right(dx, dy)

    elif track == "+":
        # перекрёсток: налево -> прямо -> направо
        if turn_state == 0:      # налево
            dx, dy = turn_left(dx, dy)
        elif turn_state == 2:    # направо
            dx, dy = turn_right(dx, dy)
        # turn_state == 1 — прямо, ничего не меняем

        turn_state = (turn_state + 1) % 3

    cart[2], cart[3] = dx, dy
    cart[4] = turn_state


def solve_part1(data: str) -> str:
    grid, carts = parse_input(data)

    while True:
        # тележки обрабатываются в порядке "чтения": сверху-вниз, слева-направо
        carts.sort(key=lambda c: (c[1], c[0]))

        # множество занятых позиций (только живые)
        positions = {(c[0], c[1]) for c in carts if c[5] == 1}

        for cart in carts:
            if cart[5] == 0:
                continue

            # старая позиция больше не занята (тележка двинулась)
            positions.discard((cart[0], cart[1]))

            move_cart(cart, grid)
            new_pos = (cart[0], cart[1])

            # если сюда уже кто-то врезался или стоит — это первое столкновение
            if new_pos in positions:
                return f"{new_pos[0]},{new_pos[1]}"

            positions.add(new_pos)


def solve_part2(data: str) -> str:
    grid, carts = parse_input(data)

    # Будем симулировать до тех пор, пока не останется одна живая тележка
    while True:
        # читаем по порядку: сверху-вниз, слева-направо
        carts.sort(key=lambda c: (c[1], c[0]))

        for i, cart in enumerate(carts):
            if cart[5] == 0:
                continue  # уже разбилась

            # двигаем тележку
            move_cart(cart, grid)
            x, y = cart[0], cart[1]

            # ищем столкновение с любой другой живой тележкой
            for j, other in enumerate(carts):
                if j == i or other[5] == 0:
                    continue
                if other[0] == x and other[1] == y:
                    # столкновение — обе тележки уничтожаются
                    cart[5] = 0
                    other[5] = 0
                    break  # текущая тележка уже "мертва", дальше её не двигаем

        # собираем живых
        alive_carts = [c for c in carts if c[5] == 1]

        if len(alive_carts) == 1:
            x, y = alive_carts[0][0], alive_carts[0][1]
            return f"{x},{y}"
        elif len(alive_carts) == 0:
            # На всякий случай, если вдруг все разбились (на реальном AoC-входе такого нет)
            return "0,0"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
