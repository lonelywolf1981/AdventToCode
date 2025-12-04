from pathlib import Path
from typing import List, Tuple, Dict
import re


# ---- Парсинг ----

def _parse_vec(s: str) -> Tuple[int, int, int]:
    # p=<1,2,3>, v=<-4,5,6> etc.
    nums = list(map(int, s[s.index("<") + 1 : s.index(">")].split(",")))
    return nums[0], nums[1], nums[2]


def _parse_input(data: str):
    """
    Возвращает список частиц:
    [
        {
            "p": [x,y,z],
            "v": [x,y,z],
            "a": [x,y,z],
        },
        ...
    ]
    """
    particles = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        # Извлекаем p=<...>, v=<...>, a=<...>
        parts = line.split(", ")
        p = _parse_vec(parts[0])
        v = _parse_vec(parts[1])
        a = _parse_vec(parts[2])

        particles.append({
            "p": [p[0], p[1], p[2]],
            "v": [v[0], v[1], v[2]],
            "a": [a[0], a[1], a[2]],
        })

    if not particles:
        raise ValueError("Пустой input для Day 20")

    return particles


# ---- Part 1 ----

def solve_part1(data: str) -> int:
    """
    Частица, которая останется ближе всех к (0,0,0) в долгосрочной перспективе.
    Алгоритм:
    1) выбираем с минимальной манхэттенской нормой ускорения
    2) при равенстве — с минимальной нормой скорости
    3) при равенстве — с минимальной нормой позиции
    """
    particles = _parse_input(data)

    def manhattan(t):
        return abs(t[0]) + abs(t[1]) + abs(t[2])

    best = None
    best_index = None

    for i, part in enumerate(particles):
        a = part["a"]
        v = part["v"]
        p = part["p"]

        accel = manhattan(a)
        vel = manhattan(v)
        pos = manhattan(p)

        key = (accel, vel, pos)

        if best is None or key < best:
            best = key
            best_index = i

    return best_index  # индекс частицы


# ---- Part 2 ----

def solve_part2(data: str) -> int:
    """
    Симулируем частиц, удаляя столкнувшиеся.
    Цикл повторяем, пока количество частиц стабильно.
    Практически хватает ~1000 итераций.
    """
    parts = _parse_input(data)

    # Превратим в список словарей, с которым удобно работать
    particles = [
        {
            "p": part["p"][:],
            "v": part["v"][:],
            "a": part["a"][:],
        }
        for part in parts
    ]

    stable_rounds = 0
    last_count = len(particles)

    for _ in range(2000):  # запас, AoC обычно сходится раньше
        positions: Dict[Tuple[int, int, int], List[int]] = {}

        # 1. Обновляем все частицы
        for idx, part in enumerate(particles):
            # v += a
            part["v"][0] += part["a"][0]
            part["v"][1] += part["a"][1]
            part["v"][2] += part["a"][2]

            # p += v
            part["p"][0] += part["v"][0]
            part["p"][1] += part["v"][1]
            part["p"][2] += part["v"][2]

            pos = tuple(part["p"])
            positions.setdefault(pos, []).append(idx)

        # 2. Удаляем столкнувшиеся
        survivors = []
        for idx, part in enumerate(particles):
            pos = tuple(part["p"])
            if len(positions[pos]) == 1:  # никто не столкнулся
                survivors.append(part)

        particles = survivors

        # 3. Проверяем стабилизацию
        if len(particles) == last_count:
            stable_rounds += 1
            if stable_rounds >= 50:  # 50 итераций без изменений -> стабильно
                break
        else:
            stable_rounds = 0
            last_count = len(particles)

    return len(particles)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
