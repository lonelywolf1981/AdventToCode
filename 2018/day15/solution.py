from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import List, Tuple, Dict, Set, Optional


# Порядок соседей: вверх, влево, вправо, вниз (reading order)
# (dy, dx)
NEIGHBORS: List[Tuple[int, int]] = [(-1, 0), (0, -1), (0, 1), (1, 0)]


def parse_map(data: str, elf_attack_power: int = 3):
    """
    Разбор карты.
    Стены: '#', пусто: '.', юниты: 'E' / 'G'.

    Возвращает:
      grid  — сетка без юнитов ('.' / '#')
      units — список словарей: {type, x, y, hp, ap}
    """
    lines = [list(line.rstrip("\n")) for line in data.splitlines() if line.strip()]

    grid: List[List[str]] = [row[:] for row in lines]
    units: List[Dict] = []

    for y, row in enumerate(lines):
        for x, ch in enumerate(row):
            if ch in ("E", "G"):
                unit = {
                    "type": ch,      # 'E' или 'G'
                    "x": x,
                    "y": y,
                    "hp": 200,
                    "ap": elf_attack_power if ch == "E" else 3,
                }
                units.append(unit)
                grid[y][x] = "."  # на карте вместо юнита — пустая клетка

    return grid, units


def occupied_positions(units: List[Dict], exclude: Optional[Dict] = None) -> Set[Tuple[int, int]]:
    """Координаты всех живых юнитов, кроме exclude."""
    return {(u["x"], u["y"]) for u in units if u["hp"] > 0 and u is not exclude}


def get_adjacent_enemies(unit: Dict, units: List[Dict]) -> List[Dict]:
    """Возвращает список врагов в соседних клетках."""
    ux, uy = unit["x"], unit["y"]
    enemies: List[Dict] = []

    for dy, dx in NEIGHBORS:
        nx, ny = ux + dx, uy + dy
        for other in units:
            if other["hp"] <= 0:
                continue
            if other["type"] == unit["type"]:
                continue
            if other["x"] == nx and other["y"] == ny:
                enemies.append(other)

    return enemies


def choose_step(
    start: Tuple[int, int],
    in_range: Set[Tuple[int, int]],
    grid: List[List[str]],
    occupied: Set[Tuple[int, int]],
) -> Optional[Tuple[int, int]]:
    """
    BFS от позиции юнита до ближайших клеток in_range.
    Возвращает первую клетку пути (шаг), куда надо пойти, или None, если пути нет.
    """
    sx, sy = start
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    visited: Set[Tuple[int, int]] = set()
    parents: Dict[Tuple[int, int], Tuple[int, int]] = {}

    q: deque[Tuple[int, int, int]] = deque()
    q.append((sx, sy, 0))
    visited.add((sx, sy))

    found_targets: List[Tuple[int, int]] = []
    min_dist: Optional[int] = None

    while q:
        x, y, dist = q.popleft()

        if min_dist is not None and dist > min_dist:
            break

        if (x, y) in in_range and (x, y) != (sx, sy):
            min_dist = dist
            found_targets.append((x, y))
            continue

        for dy, dx in NEIGHBORS:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if grid[ny][nx] != ".":
                continue
            if (nx, ny) in occupied:
                continue
            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            parents[(nx, ny)] = (x, y)
            q.append((nx, ny, dist + 1))

    if not found_targets:
        return None

    # Выбираем цель с минимальными координатами (reading order: y, x)
    found_targets.sort(key=lambda p: (p[1], p[0]))
    tx, ty = found_targets[0]

    # Восстанавливаем путь назад, пока родитель не старт
    cur = (tx, ty)
    while parents.get(cur) != (sx, sy):
        cur = parents[cur]

    return cur


def simulate_battle(
    data: str,
    elf_attack_power: int = 3,
    stop_on_elf_death: bool = False,
):
    """
    Симуляция боя.

    Возвращает:
      rounds_completed — число полностью завершённых раундов
      total_hp         — сумма HP выживших
      elves_died       — сколько эльфов погибло
    """
    grid, units = parse_map(data, elf_attack_power=elf_attack_power)

    initial_elf_count = sum(1 for u in units if u["type"] == "E")
    rounds_completed = 0

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    while True:
        # Порядок хода — по чтению
        units.sort(key=lambda u: (u["y"], u["x"]))

        for unit in units:
            if unit["hp"] <= 0:
                continue  # мёртвые не ходят

            # Остались ли враги?
            enemies_alive = [u for u in units if u["hp"] > 0 and u["type"] != unit["type"]]
            if not enemies_alive:
                # Бой завершён посреди раунда — раунд не считается полным
                total_hp = sum(u["hp"] for u in units if u["hp"] > 0)
                elves_alive = sum(1 for u in units if u["type"] == "E" and u["hp"] > 0)
                elves_died = initial_elf_count - elves_alive
                return rounds_completed, total_hp, elves_died

            # 1) Проверяем врагов в соседних клетках
            adjacent_enemies = get_adjacent_enemies(unit, units)

            # 2) Если никого рядом — пытаемся двигаться
            if not adjacent_enemies:
                occupied = occupied_positions(units, exclude=unit)
                in_range: Set[Tuple[int, int]] = set()

                # Все пустые клетки, соседние с врагами
                for enemy in enemies_alive:
                    ex, ey = enemy["x"], enemy["y"]
                    for dy, dx in NEIGHBORS:
                        nx, ny = ex + dx, ey + dy
                        if not (0 <= nx < width and 0 <= ny < height):
                            continue
                        if grid[ny][nx] != ".":
                            continue
                        if (nx, ny) in occupied:
                            continue
                        in_range.add((nx, ny))

                if in_range:
                    step = choose_step((unit["x"], unit["y"]), in_range, grid, occupied)
                    if step is not None:
                        unit["x"], unit["y"] = step
                        # после движения пересчитываем соседей
                        adjacent_enemies = get_adjacent_enemies(unit, units)

            # 3) Атака, если есть враг рядом
            if adjacent_enemies:
                target = min(
                    adjacent_enemies,
                    key=lambda e: (e["hp"], e["y"], e["x"]),
                )
                target["hp"] -= unit["ap"]

                if target["hp"] <= 0 and stop_on_elf_death and target["type"] == "E":
                    # для Part 2 можем прервать симуляцию сразу при смерти эльфа
                    elves_died = 1
                    return rounds_completed, 0, elves_died

        # Раунд успешно завершён
        rounds_completed += 1


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    rounds, total_hp, _ = simulate_battle(data, elf_attack_power=3, stop_on_elf_death=False)
    outcome = rounds * total_hp
    return str(outcome)


def solve_part2(data: str) -> str:
    """
    Нужно найти минимальную силу атаки эльфов (>=4),
    при которой они выигрывают, и ни один эльф не погибает.
    """
    ap = 4
    while True:
        rounds, total_hp, elves_died = simulate_battle(
            data,
            elf_attack_power=ap,
            stop_on_elf_death=True,
        )
        if elves_died == 0:
            outcome = rounds * total_hp
            return str(outcome)
        ap += 1


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
