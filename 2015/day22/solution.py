from dataclasses import dataclass, replace
from typing import Optional


# Заклинания (Mana cost)
SPELL_MAGIC_MISSILE = 53     # 4 damage instantly
SPELL_DRAIN = 73             # 2 damage + 2 heal instantly
SPELL_SHIELD = 113           # +7 armor for 6 turns
SPELL_POISON = 173           # 3 damage per turn for 6 turns
SPELL_RECHARGE = 229         # +101 mana per turn for 5 turns


@dataclass
class State:
    player_hp: int
    player_mana: int
    player_armor: int
    boss_hp: int
    boss_damage: int
    mana_spent: int

    # длительные эффекты (количество оставшихся ходов)
    shield_timer: int = 0
    poison_timer: int = 0
    recharge_timer: int = 0


def apply_effects(s: State) -> State:
    """Применяем все текущие длительные эффекты к состоянию."""
    armor = 0
    if s.shield_timer > 0:
        armor = 7
        s = replace(s, shield_timer=s.shield_timer - 1)
    else:
        armor = 0

    boss_hp = s.boss_hp
    if s.poison_timer > 0:
        boss_hp -= 3
        s = replace(s, poison_timer=s.poison_timer - 1)

    mana = s.player_mana
    if s.recharge_timer > 0:
        mana += 101
        s = replace(s, recharge_timer=s.recharge_timer - 1)

    return replace(s, boss_hp=boss_hp, player_armor=armor, player_mana=mana)


def can_cast(s: State, spell: int) -> bool:
    """Проверяет, может ли маг кастовать заклинание в текущем состоянии."""
    if s.player_mana < spell:
        return False
    if spell == SPELL_SHIELD and s.shield_timer > 0:
        return False
    if spell == SPELL_POISON and s.poison_timer > 0:
        return False
    if spell == SPELL_RECHARGE and s.recharge_timer > 0:
        return False
    return True


def cast_spell(s: State, spell: int) -> State:
    """Применить заклинание — обновить состояние."""
    new_s = replace(s, player_mana=s.player_mana - spell, mana_spent=s.mana_spent + spell)

    if spell == SPELL_MAGIC_MISSILE:
        return replace(new_s, boss_hp=new_s.boss_hp - 4)

    elif spell == SPELL_DRAIN:
        return replace(new_s, boss_hp=new_s.boss_hp - 2, player_hp=new_s.player_hp + 2)

    elif spell == SPELL_SHIELD:
        return replace(new_s, shield_timer=6)

    elif spell == SPELL_POISON:
        return replace(new_s, poison_timer=6)

    elif spell == SPELL_RECHARGE:
        return replace(new_s, recharge_timer=5)

    raise ValueError("Unknown spell")


best_mana = float("inf")


def search(s: State, hard_mode: bool):
    global best_mana

    # 1) HARD MODE – теряем HP в начале ХОДА ИГРОКА
    if hard_mode:
        s = replace(s, player_hp=s.player_hp - 1)
        if s.player_hp <= 0:
            return

    # 2) Применяем эффекты в начале хода игрока
    s = apply_effects(s)
    if s.boss_hp <= 0:  # умер от яда
        best_mana = min(best_mana, s.mana_spent)
        return

    # Если уже потратили больше маны, чем текущее лучшее решение — отсечь
    if s.mana_spent >= best_mana:
        return

    # 3) Перебор всех возможных заклинаний
    for spell in (SPELL_MAGIC_MISSILE, SPELL_DRAIN, SPELL_SHIELD, SPELL_POISON, SPELL_RECHARGE):

        if not can_cast(s, spell):
            continue

        # Игрок кастует заклинание
        ps = cast_spell(s, spell)

        # Если после кастования босс умер — победа
        if ps.boss_hp <= 0:
            best_mana = min(best_mana, ps.mana_spent)
            continue

        # ---- ХОД БОССА ----

        # Применяем эффекты в начале хода босса
        bs = apply_effects(ps)
        if bs.boss_hp <= 0:
            best_mana = min(best_mana, bs.mana_spent)
            continue

        # Босс бьёт
        dmg = max(1, bs.boss_damage - bs.player_armor)
        bs = replace(bs, player_hp=bs.player_hp - dmg)
        if bs.player_hp <= 0:
            continue

        # Рекурсивный вызов
        search(bs, hard_mode)


def solve_part1(data: str) -> str:
    global best_mana
    boss_hp, boss_dmg = 0, 0

    for line in data.strip().splitlines():
        key, val = line.split(":")
        key = key.strip()
        val = int(val.strip())
        if key == "Hit Points":
            boss_hp = val
        elif key == "Damage":
            boss_dmg = val

    start = State(
        player_hp=50,
        player_mana=500,
        player_armor=0,
        boss_hp=boss_hp,
        boss_damage=boss_dmg,
        mana_spent=0,
    )

    best_mana = float("inf")
    search(start, hard_mode=False)
    return str(best_mana)


def solve_part2(data: str) -> str:
    global best_mana
    boss_hp, boss_dmg = 0, 0

    for line in data.strip().splitlines():
        key, val = line.split(":")
        key = key.strip()
        val = int(val.strip())
        if key == "Hit Points":
            boss_hp = val
        elif key == "Damage":
            boss_dmg = val

    start = State(
        player_hp=50,
        player_mana=500,
        player_armor=0,
        boss_hp=boss_hp,
        boss_damage=boss_dmg,
        mana_spent=0,
    )

    best_mana = float("inf")
    search(start, hard_mode=True)
    return str(best_mana)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
