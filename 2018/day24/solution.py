from pathlib import Path


class Group:
    def __init__(self, side, units, hp, immunities, weaknesses, attk_type, attk_damage, initiative):
        self.side = side
        self.units = units
        self.hp = hp
        self.immunities = list(immunities)
        self.weaknesses = list(weaknesses)
        self.attk_type = attk_type
        self.attk_damage = attk_damage
        self.initiative = initiative
        self.target = None

    def __repr__(self):
        return f"{self.side}({self.units} units, {self.effective_power()} power, {self.hp} hp)"

    def __copy__(self):
        # Глубоко копировать списки иммунитетов/уязвимостей не критично, они неизменяемые
        return Group(
            self.side,
            self.units,
            self.hp,
            list(self.immunities),
            list(self.weaknesses),
            self.attk_type,
            self.attk_damage,
            self.initiative,
        )

    def __eq__(self, other):
        if other is None:
            return False
        return (
            self.side == other.side and
            self.units == other.units and
            self.hp == other.hp and
            self.immunities == other.immunities and
            self.weaknesses == other.weaknesses and
            self.attk_type == other.attk_type and
            self.attk_damage == other.attk_damage and
            self.initiative == other.initiative
        )

    def __hash__(self):
        # чтобы использовать в set / dict как в исходном коде
        return id(self)

    def boosted_copy(self, boost):
        return Group(
            self.side,
            self.units,
            self.hp,
            self.immunities,
            self.weaknesses,
            self.attk_type,
            self.attk_damage + boost,
            self.initiative,
        )

    def effective_power(self):
        return self.units * self.attk_damage

    def simulate_damage(self, other):
        if self.attk_type in other.immunities:
            multiplier = 0
        elif self.attk_type in other.weaknesses:
            multiplier = 2
        else:
            multiplier = 1
        return self.effective_power() * multiplier

    def attack(self, other):
        damage = self.simulate_damage(other)
        if other.hp <= 0:
            return
        destroyed_units = min(damage // other.hp, other.units)
        other.units -= destroyed_units


def parse_input(data: str):
    """
    Парсим вход в тот же формат Group, что в твоём day24.py.
    Возвращаем список initial_groups.
    """
    initial_groups = []

    blocks = data.split("\n\n")
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split("\n")
        side = lines[0].strip()
        if side.endswith(":"):
            side = side[:-1]

        for line in lines[1:]:
            line = line.strip()
            if not line:
                break

            # units, hp
            units = int(line.split("units")[0])
            hp = int(line.split("with")[1].split("hit")[0])

            # immunities
            immunities_part = line.split("immune to ")
            if len(immunities_part) == 1:
                immunities = []
            else:
                tail = immunities_part[1]
                parenthesis_i = tail.find(")")
                semicolon_i = tail.find(";")

                if parenthesis_i == -1 and semicolon_i == -1:
                    cut_char = ")"
                    cut_pos = len(tail)
                elif parenthesis_i != -1 and semicolon_i == -1:
                    cut_char = ")"
                    cut_pos = parenthesis_i
                elif semicolon_i != -1 and parenthesis_i == -1:
                    cut_char = ";"
                    cut_pos = semicolon_i
                elif semicolon_i < parenthesis_i:
                    cut_char = ";"
                    cut_pos = semicolon_i
                else:
                    cut_char = ")"
                    cut_pos = parenthesis_i

                immunities = tail[:cut_pos].split(", ")
                immunities = [x for x in immunities if x]  # на всякий

            # weaknesses
            weaknesses_part = line.split("weak to ")
            if len(weaknesses_part) == 1:
                weaknesses = []
            else:
                tail = weaknesses_part[1]
                parenthesis_i = tail.find(")")
                semicolon_i = tail.find(";")

                if parenthesis_i == -1 and semicolon_i == -1:
                    cut_char = ")"
                    cut_pos = len(tail)
                elif parenthesis_i != -1 and semicolon_i == -1:
                    cut_char = ")"
                    cut_pos = parenthesis_i
                elif semicolon_i != -1 and parenthesis_i == -1:
                    cut_char = ";"
                    cut_pos = semicolon_i
                elif semicolon_i < parenthesis_i:
                    cut_char = ";"
                    cut_pos = semicolon_i
                else:
                    cut_char = ")"
                    cut_pos = parenthesis_i

                weaknesses = tail[:cut_pos].split(", ")
                weaknesses = [x for x in weaknesses if x]

            # attack type, damage
            attk_info = line.split("with an attack that does ")[1]
            attk_damage = int(attk_info.split(" ")[0])
            attk_type = attk_info.split(" ")[1]

            # initiative
            initiative = int(line.split("at initiative ")[1])

            g = Group(side, units, hp, immunities, weaknesses, attk_type, attk_damage, initiative)
            initial_groups.append(g)

    return initial_groups


def select_targets(groups, debug=False):
    targets = set()
    groups.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)

    for group in groups:
        enemy_groups = [x for x in groups if x.side != group.side and x.units > 0]
        chosen_enemy = None
        max_damage = 0

        available_enemies = [g for g in enemy_groups if g not in targets]

        for enemy in available_enemies:
            damage = group.simulate_damage(enemy)

            good = False
            if chosen_enemy is None:
                good = True
            elif damage > max_damage:
                good = True
            elif damage == max_damage:
                if enemy.effective_power() > chosen_enemy.effective_power():
                    good = True
                elif enemy.effective_power() == chosen_enemy.effective_power():
                    if enemy.initiative > chosen_enemy.initiative:
                        good = True

            if good:
                max_damage = damage
                chosen_enemy = enemy

        if chosen_enemy is not None and max_damage != 0:
            targets.add(chosen_enemy)
            group.target = chosen_enemy
        else:
            group.target = None


def attack_phase(groups, debug=False):
    groups.sort(key=lambda x: x.initiative, reverse=True)
    for group in groups:
        if group.target is not None and group.units > 0:
            group.attack(group.target)


def battle(groups, debug=False):
    """
    Полная симуляция боя.
    Возвращает (winner_side_or_None, финальный_список_групп).
    Если ничья/зацикливание — winner_side_or_None = None.
    """
    won = False

    while not won:
        prev_groups = [x.__copy__() for x in groups]

        select_targets(groups, debug=debug)
        attack_phase(groups, debug=debug)

        # удаляем мёртвые
        groups = [x for x in groups if x.units > 0]

        # проверяем победу
        sides = {group.side for group in groups}
        won = len(sides) == 1

        # проверка зацикливания
        if len(prev_groups) == len(groups):
            same = True
            for i in range(len(groups)):
                if not prev_groups[i] == groups[i]:
                    same = False
                    break
            if same:
                return None, groups

    if len(groups) == 0:
        return None, groups
    else:
        return groups[0].side, groups


def count_units(groups):
    return sum(g.units for g in groups)


def solve_part1(data: str) -> str:
    initial_groups = parse_input(data)
    groups = [g.__copy__() for g in initial_groups]
    winner, final_groups = battle(groups, debug=False)
    return str(count_units(final_groups))


def solve_part2(data: str) -> str:
    initial_groups = parse_input(data)

    boost = 1
    while True:
        # копия с бустом для Immune System
        new_groups = [
            g.boosted_copy(boost) if g.side == "Immune System" else g.__copy__()
            for g in initial_groups
        ]

        winner, final_groups = battle(new_groups, debug=False)
        if winner == "Immune System":
            return str(count_units(final_groups))

        boost += 1


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
