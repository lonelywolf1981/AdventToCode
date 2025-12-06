from __future__ import annotations
from typing import List


# ================== Intcode ==================

def parse_program(data: str) -> List[int]:
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


class Intcode:
    def __init__(self, program: List[int]) -> None:
        # "Бесконечная" память: расширяемый список
        self.mem = program[:] + [0] * 10_000
        self.ip = 0
        self.rb = 0
        self.halted = False

    def run(self, inputs: List[int]) -> List[int]:
        """
        Запускаем программу до остановки.
        На вход подаём список целых чисел (ASCII-коды).
        Возвращаем список всех выходных значений.
        """
        inp_pos = 0
        outputs: List[int] = []

        def get_param(mode: int, offset: int) -> int:
            val = self.mem[self.ip + offset]
            if mode == 0:   # позиционный
                return self.mem[val]
            elif mode == 1:  # непосредственный
                return val
            elif mode == 2:  # относительный
                return self.mem[self.rb + val]
            else:
                raise ValueError(f"Unknown mode {mode}")

        def get_addr(mode: int, offset: int) -> int:
            val = self.mem[self.ip + offset]
            if mode == 0:
                return val
            elif mode == 2:
                return self.rb + val
            else:
                raise ValueError(f"Bad mode for write address: {mode}")

        while True:
            instr = self.mem[self.ip]
            opcode = instr % 100
            mode1 = (instr // 100) % 10
            mode2 = (instr // 1000) % 10
            mode3 = (instr // 10000) % 10

            if opcode == 99:
                self.halted = True
                break

            if opcode in (1, 2, 7, 8):
                a = get_param(mode1, 1)
                b = get_param(mode2, 2)
                out_addr = get_addr(mode3, 3)

                if opcode == 1:
                    self.mem[out_addr] = a + b
                elif opcode == 2:
                    self.mem[out_addr] = a * b
                elif opcode == 7:
                    self.mem[out_addr] = 1 if a < b else 0
                elif opcode == 8:
                    self.mem[out_addr] = 1 if a == b else 0

                self.ip += 4

            elif opcode == 3:
                if inp_pos >= len(inputs):
                    raise RuntimeError("Not enough input for opcode 3")
                out_addr = get_addr(mode1, 1)
                self.mem[out_addr] = inputs[inp_pos]
                inp_pos += 1
                self.ip += 2

            elif opcode == 4:
                a = get_param(mode1, 1)
                outputs.append(a)
                self.ip += 2

            elif opcode in (5, 6):
                a = get_param(mode1, 1)
                b = get_param(mode2, 2)
                if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                    self.ip = b
                else:
                    self.ip += 3

            elif opcode == 9:
                a = get_param(mode1, 1)
                self.rb += a
                self.ip += 2

            else:
                raise RuntimeError(f"Unknown opcode {opcode} at ip={self.ip}")

        return outputs


# ================== SPRINGSCRIPT helper ==================

def run_springscript(program: List[int], script_lines: List[str]) -> int:
    """
    Запускает Intcode-программу с заданным скриптом.
    script_lines — список строк (без завершающего \n), последняя строка WALK или RUN.
    Возвращаем последнее выходное значение (обычно damage).
    """
    comp = Intcode(program)
    script = "\n".join(script_lines) + "\n"
    inputs = [ord(ch) for ch in script]
    outputs = comp.run(inputs)

    # Последнее значение > 255 — это damage.
    # Но по условию нам нужен просто последний выход.
    return outputs[-1] if outputs else 0


# ================== Part 1 ==================

def solve_part1(data: str) -> str:
    """
    Part 1: WALK-режим.
    Условие прыжка: (!A or !B or !C) and D
    Реализация на SPRINGSCRIPT:

    NOT A J      # J = !A
    NOT B T      # T = !B
    OR T J       # J = !A or !B
    NOT C T      # T = !C
    OR T J       # J = !A or !B or !C
    AND D J      # J = (!A or !B or !C) and D
    WALK
    """
    program = parse_program(data)

    script = [
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "WALK",
    ]

    damage = run_springscript(program, script)
    return str(damage)


# ================== Part 2 ==================

def solve_part2(data: str) -> str:
    """
    Part 2: RUN-режим.
    Условие прыжка: (!A or !B or !C) and D and (E or H)

    Часть (!A or !B or !C) and D — как в Part 1.
    Затем домножаем на (E or H).

    В SPRINGSCRIPT нет прямого OR/AND с константой, поэтому:

    T = E
      NOT E T   # T = !E
      NOT T T   # T = !!E = E
      OR H T    # T = E or H

    J = J and T
      AND T J
    """
    program = parse_program(data)

    script = [
        # J = (!A or !B or !C)
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        # J = J and D
        "AND D J",
        # T = (E or H)
        "NOT E T",  # T = !E
        "NOT T T",  # T = E
        "OR H T",   # T = E or H
        # J = J and T
        "AND T J",
        "RUN",
    ]

    damage = run_springscript(program, script)
    return str(damage)


# ================== Шаблон запуска ==================

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
