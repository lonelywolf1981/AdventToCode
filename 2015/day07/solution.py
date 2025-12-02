from typing import Dict, List

MASK = 0xFFFF


def parse_instructions(data: str) -> Dict[str, List[str]]:
    wiring: Dict[str, List[str]] = {}
    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        expr, target = line.split("->")
        expr = expr.strip()
        target = target.strip()
        tokens = expr.split()
        wiring[target] = tokens
    return wiring


def eval_wire(name: str, wiring: Dict[str, List[str]], cache: Dict[str, int]) -> int:
    # Константа
    if name.isdigit():
        return int(name) & MASK

    if name in cache:
        return cache[name]

    tokens = wiring[name]

    def val(t: str) -> int:
        return eval_wire(t, wiring, cache) if not t.isdigit() else int(t) & MASK

    if len(tokens) == 1:
        # Просто провод или число
        res = val(tokens[0])
    elif len(tokens) == 2:
        # NOT x
        op, x = tokens
        if op == "NOT":
            res = (~val(x)) & MASK
        else:
            raise ValueError(f"Unknown unary op: {op}")
    elif len(tokens) == 3:
        # x AND y, x OR y, x LSHIFT n, x RSHIFT n
        a, op, b = tokens
        if op == "AND":
            res = (val(a) & val(b)) & MASK
        elif op == "OR":
            res = (val(a) | val(b)) & MASK
        elif op == "LSHIFT":
            res = (val(a) << int(b)) & MASK
        elif op == "RSHIFT":
            res = (val(a) >> int(b)) & MASK
        else:
            raise ValueError(f"Unknown binary op: {op}")
    else:
        raise ValueError(f"Bad tokens for {name}: {tokens}")

    cache[name] = res
    return res


def solve_part1(data: str) -> str:
    wiring = parse_instructions(data)
    cache: Dict[str, int] = {}
    a_val = eval_wire("a", wiring, cache)
    return str(a_val)


def solve_part2(data: str) -> str:
    # Сначала считаем обычное значение 'a'
    wiring = parse_instructions(data)
    cache: Dict[str, int] = {}
    a_val = eval_wire("a", wiring, cache)

    # Теперь пересобираем схему: провод b получает константу a_val
    wiring2 = parse_instructions(data)
    wiring2["b"] = [str(a_val)]

    cache2: Dict[str, int] = {}
    a_val2 = eval_wire("a", wiring2, cache2)
    return str(a_val2)


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

