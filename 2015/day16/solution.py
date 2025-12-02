from typing import Dict, List, Tuple


REFERENCE: Dict[str, int] = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse(data: str) -> List[Tuple[int, Dict[str, int]]]:
    """
    Возвращает список (номер_Сью, свойства_Сью)
    """
    sues: List[Tuple[int, Dict[str, int]]] = []

    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        # Формат:
        # Sue 1: children: 1, cars: 8, vizslas: 7
        head, rest = line.split(":", 1)
        _, num_str = head.split()
        num = int(num_str)

        props: Dict[str, int] = {}
        parts = rest.split(",")
        for part in parts:
            part = part.strip()
            if not part:
                continue
            name, val = part.split(":")
            name = name.strip()
            val = int(val.strip())
            props[name] = val

        sues.append((num, props))

    return sues


def matches_part1(props: Dict[str, int]) -> bool:
    """
    Проверка для части 1: все указанные свойства должны совпасть с эталоном.
    """
    for k, v in props.items():
        if REFERENCE.get(k) != v:
            return False
    return True


def matches_part2(props: Dict[str, int]) -> bool:
    """
    Проверка для части 2 с особыми правилами сравнения.
    """
    for k, v in props.items():
        ref = REFERENCE.get(k)
        if k in ("cats", "trees"):
            # у настоящей Сью этих значений больше
            if not (v > ref):
                return False
        elif k in ("pomeranians", "goldfish"):
            # у настоящей Сью этих значений меньше
            if not (v < ref):
                return False
        else:
            # остальные свойства равны
            if v != ref:
                return False
    return True


def solve_part1(data: str) -> str:
    sues = parse(data)
    for num, props in sues:
        if matches_part1(props):
            return str(num)
    # На случай, если ничего не найдено
    return "not found"


def solve_part2(data: str) -> str:
    sues = parse(data)
    for num, props in sues:
        if matches_part2(props):
            return str(num)
    return "not found"


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
