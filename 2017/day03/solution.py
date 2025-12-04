from pathlib import Path


def _parse_input(data: str) -> int:
    """
    Вход у Day 3 — одно число (может быть с переводом строки).
    """
    data = data.strip()
    if not data:
        raise ValueError("Пустой input для Day 3")
    return int(data)


def solve_part1(data: str) -> int:
    """
    Day 3, Part 1:
    Манхэттенское расстояние от числа n до 1 в спирали.
    Математическое решение без явного построения всей спирали.
    """
    n = _parse_input(data)
    if n == 1:
        return 0

    # Определяем "кольцо" спирали.
    # Кольцо k имеет максимальное значение (2k+1)^2.
    # k = 0 -> только 1
    # k = 1 -> числа до 9, k = 2 -> до 25, и т.д.
    import math

    k = math.ceil((math.sqrt(n) - 1) / 2)
    side_len = 2 * k
    max_val = (2 * k + 1) ** 2

    # Центры сторон квадрата на этом кольце:
    # max_val - k, max_val - 3k, max_val - 5k, max_val - 7k
    # расстояние до ближайшего центра стороны по оси = min(|n - center|).
    centers = [max_val - k - side_len * i for i in range(4)]
    min_offset = min(abs(n - c) for c in centers)

    # Манхэттенское расстояние = "радиус кольца" + смещение до центра стороны
    return k + min_offset


def solve_part2(data: str) -> int:
    """
    Day 3, Part 2:
    Строим спираль, где значение каждой клетки — сумма соседей,
    и ищем первое значение, строго большее n.
    """
    target = _parse_input(data)

    # Координаты -> значение в ячейке
    grid: dict[tuple[int, int], int] = {}
    x = y = 0
    grid[(0, 0)] = 1

    # Направления для спирали: вправо, вверх, влево, вниз
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # Паттерн шагов: 1 вправо, 1 вверх, 2 влево, 2 вниз, 3 вправо, 3 вверх, ...
    step_size = 1
    dir_index = 0

    def neighbor_sum(cx: int, cy: int) -> int:
        s = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                s += grid.get((cx + dx, cy + dy), 0)
        return s

    while True:
        for _ in range(2):  # два раза по step_size: по двум направлениям
            dx, dy = directions[dir_index]
            for _ in range(step_size):
                x += dx
                y += dy
                val = neighbor_sum(x, y)
                grid[(x, y)] = val
                if val > target:
                    return val
            dir_index = (dir_index + 1) % 4
        step_size += 1


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
