from __future__ import annotations
from typing import List, Tuple


def parse_input(data: str) -> Tuple[int, int, int, List[int]]:
    """
    Ожидаемый формат:

    Register A: 59590048
    Register B: 0
    Register C: 0

    Program: 2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if len(lines) < 4:
        return 0, 0, 0, []

    a_line = lines[0]
    b_line = lines[1]
    c_line = lines[2]

    A = int(a_line.split(":")[1].strip())
    B = int(b_line.split(":")[1].strip())
    C = int(c_line.split(":")[1].strip())

    # Ищем строку с программой
    prog_line = next(
        line for line in lines if line.lower().startswith("program:")
    )
    prog_str = prog_line.split(":", 1)[1].strip()
    program = [int(x) for x in prog_str.split(",") if x.strip()]

    return A, B, C, program


def combo_value(operand: int, A: int, B: int, C: int) -> int:
    """
    Комбо-операнд:
      0..3 -> литералы,
      4 -> A,
      5 -> B,
      6 -> C.
    (7 не встречается)
    """
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return A
    if operand == 5:
        return B
    if operand == 6:
        return C
    raise ValueError(f"Invalid combo operand: {operand}")


def run_program(A0: int, B0: int, C0: int, program: List[int]) -> List[int]:
    """
    Запускает виртуальную машину и возвращает список выводов (out).
    """
    A = int(A0)
    B = int(B0)
    C = int(C0)
    ip = 0
    out: List[int] = []

    n = len(program)

    while 0 <= ip < n:
        opcode = program[ip]
        if ip + 1 >= n:
            break
        operand = program[ip + 1]

        if opcode == 0:  # adv
            cv = combo_value(operand, A, B, C)
            denom = 1 << cv
            A = A // denom
            ip += 2

        elif opcode == 1:  # bxl
            B = B ^ operand
            ip += 2

        elif opcode == 2:  # bst
            cv = combo_value(operand, A, B, C)
            B = cv % 8
            ip += 2

        elif opcode == 3:  # jnz
            if A != 0:
                ip = operand
            else:
                ip += 2

        elif opcode == 4:  # bxc
            B = B ^ C
            ip += 2

        elif opcode == 5:  # out
            cv = combo_value(operand, A, B, C)
            out.append(cv % 8)
            ip += 2

        elif opcode == 6:  # bdv
            cv = combo_value(operand, A, B, C)
            denom = 1 << cv
            B = A // denom
            ip += 2

        elif opcode == 7:  # cdv
            cv = combo_value(operand, A, B, C)
            denom = 1 << cv
            C = A // denom
            ip += 2

        else:
            # Неверный opcode — по условию такого не будет
            break

    return out


def solve_part1(data: str) -> str:
    A0, B0, C0, program = parse_input(data)
    if not program:
        return ""

    outputs = run_program(A0, B0, C0, program)
    return ",".join(str(x) for x in outputs)


def find_minimal_A_for_quine(B0: int, C0: int, program: List[int]) -> int:
    """
    Ищем минимальное A > 0 такое, что run_program(A, B0, C0, program)
    выводит точную копию program.

    Алгоритм:
      - строим A по 3 бита (octal-цифры) с хвоста,
      - на каждом шаге оставляем только те кандидаты, у которых
        первый вывод совпадает с нужной цифрой (берём цифры программы с конца).
    """
    if not program:
        return 0

    reversed_prog = list(reversed(program))
    candidates = [0]

    for target in reversed_prog:
        new_candidates = set()
        for prev in candidates:
            base = prev << 3  # сдвиг на одну октальную цифру
            for d in range(8):
                candidate = base | d
                out = run_program(candidate, B0, C0, program)
                if not out:
                    continue
                # Здесь используем ту же эвристику, что и в большинстве решений:
                # первая цифра вывода должна совпадать с текущей "хвостовой" цифрой.
                if out[0] == target:
                    new_candidates.add(candidate)
        if not new_candidates:
            raise RuntimeError("Не удалось найти ни одного кандидата A — что-то пошло не так")
        candidates = sorted(new_candidates)

    # оставляем только положительные и проверяем, что действительно получаем программу
    valid = []
    for a in candidates:
        if a <= 0:
            continue
        out = run_program(a, B0, C0, program)
        if out == program:
            valid.append(a)

    if not valid:
        raise RuntimeError("Не найдено положительное A, дающее точную копию программы")

    return min(valid)


def solve_part2(data: str) -> str:
    _, B0, C0, program = parse_input(data)
    if not program:
        return "0"

    best_A = find_minimal_A_for_quine(B0, C0, program)
    return str(best_A)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
