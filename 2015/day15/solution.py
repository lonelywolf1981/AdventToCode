from typing import List, Dict, Tuple
from math import prod


def parse(data: str) -> List[Dict[str, int]]:
    ingredients = []
    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        # Пример:
        # Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
        name_part, rest = line.split(":")
        parts = rest.split(",")
        props = {}
        for p in parts:
            p = p.strip()
            key, val = p.split()[:2]  # key value
            props[key] = int(val)
        ingredients.append(props)
    return ingredients


def generate_distributions(n: int, total: int):
    """
    Генерируем все n-мерные неотрицательные целочисленные вектора,
    сумма которых равна total.
    """
    def rec(i: int, remaining: int, current: List[int]):
        if i == n - 1:
            # последний ингредиент — всё, что осталось
            current.append(remaining)
            yield current[:]
            current.pop()
            return
        for x in range(remaining + 1):
            current.append(x)
            yield from rec(i + 1, remaining - x, current)
            current.pop()

    yield from rec(0, total, [])


def score(ingredients: List[Dict[str, int]], amounts: List[int]) -> Tuple[int, int]:
    """
    Возвращает (score, calories) для данной комбинации amounts.
    score = произведение capacity, durability, flavor, texture (минимум 0)
    calories = сумма калорий.
    """
    props = ["capacity", "durability", "flavor", "texture"]
    sums = {p: 0 for p in props}
    calories = 0

    for amt, ing in zip(amounts, ingredients):
        for p in props:
            sums[p] += ing[p] * amt
        calories += ing["calories"] * amt

    # отрицательные свойства обнуляем
    values = []
    for p in props:
        v = sums[p]
        if v < 0:
            v = 0
        values.append(v)

    # если хоть одно свойство 0, продукт будет 0 — всё равно считаем
    return prod(values), calories


def solve_part1(data: str) -> str:
    ingredients = parse(data)
    n = len(ingredients)
    total = 100

    best = 0
    for amounts in generate_distributions(n, total):
        sc, _ = score(ingredients, amounts)
        if sc > best:
            best = sc

    return str(best)


def solve_part2(data: str) -> str:
    ingredients = parse(data)
    n = len(ingredients)
    total = 100

    best = 0
    for amounts in generate_distributions(n, total):
        sc, cal = score(ingredients, amounts)
        if cal == 500 and sc > best:
            best = sc

    return str(best)


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
