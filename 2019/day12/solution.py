from __future__ import annotations
from typing import List, Tuple
from math import gcd


# ------------------------------------------------------------
# Вспомогательные функции
# ------------------------------------------------------------

def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def parse_positions(data: str) -> List[Tuple[int, int, int]]:
    """
    Пример строки:
    <x=-1, y=0, z=2>
    Возвращаем список кортежей (x, y, z).
    """
    positions = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        # Удаляем < и >
        line = line.strip("<>")
        parts = line.split(",")
        d = {}
        for p in parts:
            k, v = p.strip().split("=")
            d[k] = int(v)
        positions.append((d["x"], d["y"], d["z"]))
    return positions


# ------------------------------------------------------------
# Симуляция для part1
# ------------------------------------------------------------

def simulate(positions: List[Tuple[int, int, int]], steps: int) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    """
    Симуляция движения для части 1.
    positions — список (x, y, z)
    Возвращаем (positions, velocities) после заданного числа шагов.
    """
    # Изначально скорости — нули
    velocities = [(0, 0, 0) for _ in positions]
    moons = len(positions)

    px = [p[0] for p in positions]
    py = [p[1] for p in positions]
    pz = [p[2] for p in positions]

    vx = [0] * moons
    vy = [0] * moons
    vz = [0] * moons

    for _ in range(steps):
        # 1) Гравитация
        for i in range(moons):
            for j in range(i + 1, moons):
                # X
                if px[i] < px[j]:
                    vx[i] += 1
                    vx[j] -= 1
                elif px[i] > px[j]:
                    vx[i] -= 1
                    vx[j] += 1
                # Y
                if py[i] < py[j]:
                    vy[i] += 1
                    vy[j] -= 1
                elif py[i] > py[j]:
                    vy[i] -= 1
                    vy[j] += 1
                # Z
                if pz[i] < pz[j]:
                    vz[i] += 1
                    vz[j] -= 1
                elif pz[i] > pz[j]:
                    vz[i] -= 1
                    vz[j] += 1

        # 2) Обновляем позиции
        for i in range(moons):
            px[i] += vx[i]
            py[i] += vy[i]
            pz[i] += vz[i]

    final_positions = list(zip(px, py, pz))
    final_velocities = list(zip(vx, vy, vz))
    return final_positions, final_velocities


def total_energy(positions: List[Tuple[int, int, int]], velocities: List[Tuple[int, int, int]]) -> int:
    total = 0
    for (x, y, z), (vx, vy, vz) in zip(positions, velocities):
        pot = abs(x) + abs(y) + abs(z)
        kin = abs(vx) + abs(vy) + abs(vz)
        total += pot * kin
    return total


# ------------------------------------------------------------
# Part 2 — поиск периода по одной оси
# ------------------------------------------------------------

def find_axis_period(initial_pos: List[int], initial_vel: List[int]) -> int:
    """
    Для одной оси ищем период полного возвращения к начальному состоянию.
    """
    px = initial_pos[:]
    vx = initial_vel[:]
    moons = len(px)
    step = 0

    while True:
        step += 1

        # гравитация
        for i in range(moons):
            for j in range(i + 1, moons):
                if px[i] < px[j]:
                    vx[i] += 1
                    vx[j] -= 1
                elif px[i] > px[j]:
                    vx[i] -= 1
                    vx[j] += 1

        # обновление позиций
        for i in range(moons):
            px[i] += vx[i]

        # проверяем возвращение в начало
        if all(px[i] == initial_pos[i] and vx[i] == initial_vel[i] for i in range(moons)):
            return step


# ------------------------------------------------------------
# Решения
# ------------------------------------------------------------

def solve_part1(data: str) -> str:
    positions = parse_positions(data)
    final_pos, final_vel = simulate(positions, steps=1000)
    return str(total_energy(final_pos, final_vel))


def solve_part2(data: str) -> str:
    positions = parse_positions(data)
    moons = len(positions)

    # позиции и скорости по осям
    px = [p[0] for p in positions]
    py = [p[1] for p in positions]
    pz = [p[2] for p in positions]

    vx = [0] * moons
    vy = [0] * moons
    vz = [0] * moons

    period_x = find_axis_period(px, vx)
    period_y = find_axis_period(py, vy)
    period_z = find_axis_period(pz, vz)

    return str(lcm(lcm(period_x, period_y), period_z))


# ------------------------------------------------------------
# Шаблон запуска
# ------------------------------------------------------------

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
