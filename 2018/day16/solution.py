from pathlib import Path
from typing import List, Tuple, Dict, Callable
import re


# =========================
#   Определения операций
# =========================

def addr(r, a, b, c): r[c] = r[a] + r[b]
def addi(r, a, b, c): r[c] = r[a] + b

def mulr(r, a, b, c): r[c] = r[a] * r[b]
def muli(r, a, b, c): r[c] = r[a] * b

def banr(r, a, b, c): r[c] = r[a] & r[b]
def bani(r, a, b, c): r[c] = r[a] & b

def borr(r, a, b, c): r[c] = r[a] | r[b]
def bori(r, a, b, c): r[c] = r[a] | b

def setr(r, a, b, c): r[c] = r[a]
def seti(r, a, b, c): r[c] = a

def gtir(r, a, b, c): r[c] = 1 if a     > r[b] else 0
def gtri(r, a, b, c): r[c] = 1 if r[a] > b     else 0
def gtrr(r, a, b, c): r[c] = 1 if r[a] > r[b] else 0

def eqir(r, a, b, c): r[c] = 1 if a     == r[b] else 0
def eqri(r, a, b, c): r[c] = 1 if r[a] == b     else 0
def eqrr(r, a, b, c): r[c] = 1 if r[a] == r[b] else 0


OPS: Dict[str, Callable] = {
    "addr": addr, "addi": addi,
    "mulr": mulr, "muli": muli,
    "banr": banr, "bani": bani,
    "borr": borr, "bori": bori,
    "setr": setr, "seti": seti,
    "gtir": gtir, "gtri": gtri, "gtrr": gtrr,
    "eqir": eqir, "eqri": eqri, "eqrr": eqrr,
}


# =========================
#     Парсер входа
# =========================

def parse_input(data: str):
    """
    Разделяем input на:
      - список примеров (before, instruction, after)
      - список инструкций программы
    """

    before_re = re.compile(r"Before:\s*\[(.*)\]")
    after_re  = re.compile(r"After:\s*\[(.*)\]")

    lines = data.splitlines()
    samples = []
    program = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = before_re.match(line)
        if m:
            before = list(map(int, m.group(1).split(",")))
            instr = list(map(int, lines[i+1].split()))
            m2 = after_re.match(lines[i+2].strip())
            after = list(map(int, m2.group(1).split(",")))
            samples.append((before, instr, after))
            i += 3
        else:
            i += 1

    # остальное — программа
    for line in lines:
        parts = line.split()
        if len(parts) == 4 and all(p.lstrip("-").isdigit() for p in parts):
            program.append(list(map(int, parts)))

    return samples, program


# =========================
#        Part 1
# =========================

def count_matching_ops(before, instr, after):
    opcode, a, b, c = instr
    count = 0
    for name, op in OPS.items():
        regs = before[:]  # копия
        op(regs, a, b, c)
        if regs == after:
            count += 1
    return count


def solve_part1(data: str) -> str:
    samples, _ = parse_input(data)
    total = sum(1 for (before, instr, after) in samples if count_matching_ops(before, instr, after) >= 3)
    return str(total)


# =========================
#        Part 2
# =========================

def find_opcode_mapping(samples):
    """
    Выводим отображение opcode → операция (по имени).
    Используем пересечение возможных операций и постепенное исключение.
    """

    possible: Dict[int, set] = {i: set(OPS.keys()) for i in range(16)}

    # Уточняем по каждому примеру
    for before, instr, after in samples:
        opcode, a, b, c = instr
        good = set()
        for name, op in OPS.items():
            regs = before[:]
            op(regs, a, b, c)
            if regs == after:
                good.add(name)
        # пересекаем
        possible[opcode] &= good

    # процесс исключения (как в Судоку)
    final = {}
    changed = True
    while changed:
        changed = False
        solved = {op for op, s in possible.items() if len(s) == 1}
        taken = {next(iter(possible[op])) for op in solved}
        for op in possible:
            if len(possible[op]) > 1:
                newset = possible[op] - taken
                if newset != possible[op]:
                    possible[op] = newset
                    changed = True

    for op, s in possible.items():
        final[op] = next(iter(s))

    return final


def run_program(program, mapping):
    regs = [0, 0, 0, 0]
    for opcode, a, b, c in program:
        name = mapping[opcode]
        OPS[name](regs, a, b, c)
    return regs[0]


def solve_part2(data: str) -> str:
    samples, program = parse_input(data)
    mapping = find_opcode_mapping(samples)
    result = run_program(program, mapping)
    return str(result)


# =========================
#     main wrapper
# =========================

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
