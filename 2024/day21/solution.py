from __future__ import annotations

from collections import deque
from functools import lru_cache
from typing import Dict, List, Tuple


# ---------- Описание клавиатур ----------

# Числовая клавиатура (как в условии):
# 7 8 9
# 4 5 6
# 1 2 3
#   0 A
NUMERIC_GRID = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"],  # пробел = запрещённая ячейка
]

# Направляющая клавиатура:
#   ^ A
# < v >
DIR_GRID = [
    [" ", "^", "A"],
    ["<", "v", ">"],
]


def build_paths(grid: List[List[str]]) -> Dict[Tuple[str, str], List[str]]:
    """
    Для данной клавиатуры строим словарь:
        (start_key, end_key) -> список всех кратчайших последовательностей
        движений ('^', 'v', '<', '>') от start_key к end_key.

    ВНИМАНИЕ: здесь БЕЗ финального 'A'. Его мы добавляем на уровне рекурсии.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Координаты каждой кнопки (кроме пустых)
    positions: Dict[str, Tuple[int, int]] = {}
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch != " ":
                positions[ch] = (r, c)

    # Возможные смещения и символы направлений
    moves = {
        (0, 1): ">",
        (0, -1): "<",
        (1, 0): "v",
        (-1, 0): "^",
    }

    # Итог: для каждой пары (s, t) список кратчайших путей
    paths: Dict[Tuple[str, str], List[str]] = {}

    # Сразу добавим случай "остаться на месте": путь пустой строкой
    for s in positions:
        for t in positions:
            if s == t:
                paths[(s, t)] = [""]
            else:
                paths[(s, t)] = []

    # Для каждой стартовой кнопки делаем BFS по клеткам
    for s, (sr, sc) in positions.items():
        dist: Dict[Tuple[int, int], int] = {(sr, sc): 0}
        # для каждой клетки храним ВСЕ кратчайшие пути из s в неё
        paths_at: Dict[Tuple[int, int], List[str]] = {(sr, sc): [""]}

        q = deque([(sr, sc)])
        while q:
            r, c = q.popleft()
            d = dist[(r, c)]
            for (dr, dc), dir_char in moves.items():
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                if grid[nr][nc] == " ":
                    continue

                np = (nr, nc)
                nd = d + 1
                if np not in dist:
                    # Первый раз дошли до этой клетки: фиксируем дистанцию и пути
                    dist[np] = nd
                    paths_at[np] = [p + dir_char for p in paths_at[(r, c)]]
                    q.append(np)
                elif nd == dist[np]:
                    # Ещё один кратчайший путь до той же клетки
                    new_paths = [p + dir_char for p in paths_at[(r, c)]]
                    paths_at[np].extend(new_paths)

        # Переносим в общий словарь пути s -> t
        for t, (tr, tc) in positions.items():
            if t == s:
                # уже [""]
                continue
            pos_t = (tr, tc)
            if pos_t in paths_at:
                paths[(s, t)] = paths_at[pos_t]
            # иначе кнопка недостижима, но в этой задаче такого нет

    return paths


# Предрасчёт всех кратчайших путей по двум клавиатурам
NUMERIC_PATHS = build_paths(NUMERIC_GRID)
DIR_PATHS = build_paths(DIR_GRID)


def compute_total_complexity(codes: List[str], num_bots: int) -> int:
    """
    Считает суммарную сложность списка кодов
    при заданном числе промежуточных роботов на направляющих клавиатурах.
    num_bots:
        - 2  для Part 1
        - 25 для Part 2
    """

    @lru_cache(maxsize=None)
    def min_presses(level: int, text: str) -> int:
        """
        Возвращает минимальное количество нажатий на САМЫЙ верхний пульт,
        чтобы на уровне `level` робот набрал строку `text` на своей клавиатуре.

        level = 0  -> робот на числовой клавиатуре
        1..num_bots -> роботы на направляющих клавиатурах
        level = num_bots + 1 -> мы сами нажимаем стрелки и 'A' напрямую
        """
        # База: дальше роботов нет — просто нажимаем эту строку напрямую
        if level == num_bots + 1:
            return len(text)

        # Для level=0 — используем NUMERIC_PATHS, иначе DIR_PATHS
        paths_map = NUMERIC_PATHS if level == 0 else DIR_PATHS

        total = 0
        prev = "A"  # курсор всегда стартует на 'A' на каждом уровне

        # Для каждой следующей целевой кнопки считаем минимальный путь
        for ch in text:
            options = paths_map[(prev, ch)]  # все кратчайшие варианты движения
            # Для каждого варианта пути: двигаемся по стрелкам + жмём 'A'
            # То есть на уровень ниже нужно передать (path + 'A').
            costs = [min_presses(level + 1, path + "A") for path in options]
            total += min(costs)
            prev = ch

        return total

    total_sum = 0
    for code in codes:
        # Выделяем числовую часть (игнорируя 'A')
        numeric_part_str = "".join(ch for ch in code if ch.isdigit())
        if not numeric_part_str:
            continue
        numeric_part = int(numeric_part_str)

        # Минимальное количество нажатий на верхнем уровне
        presses = min_presses(0, code)
        total_sum += numeric_part * presses

    return total_sum


def solve_part1(data: str) -> str:
    """
    Part 1: два промежуточных робота на направляющих клавиатурах.
    """
    codes = [line.strip() for line in data.splitlines() if line.strip()]
    if not codes:
        return "0"
    ans = compute_total_complexity(codes, num_bots=2)
    return str(ans)


def solve_part2(data: str) -> str:
    """
    Part 2: 25 промежуточных роботов на направляющих клавиатурах.
    """
    codes = [line.strip() for line in data.splitlines() if line.strip()]
    if not codes:
        return "0"
    ans = compute_total_complexity(codes, num_bots=25)
    return str(ans)


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
