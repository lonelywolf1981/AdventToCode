from pathlib import Path
from typing import Dict, Tuple


def _parse_input(data: str) -> list[tuple[str, str, int, str, str, int]]:
    """
    Разбираем строки вида:
      b inc 5 if a > 1
    в кортеж:
      (target, op, delta, cond_reg, cond_op, cond_val)
    """
    instructions: list[tuple[str, str, int, str, str, int]] = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        # Ожидаемый формат: <reg> <inc/dec> <value> if <reg2> <op> <value2>
        parts = line.split()
        if len(parts) != 7 or parts[3] != "if":
            raise ValueError(f"Непонятная строка: {line!r}")

        target = parts[0]
        op = parts[1]           # inc / dec
        delta = int(parts[2])
        cond_reg = parts[4]
        cond_op = parts[5]      # > < >= <= == !=
        cond_val = int(parts[6])

        instructions.append((target, op, delta, cond_reg, cond_op, cond_val))

    return instructions


def _eval_cond(lhs: int, op: str, rhs: int) -> bool:
    """
    Оцениваем условие вида lhs <op> rhs.
    op: >, <, >=, <=, ==, !=
    """
    if op == ">":
        return lhs > rhs
    if op == "<":
        return lhs < rhs
    if op == ">=":
        return lhs >= rhs
    if op == "<=":
        return lhs <= rhs
    if op == "==":
        return lhs == rhs
    if op == "!=":
        return lhs != rhs
    raise ValueError(f"Неизвестный оператор сравнения: {op!r}")


def _run_program(
    data: str,
) -> Tuple[int, int]:
    """
    Выполняем все инструкции.
    Возвращаем:
      (max_at_end, max_ever)
      max_at_end — максимум среди регистров после выполнения всех инструкций.
      max_ever   — максимум, который когда-либо был в любом регистре в процессе.
    """
    instructions = _parse_input(data)
    registers: Dict[str, int] = {}

    def get_reg(name: str) -> int:
        return registers.get(name, 0)

    max_ever = 0

    for target, op, delta, cond_reg, cond_op, cond_val in instructions:
        # Проверяем условие
        lhs = get_reg(cond_reg)
        if _eval_cond(lhs, cond_op, cond_val):
            # Выполняем изменение
            current = get_reg(target)
            if op == "inc":
                current += delta
            elif op == "dec":
                current -= delta
            else:
                raise ValueError(f"Неизвестная операция: {op!r}")
            registers[target] = current

            if current > max_ever:
                max_ever = current

    # Если не было ни одной инструкции, максимум в конце = 0
    max_at_end = max(registers.values()) if registers else 0
    return max_at_end, max_ever


def solve_part1(data: str) -> int:
    """
    Day 8, Part 1:
    Максимальное значение в регистрах после выполнения всех инструкций.
    """
    max_at_end, _ = _run_program(data)
    return max_at_end


def solve_part2(data: str) -> int:
    """
    Day 8, Part 2:
    Максимальное значение, которое когда-либо было в каком-либо регистре
    в процессе выполнения программы.
    """
    _, max_ever = _run_program(data)
    return max_ever


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
