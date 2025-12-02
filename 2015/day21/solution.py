from itertools import combinations
from typing import Tuple


# Магазин из условия AoC 2015 Day 21

WEAPONS = [
    # (cost, damage, armor)
    (8, 4, 0),   # Dagger
    (10, 5, 0),  # Shortsword
    (25, 6, 0),  # Warhammer
    (40, 7, 0),  # Longsword
    (74, 8, 0),  # Greataxe
]

ARMORS = [
    (0, 0, 0),   # Нет брони
    (13, 0, 1),  # Leather
    (31, 0, 2),  # Chainmail
    (53, 0, 3),  # Splintmail
    (75, 0, 4),  # Bandedmail
    (102, 0, 5), # Platemail
]

RINGS = [
    (25, 1, 0),   # Damage +1
    (50, 2, 0),   # Damage +2
    (100, 3, 0),  # Damage +3
    (20, 0, 1),   # Defense +1
    (40, 0, 2),   # Defense +2
    (80, 0, 3),   # Defense +3
]


def parse_boss(data: str) -> Tuple[int, int, int]:
    boss_hp = boss_damage = boss_armor = 0
    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(":")
        key = parts[0].strip()
        val = int(parts[1].strip())
        if key == "Hit Points":
            boss_hp = val
        elif key == "Damage":
            boss_damage = val
        elif key == "Armor":
            boss_armor = val
    return boss_hp, boss_damage, boss_armor


def player_wins(player_damage: int, player_armor: int,
                boss_hp: int, boss_damage: int, boss_armor: int) -> bool:
    player_hp = 100

    # Урон за ход
    player_hit = max(1, player_damage - boss_armor)
    boss_hit = max(1, boss_damage - player_armor)

    # Сколько ходов до смерти
    turns_to_kill_boss = (boss_hp + player_hit - 1) // player_hit
    turns_to_kill_player = (player_hp + boss_hit - 1) // boss_hit

    # Игрок ходит первым, выигрывает, если убивает не позже, чем его убьют
    return turns_to_kill_boss <= turns_to_kill_player


def all_loadouts():
    """
    Генерирует все варианты снаряжения:
    - 1 оружие
    - 0 или 1 броня
    - 0, 1 или 2 кольца
    Возвращает (cost, damage, armor)
    """
    # Ровно одно оружие
    for w_cost, w_dmg, w_arm in WEAPONS:
        # 0 или 1 броня
        for a_cost, a_dmg, a_arm in ARMORS:
            # 0 колец
            yield (w_cost + a_cost,
                   w_dmg + a_dmg,
                   w_arm + a_arm)

            # 1 кольцо
            for (r1_cost, r1_dmg, r1_arm) in RINGS:
                yield (w_cost + a_cost + r1_cost,
                       w_dmg + a_dmg + r1_dmg,
                       w_arm + a_arm + r1_arm)

            # 2 кольца
            for (r1_cost, r1_dmg, r1_arm), (r2_cost, r2_dmg, r2_arm) in combinations(RINGS, 2):
                yield (w_cost + a_cost + r1_cost + r2_cost,
                       w_dmg + a_dmg + r1_dmg + r2_dmg,
                       w_arm + a_arm + r1_arm + r2_arm)


def solve_part1(data: str) -> str:
    boss_hp, boss_damage, boss_armor = parse_boss(data)

    best_cost = float("inf")

    for cost, dmg, arm in all_loadouts():
        if player_wins(dmg, arm, boss_hp, boss_damage, boss_armor):
            if cost < best_cost:
                best_cost = cost

    return str(best_cost)


def solve_part2(data: str) -> str:
    boss_hp, boss_damage, boss_armor = parse_boss(data)

    worst_cost = 0

    for cost, dmg, arm in all_loadouts():
        if not player_wins(dmg, arm, boss_hp, boss_damage, boss_armor):
            if cost > worst_cost:
                worst_cost = cost

    return str(worst_cost)


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
