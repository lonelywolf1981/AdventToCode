from __future__ import annotations
from typing import List, Tuple, Optional


# ================== Intcode ==================


def parse_program(data: str) -> List[int]:
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


class Intcode:
    def __init__(self, program: List[int]):
        # Делаем "расширяемую" память
        self.mem = program[:] + [0] * 10000
        self.ip = 0
        self.rb = 0
        self.halted = False

    def run(self, inputs: List[int]) -> List[int]:
        """
        Запускаем программу до остановки.
        Возвращаем все outputs.
        """
        inp_pos = 0
        outputs: List[int] = []

        def get_param(mode: int, offset: int) -> int:
            val = self.mem[self.ip + offset]
            if mode == 0:  # позиционный
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


def probe(program: List[int], x: int, y: int) -> int:
    """
    Возвращает 0 или 1 — находится ли точка (x,y) в луче.
    Для каждого запроса создаём новую машину.
    """
    comp = Intcode(program)
    out = comp.run([x, y])
    if not out:
        return 0
    return out[-1]


# ================== Part 1 ==================


def solve_part1(data: str) -> str:
    program = parse_program(data)
    affected = 0
    for y in range(50):
        for x in range(50):
            if probe(program, x, y) == 1:
                affected += 1
    return str(affected)


# ================== Part 2 ==================


def solve_part2(data: str) -> str:
    program = parse_program(data)

    # Идея:
    #  - луч почти непрерывный "клин", расширяется с ростом y.
    #  - левая граница луча по x монотонно не убывает.
    #  - проверяем строки по y, двигая x только вперёд.
    #  - для каждой строки y ищем первый x, где начинается луч,
    #    и проверяем, помещается ли квадрат 100x100.
    #
    #  Форма условия для квадрата:
    #   есть y (нижняя сторона квадрата) и x (левая сторона),
    #   такие что:
    #     (x, y)      в луче
    #     (x+99, y-99) в луче
    #   тогда квадрат 100x100 вписывается (по свойствам луча).

    size = 100
    x = 0
    y = size  # начинать можно примерно с 100-й строки

    while True:
        # смещаем x, пока не войдём в луч
        while probe(program, x, y) == 0:
            x += 1

        # теперь (x, y) в луче; проверим верхний левый угол квадрата
        top_y = y - (size - 1)
        right_x = x + (size - 1)

        if top_y >= 0 and probe(program, right_x, top_y) == 1:
            # нашли квадрат: (x, top_y) — его верхний левый угол
            answer = x * 10000 + top_y
            return str(answer)

        # иначе, идём ниже
        y += 1


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
