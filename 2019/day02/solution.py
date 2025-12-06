from __future__ import annotations

from typing import List


def parse_program(data: str) -> List[int]:
    """
    Разбор программы Intcode.
    Как правило, числа разделены запятыми, но на всякий случай
    уберём переводы строк.
    """
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


def run_intcode(memory: List[int]) -> List[int]:
    """
    Запуск Intcode-программы (опкоды 1, 2, 99).
    Работает только в позиционном режиме (как в Day 2).
    Возвращает изменённую память.
    """
    ip = 0  # instruction pointer

    while True:
        opcode = memory[ip]

        if opcode == 99:
            break
        elif opcode in (1, 2):
            a_pos = memory[ip + 1]
            b_pos = memory[ip + 2]
            out_pos = memory[ip + 3]

            a_val = memory[a_pos]
            b_val = memory[b_pos]

            if opcode == 1:
                memory[out_pos] = a_val + b_val
            else:  # opcode == 2
                memory[out_pos] = a_val * b_val

            ip += 4
        else:
            raise ValueError(f"Неизвестный opcode {opcode} на позиции {ip}")

    return memory


def solve_part1(data: str) -> str:
    """
    Part 1: установить noun=12, verb=2 и вывести memory[0] после выполнения.
    """
    program = parse_program(data)
    program[1] = 12
    program[2] = 2

    result_mem = run_intcode(program)
    return str(result_mem[0])


def solve_part2(data: str) -> str:
    """
    Part 2: подобрать noun и verb (0..99), чтобы после выполнения
    result_mem[0] == 19690720, и вернуть 100 * noun + verb.
    """
    target = 19690720
    base_program = parse_program(data)

    for noun in range(100):
        for verb in range(100):
            program = base_program.copy()
            program[1] = noun
            program[2] = verb

            result_mem = run_intcode(program)
            if result_mem[0] == target:
                answer = 100 * noun + verb
                return str(answer)

    raise RuntimeError("Подходящие noun и verb не найдены в диапазоне 0..99")


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
