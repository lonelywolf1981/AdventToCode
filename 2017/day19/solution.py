from pathlib import Path
from typing import List, Tuple


def _parse_grid(data: str) -> List[List[str]]:
    """
    Преобразует текст карты в прямоугольную сетку символов.
    Короткие строки дополняются пробелами справа.
    """
    lines = data.splitlines()
    if not lines:
        raise ValueError("Пустой input для Day 19")

    max_len = max(len(line) for line in lines)
    grid: List[List[str]] = []
    for line in lines:
        # дополняем до max_len пробелами, чтобы индексация была ровной
        padded = line.ljust(max_len, " ")
        grid.append(list(padded))
    return grid


def _walk_tubes(grid: List[List[str]]) -> Tuple[str, int]:
    """
    Общая симуляция маршрута.
    Возвращает:
      (letters, steps)
    letters — собранные буквы по пути.
    steps   — количество шагов до выхода.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Находим стартовую колонку в первой строке (символ '|')
    top_row = grid[0]
    try:
        col = top_row.index("|")
    except ValueError:
        raise ValueError("Не найден стартовый символ '|' в первой строке")

    row = 0
    # первоначальное направление — вниз
    dr, dc = 1, 0

    letters: List[str] = []
    steps = 0

    # Идём, пока не выйдем за карту или не врежемся в пробел
    while True:
        # Текущий символ
        ch = grid[row][col]

        # Если буква — запоминаем
        if ch.isalpha():
            letters.append(ch)

        if ch == "+":
            # Нужно повернуть: ищем новое направление
            # Если шли вертикально -> пробуем влево/вправо
            if dr != 0:  # шли вверх или вниз
                # влево
                if col - 1 >= 0 and grid[row][col - 1] != " ":
                    dr, dc = 0, -1
                # вправо
                elif col + 1 < cols and grid[row][col + 1] != " ":
                    dr, dc = 0, 1
                else:
                    # повернуть некуда — конец
                    break
            else:  # шли горизонтально
                # вверх
                if row - 1 >= 0 and grid[row - 1][col] != " ":
                    dr, dc = -1, 0
                # вниз
                elif row + 1 < rows and grid[row + 1][col] != " ":
                    dr, dc = 1, 0
                else:
                    break

        # Двигаемся к следующей клетке
        row += dr
        col += dc
        steps += 1

        # Проверяем выход за границы или попадание в пустоту
        if not (0 <= row < rows and 0 <= col < cols):
            break
        if grid[row][col] == " ":
            break

    return "".join(letters), steps


def solve_part1(data: str) -> str:
    """
    Day 19, Part 1:
    Возвращаем строку из всех букв, собранных по пути.
    """
    grid = _parse_grid(data)
    letters, _ = _walk_tubes(grid)
    return letters


def solve_part2(data: str) -> int:
    """
    Day 19, Part 2:
    Возвращаем количество шагов по маршруту до выхода.
    """
    grid = _parse_grid(data)
    _, steps = _walk_tubes(grid)
    return steps


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
