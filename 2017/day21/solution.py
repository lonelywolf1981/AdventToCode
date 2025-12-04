from pathlib import Path
from typing import Dict, List, Tuple, Iterable, Set


Pattern = Tuple[str, ...]  # кортеж строк, например (".#.", "..#", "###")


def _parse_pattern(s: str) -> Pattern:
    """
    " .#./..#/### " -> (".#.", "..#", "###")
    """
    s = s.strip()
    return tuple(part for part in s.split("/"))


def _rotate(p: Pattern) -> Pattern:
    """
    Поворот узора по часовой стрелке на 90 градусов.
    """
    n = len(p)
    # new[i][j] = old[n-1-j][i]
    return tuple("".join(p[n - 1 - j][i] for j in range(n)) for i in range(n))


def _flip_h(p: Pattern) -> Pattern:
    """
    Отражение по горизонтали (зеркало слева-направо).
    """
    return tuple(row[::-1] for row in p)


def _variations(p: Pattern) -> List[Pattern]:
    """
    Все симметрии узора: 4 поворота * (без отражения / с отражением).
    Итого до 8 вариантов, но можем дедуплицировать через set.
    """
    res: Set[Pattern] = set()
    cur = p
    for _ in range(4):
        res.add(cur)
        res.add(_flip_h(cur))
        cur = _rotate(cur)
    return list(res)


def _parse_rules(data: str) -> Dict[Pattern, Pattern]:
    """
    Парсим строки вида:
      ../.# => ##./#../...
      .#./..#/### => #..#/..../..../#..#
    Возвращаем словарь:
      вариант_входного_узора (с учётом всех поворотов/отражений) -> выходной_узор
    """
    rules: Dict[Pattern, Pattern] = {}

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        left, right = line.split("=>")
        in_pat = _parse_pattern(left)
        out_pat = _parse_pattern(right)

        for var in _variations(in_pat):
            rules[var] = out_pat

    if not rules:
        raise ValueError("Пустой или некорректный input для Day 21")

    return rules


def _enhance(grid: Pattern, rules: Dict[Pattern, Pattern]) -> Pattern:
    """
    Один шаг улучшения:
    - режем картинку на блоки 2x2 или 3x3,
    - каждый блок заменяем по правилу,
    - собираем новую большую картинку.
    """
    size = len(grid)
    if size % 2 == 0:
        block_size = 2
        new_block_size = 3
    elif size % 3 == 0:
        block_size = 3
        new_block_size = 4
    else:
        raise ValueError(f"Размер рисунка {size} не делится ни на 2, ни на 3")

    blocks_per_side = size // block_size
    new_size = blocks_per_side * new_block_size

    # Готовим пустую сетку для нового рисунка
    new_grid: List[List[str]] = [["." for _ in range(new_size)] for _ in range(new_size)]

    for by in range(blocks_per_side):          # индекс блока по вертикали
        for bx in range(blocks_per_side):      # индекс блока по горизонтали
            # Вырезаем блок block_size x block_size
            sub: Pattern = tuple(
                grid[by * block_size + r][bx * block_size : bx * block_size + block_size]
                for r in range(block_size)
            )

            # Находим соответствующее правило (с учётом симметрий)
            out = rules.get(sub)
            if out is None:
                # На всякий случай: попробуем поискать по вариациям здесь,
                # если вдруг не занесли при парсинге (но не должно быть так).
                for var in _variations(sub):
                    if var in rules:
                        out = rules[var]
                        break
            if out is None:
                raise KeyError(f"Не найдено правило для блока: {sub}")

            # Записываем out (new_block_size x new_block_size) в нужное место
            for r in range(new_block_size):
                for c in range(new_block_size):
                    new_grid[by * new_block_size + r][bx * new_block_size + c] = out[r][c]

    # Превращаем список списков в кортеж строк
    return tuple("".join(row) for row in new_grid)


def _iterate(grid: Pattern, rules: Dict[Pattern, Pattern], steps: int) -> Pattern:
    """
    Применяем _enhance 'steps' раз подряд.
    """
    cur = grid
    for _ in range(steps):
        cur = _enhance(cur, rules)
    return cur


def _count_on(grid: Pattern) -> int:
    """
    Подсчитать количество '#' в рисунке.
    """
    return sum(row.count("#") for row in grid)


def solve_part1(data: str) -> int:
    """
    Day 21, Part 1:
    Стартуем с ".#./..#/###", делаем 5 итераций, считаем '#'.
    """
    rules = _parse_rules(data)
    start: Pattern = (".#.", "..#", "###")
    final = _iterate(start, rules, steps=5)
    return _count_on(final)


def solve_part2(data: str) -> int:
    """
    Day 21, Part 2:
    Тот же процесс, но 18 итераций.
    """
    rules = _parse_rules(data)
    start: Pattern = (".#.", "..#", "###")
    final = _iterate(start, rules, steps=18)
    return _count_on(final)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
