from __future__ import annotations

from typing import List, Tuple


def parse_program(data: str) -> List[int]:
    """
    Разбор Intcode-программы: числа через запятую (возможны переводы строк).
    """
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


def run_intcode(program: List[int], input_values: List[int]) -> Tuple[List[int], List[int]]:
    """
    Универсальный интерпретатор Intcode (для Day 5):
    Опкоды:
      1 - add
      2 - mul
      3 - input
      4 - output
      5 - jump-if-true
      6 - jump-if-false
      7 - less-than
      8 - equals
     99 - halt

    Режимы параметров:
      0 - позиционный (адрес)
      1 - непосредственный (значение)

    Возвращает (outputs, final_memory).
    """
    memory = program.copy()
    ip = 0  # instruction pointer
    inputs = list(input_values)
    input_pos = 0
    outputs: List[int] = []

    def get_param(mode: int, offset: int) -> int:
        """
        Прочитать параметр с учётом режима.
        offset — смещение от ip (1, 2, 3, ...).
        """
        val = memory[ip + offset]
        if mode == 0:  # позиционный
            return memory[val]
        elif mode == 1:  # непосредственный
            return val
        else:
            raise ValueError(f"Неизвестный режим параметра: {mode}")

    def get_addr(offset: int) -> int:
        """
        Адрес для записи (в этих задачах всегда позиционный режим).
        """
        return memory[ip + offset]

    while True:
        instr = memory[ip]
        opcode = instr % 100
        modes = instr // 100  # дальше раскладываем по цифрам

        if opcode == 99:
            break

        # Для удобства режимы параметров берём по одной цифре
        mode1 = modes % 10
        mode2 = (modes // 10) % 10
        mode3 = (modes // 100) % 10  # на будущее, здесь не нужен

        if opcode in (1, 2, 7, 8):
            # три параметра: два чтения, одна запись
            p1 = get_param(mode1, 1)
            p2 = get_param(mode2, 2)
            out_addr = get_addr(3)

            if opcode == 1:      # add
                memory[out_addr] = p1 + p2
            elif opcode == 2:    # mul
                memory[out_addr] = p1 * p2
            elif opcode == 7:    # less-than
                memory[out_addr] = 1 if p1 < p2 else 0
            elif opcode == 8:    # equals
                memory[out_addr] = 1 if p1 == p2 else 0

            ip += 4

        elif opcode == 3:
            # input
            if input_pos >= len(inputs):
                raise RuntimeError("Закончились входные данные для opcode 3")
            out_addr = get_addr(1)
            memory[out_addr] = inputs[input_pos]
            input_pos += 1
            ip += 2

        elif opcode == 4:
            # output
            p1 = get_param(mode1, 1)
            outputs.append(p1)
            ip += 2

        elif opcode in (5, 6):
            # jumps
            p1 = get_param(mode1, 1)
            p2 = get_param(mode2, 2)

            if opcode == 5:  # jump-if-true
                if p1 != 0:
                    ip = p2
                else:
                    ip += 3
            elif opcode == 6:  # jump-if-false
                if p1 == 0:
                    ip = p2
                else:
                    ip += 3

        else:
            raise ValueError(f"Неизвестный opcode {opcode} на позиции {ip}")

    return outputs, memory


def solve_part1(data: str) -> str:
    """
    Part 1: запускаем программу с входом 1,
    возвращаем последний выведенный диагностический код.
    """
    program = parse_program(data)
    outputs, _ = run_intcode(program, [1])

    if not outputs:
        raise RuntimeError("Программа не вывела ни одного значения (Part 1).")

    return str(outputs[-1])


def solve_part2(data: str) -> str:
    """
    Part 2: запускаем программу с входом 5,
    возвращаем последний выведенный диагностический код.
    """
    program = parse_program(data)
    outputs, _ = run_intcode(program, [5])

    if not outputs:
        raise RuntimeError("Программа не вывела ни одного значения (Part 2).")

    return str(outputs[-1])


if __name__ == "__main__":
    import pathlib
    import sys

    input_path = pathlib.Path("input.txt")
    data = input_path.read_text(encoding="utf-8").strip()

    part = sys.argv[1] if len(sys.argv) > 1 else "both"

    if part in ("1", "one", "part1", "both"):
        print("Part 1:", solve_part1(data))
    if part in ("2", "two", "part2", "both"):
        print("Part 2:", solve_part2(data))
