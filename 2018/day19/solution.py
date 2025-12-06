from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Callable, Dict
import re


# --- Определения операций (как в Day 16) -------------------------------

def addr(r,a,b,c): r[c] = r[a] + r[b]
def addi(r,a,b,c): r[c] = r[a] + b
def mulr(r,a,b,c): r[c] = r[a] * r[b]
def muli(r,a,b,c): r[c] = r[a] * b
def banr(r,a,b,c): r[c] = r[a] & r[b]
def bani(r,a,b,c): r[c] = r[a] & b
def borr(r,a,b,c): r[c] = r[a] | r[b]
def bori(r,a,b,c): r[c] = r[a] | b
def setr(r,a,b,c): r[c] = r[a]
def seti(r,a,b,c): r[c] = a
def gtir(r,a,b,c): r[c] = 1 if a > r[b] else 0
def gtri(r,a,b,c): r[c] = 1 if r[a] > b else 0
def gtrr(r,a,b,c): r[c] = 1 if r[a] > r[b] else 0
def eqir(r,a,b,c): r[c] = 1 if a == r[b] else 0
def eqri(r,a,b,c): r[c] = 1 if r[a] == b else 0
def eqrr(r,a,b,c): r[c] = 1 if r[a] == r[b] else 0

OPS: Dict[str, Callable] = {
    "addr": addr, "addi": addi,
    "mulr": mulr, "muli": muli,
    "banr": banr, "bani": bani,
    "borr": borr, "bori": bori,
    "setr": setr, "seti": seti,
    "gtir": gtir, "gtri": gtri, "gtrr": gtrr,
    "eqir": eqir, "eqri": eqri, "eqrr": eqrr,
}


# --- Парсер входа -------------------------------------------------------

def parse_program(data: str):
    """
    Возвращает (ip_reg, program):
      ip_reg — номер регистра, связанного с IP
      program — список (opname, a, b, c)
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return 0, []

    m = re.match(r"#ip\s+(\d+)", lines[0])
    if not m:
        raise ValueError("Первая строка должна быть '#ip X'")
    ip_reg = int(m.group(1))
    prog = []
    for line in lines[1:]:
        parts = line.split()
        opname = parts[0]
        a, b, c = map(int, parts[1:])
        prog.append((opname, a, b, c))
    return ip_reg, prog


# --- СИМУЛЯЦИЯ ДЛЯ PART 1 ----------------------------------------------

def run_program(ip_reg: int, prog, regs: List[int], limit_steps: int = 10_000_000) -> List[int]:
    """
    Наивная симуляция программы. Подходит для Part 1 (завершается быстро).
    limit_steps — защита от зацикливания.
    """
    ip = regs[ip_reg]
    steps = 0
    n = len(prog)

    while 0 <= ip < n and steps < limit_steps:
        opname, a, b, c = prog[ip]
        regs[ip_reg] = ip
        OPS[opname](regs, a, b, c)
        ip = regs[ip_reg] + 1
        steps += 1

    return regs


# --- ОПТИМИЗАЦИЯ ДЛЯ PART 2 --------------------------------------------
# Программа AoC Day 19 в Part 2 сводится к вычислению суммы делителей
# определённого числа, который создаётся в регистрах при старте с r0=1.

def extract_target_number(ip_reg: int, prog) -> int:
    """
    Программой AoC 2018 Day 19 создаётся число, чьи делители суммируются.
    Мы его находим, исполнив первые ~20 шагов с r0=1 и отслеживая,
    где накапливается большое значение (обычно в r2 или r5).
    """

    regs = [1, 0, 0, 0, 0, 0]
    ip = 0
    for _ in range(50):  # достаточно, чтобы число стало явно видно
        if not (0 <= ip < len(prog)):
            break
        opname, a, b, c = prog[ip]
        regs[ip_reg] = ip
        OPS[opname](regs, a, b, c)
        ip = regs[ip_reg] + 1

    # Ищем самый большой регистр — это и есть целевое число
    return max(regs)


def sum_of_divisors(n: int) -> int:
    """Сумма всех делителей числа n."""
    s = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            s += i
            if i * i != n:
                s += n // i
        i += 1
    return s


# --- PART 1 -------------------------------------------------------------

def solve_part1(data: str) -> str:
    ip_reg, prog = parse_program(data)
    regs = run_program(ip_reg, prog, [0, 0, 0, 0, 0, 0])
    return str(regs[0])


# --- PART 2 -------------------------------------------------------------

def solve_part2(data: str) -> str:
    ip_reg, prog = parse_program(data)

    # Вычисляем число, для которого нужно найти сумму делителей
    target = extract_target_number(ip_reg, prog)

    # Сумма делителей = ответ
    return str(sum_of_divisors(target))


# --- MAIN WRAPPER -------------------------------------------------------

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
