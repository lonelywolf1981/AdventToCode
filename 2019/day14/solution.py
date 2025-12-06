from __future__ import annotations
from typing import Dict, List, Tuple

Chemical = str
Quantity = int
ReactionInputs = List[Tuple[Chemical, Quantity]]
ReactionsMap = Dict[Chemical, Tuple[Quantity, ReactionInputs]]


def parse_reactions(data: str) -> ReactionsMap:
    """
    Парсим вход:
    7 A, 1 B => 1 C
    2 AB, 3 BC, 4 CA => 1 FUEL
    5 ORE => 4 CA
    ...
    Возвращаем словарь:
      продукт -> (выходное_количество, [(реагент, количество), ...])
    """
    reactions: ReactionsMap = {}
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        left, right = line.split("=>")
        inputs_part = left.strip()
        output_part = right.strip()

        # Выход
        out_qty_str, out_chem = output_part.split()
        out_qty = int(out_qty_str)

        # Входы
        inputs: ReactionInputs = []
        for chunk in inputs_part.split(","):
            chunk = chunk.strip()
            qty_str, chem = chunk.split()
            inputs.append((chem, int(qty_str)))

        reactions[out_chem] = (out_qty, inputs)

    return reactions


def ore_for(
    chem: Chemical,
    amount: int,
    reactions: ReactionsMap,
    leftovers: Dict[Chemical, int],
) -> int:
    """
    Рекурсивно считаем, сколько ORE нужно для получения `amount` вещества `chem`,
    учитывая остатки в `leftovers`.
    """
    if chem == "ORE":
        return amount

    # Остатки уже произведённого химиката
    have = leftovers.get(chem, 0)
    if have >= amount:
        leftovers[chem] = have - amount
        return 0
    elif have > 0:
        amount -= have
        leftovers[chem] = 0

    if chem not in reactions:
        raise ValueError(f"Нет реакции для химиката {chem}")

    out_qty, inputs = reactions[chem]

    # Сколько раз нужно запустить реакцию, чтобы покрыть нужное количество
    times = (amount + out_qty - 1) // out_qty  # ceil(amount / out_qty)

    produced = times * out_qty
    leftover = produced - amount
    if leftover > 0:
        leftovers[chem] = leftovers.get(chem, 0) + leftover

    total_ore = 0
    for in_chem, in_qty in inputs:
        need_amount = in_qty * times
        total_ore += ore_for(in_chem, need_amount, reactions, leftovers)

    return total_ore


def ore_needed_for_fuel(reactions: ReactionsMap, fuel_amount: int) -> int:
    """
    Обёртка: сколько ORE нужно для fuel_amount FUEL.
    Каждый расчёт — с чистыми остатками.
    """
    leftovers: Dict[Chemical, int] = {}
    return ore_for("FUEL", fuel_amount, reactions, leftovers)


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    reactions = parse_reactions(data)
    ore = ore_needed_for_fuel(reactions, fuel_amount=1)
    return str(ore)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    reactions = parse_reactions(data)
    ore_limit = 1_000_000_000_000

    # Бинарный поиск по количеству FUEL
    low = 1
    high = 1

    # Сначала найдём верхнюю границу, где ORE уже не хватает
    while ore_needed_for_fuel(reactions, high) <= ore_limit:
        high *= 2

    # Теперь бинарный поиск в [low, high)
    while low + 1 < high:
        mid = (low + high) // 2
        ore = ore_needed_for_fuel(reactions, mid)
        if ore <= ore_limit:
            low = mid
        else:
            high = mid

    # low — максимальное целое количество FUEL, укладывающееся в ore_limit
    return str(low)


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
