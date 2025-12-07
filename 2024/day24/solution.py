from __future__ import annotations
from typing import Dict, List, Tuple
import re


# ---------- Разбор входа ----------

def parse(data: str):
    """
    Разбиваем вход на:
      - init: начальные значения xNN / yNN
      - gates: список логических ворот (a, op, b, out)
    """
    sections = data.strip().split("\n\n")
    init_block = sections[0].splitlines()
    gate_block = sections[1].splitlines()

    init: Dict[str, int] = {}
    for line in init_block:
        if not line.strip():
            continue
        name, val = line.split(":")
        init[name.strip()] = int(val.strip())

    gates: List[Tuple[str, str, str, str]] = []
    for line in gate_block:
        line = line.strip()
        if not line:
            continue
        m = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", line)
        if not m:
            raise ValueError(f"Не удалось распарсить строку с воротами: {line}")
        a, op, b, out = m.groups()
        gates.append((a, op, b, out))

    return init, gates


# ---------- Симуляция схемы (Part 1) ----------

def simulate(init: Dict[str, int], gates: List[Tuple[str, str, str, str]]) -> Dict[str, int]:
    """
    Прямолинейная симуляция схемы:
      - начинаем с известных init (xNN, yNN)
      - пока можем, вычисляем выходы ворот, у которых оба входа уже известны
    Возвращаем словарь всех wires -> 0/1.
    """
    values: Dict[str, int] = dict(init)
    remaining = list(gates)

    while remaining:
        changed = False
        next_remaining = []
        for a, op, b, out in remaining:
            if a in values and b in values:
                av, bv = values[a], values[b]
                if op == "AND":
                    values[out] = av & bv
                elif op == "OR":
                    values[out] = av | bv
                elif op == "XOR":
                    values[out] = av ^ bv
                else:
                    raise ValueError(f"Неизвестная операция: {op}")
                changed = True
            else:
                next_remaining.append((a, op, b, out))
        if not changed:
            # больше ничего вычислить не можем
            break
        remaining = next_remaining

    return values


def solve_part1(data: str) -> str:
    init, gates = parse(data)
    vals = simulate(init, gates)

    # Собираем число из z-битов: z00 — младший
    z_bits = [(name, val) for name, val in vals.items() if name.startswith("z")]
    z_bits.sort(key=lambda kv: int(kv[0][1:]))

    value = 0
    for i, (_, bit) in enumerate(z_bits):
        value |= (bit << i)

    return str(value)


# ---------- Поиск перепутанных проводов (Part 2) ----------

def solve_part2(data: str) -> str:
    """
    Структурный анализ схемы как набора фулл-аддеров.

    Логика полностью повторяет идею из статьи:
      - находим "неправильные" z-биты,
      - некорректные AND (которые не идут в OR),
      - некорректные XOR (которые прицеплены к OR или вообще не связаны с x/y/z),
      - собираем их выходные имена, сортируем, склеиваем запятыми.
    """
    init, gates = parse(data)

    # Словарь: out_wire -> (in1, op, in2)
    gate_map: Dict[str, Tuple[str, str, str]] = {}
    for a, op, b, out in gates:
        gate_map[out] = (a, op, b)

    # Определим длину в битах по x/y-проводам
    bit_indices = []
    for name in init.keys():
        if name.startswith("x") or name.startswith("y"):
            try:
                bit_indices.append(int(name[1:]))
            except ValueError:
                pass
    if not bit_indices:
        return ""
    BIT_LENGTH = max(bit_indices) + 1

    incorrect: List[str] = []

    # Вспомогательные функции поиска
    def find_gate_by_inputs_and_op(w1: str, w2: str, op: str):
        """
        Ищем ворота (по выходу и описанию), у которых входы — w1 и w2 (в любом порядке) и операция op.
        """
        for out, (a, gop, b) in gate_map.items():
            if gop != op:
                continue
            if (a == w1 and b == w2) or (a == w2 and b == w1):
                return out, (a, gop, b)
        return None

    def find_next_gate_using_wire(wire: str):
        """
        Ищем ворота, где wire используется как один из входов.
        (Берём первый попавшийся — в корректной схеме связи однозначные.)
        """
        for out, (a, op, b) in gate_map.items():
            if a == wire or b == wire:
                return out, (a, op, b)
        return None

    # Основной проход по битам
    for i in range(BIT_LENGTH):
        bit_id = f"{i:02d}"
        xwire = f"x{bit_id}"
        ywire = f"y{bit_id}"
        zwire = f"z{bit_id}"

        xor_gate_entry = find_gate_by_inputs_and_op(xwire, ywire, "XOR")
        and_gate_entry = find_gate_by_inputs_and_op(xwire, ywire, "AND")
        z_gate_entry = gate_map.get(zwire, None)

        if xor_gate_entry is None or and_gate_entry is None or z_gate_entry is None:
            # чего-то не хватает — пропускаем этот бит
            continue

        xor_key, (xor_a, xor_op, xor_b) = xor_gate_entry
        and_key, (and_a, and_op, and_b) = and_gate_entry
        z_a, z_op, z_b = z_gate_entry

        # 1) Все z-биты должны приходить из XOR
        if z_op != "XOR":
            incorrect.append(zwire)

        # 2) AND(xi, yi) должен либо:
        #    - на младшем бите (i == 0) просто быть начальным carry
        #    - на остальных битах вступать во вход OR (формирование carry)
        # Ищем какой-либо gate, где and_key используется как вход
        next_or = None
        for out, (a, op, b) in gate_map.items():
            if a == and_key or b == and_key:
                next_or = (out, (a, op, b))
                break

        if next_or is not None:
            _, (_, or_op, _) = next_or
            if or_op != "OR" and i > 0:
                incorrect.append(and_key)

        # 3) выход XOR(xi, yi) не должен идти в OR напрямую
        next_gate = find_next_gate_using_wire(xor_key)
        if next_gate is not None:
            _, (_, next_op, _) = next_gate
            if next_op == "OR":
                incorrect.append(xor_key)

    # 4) Все XOR-ворота должны быть связаны либо с x*, y* или z*.
    #    Внутренние XOR, не ведущие к x/y/z, подозрительны.
    wrong_xors = []
    for out, (a, op, b) in gate_map.items():
        if op != "XOR":
            continue
        # оба входа НЕ x и НЕ y
        if not (a[0] in ("x", "y")) and not (b[0] in ("x", "y")):
            # и выход не z*
            if not out.startswith("z"):
                wrong_xors.append(out)

    incorrect.extend(wrong_xors)

    # Убираем дубликаты, сортируем, склеиваем
    incorrect_unique = sorted(set(incorrect))
    return ",".join(incorrect_unique)


# ---------- Runner ----------

if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
