from pathlib import Path
from typing import List, Tuple, Dict, Optional


Instruction = Tuple[str, str, Optional[str]]  # (op, X, Y_or_None)


def _parse_program(data: str) -> List[Instruction]:
    """
    Разбираем input.txt в список инструкций:
    (op, x, y_or_None)
    """
    program: List[Instruction] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        op = parts[0]
        x = parts[1]
        y = parts[2] if len(parts) > 2 else None
        program.append((op, x, y))
    if not program:
        raise ValueError("Пустой input для Day 23")
    return program


def _get_value(token: str, regs: Dict[str, int]) -> int:
    """
    Получить значение операнда: либо число, либо значение регистра.
    """
    try:
        return int(token)
    except ValueError:
        return regs.get(token, 0)


# ---------- Part 1: прямой интерпретатор ----------

def solve_part1(data: str) -> int:
    """
    Day 23, Part 1:
    Запускаем программу (a..h = 0), считаем количество вызовов 'mul'.
    """
    program = _parse_program(data)
    regs: Dict[str, int] = {}
    ip = 0
    mul_count = 0

    while 0 <= ip < len(program):
        op, x, y = program[ip]

        if op == "set":
            assert y is not None
            regs[x] = _get_value(y, regs)
            ip += 1

        elif op == "sub":
            assert y is not None
            regs[x] = regs.get(x, 0) - _get_value(y, regs)
            ip += 1

        elif op == "mul":
            assert y is not None
            regs[x] = regs.get(x, 0) * _get_value(y, regs)
            mul_count += 1
            ip += 1

        elif op == "jnz":
            assert y is not None
            cond = _get_value(x, regs)
            if cond != 0:
                ip += _get_value(y, regs)
            else:
                ip += 1

        else:
            raise ValueError(f"Неизвестная инструкция: {op!r}")

    return mul_count


# ---------- Part 2: аккуратная раскрутка через короткую симуляцию ----------

def _init_bc_with_a1(program: List[Instruction]) -> Tuple[int, int]:
    """
    Запускаем программу с a = 1, но только на коротком префиксе,
    пока не будет выполнена первая инструкция вида 'sub c -N'.
    После этого b и c уже инициализированы (как в исходном коде AoC).

    Возвращаем (b_start, c).
    """
    regs: Dict[str, int] = {"a": 1}
    ip = 0

    visited_sub_c = False
    steps = 0
    max_steps = 10_000  # с большим запасом: реально нужно меньше сотни

    while 0 <= ip < len(program):
        if steps > max_steps:
            raise RuntimeError("Слишком много шагов при инициализации b/c; формат программы, похоже, другой.")
        steps += 1

        op, x, y = program[ip]

        if op == "set":
            assert y is not None
            regs[x] = _get_value(y, regs)
            ip += 1

        elif op == "sub":
            assert y is not None
            regs[x] = regs.get(x, 0) - _get_value(y, regs)
            # ловим именно 'sub c -N'
            if x == "c" and y.startswith("-"):
                visited_sub_c = True
                ip += 1
                break  # после этого c и b установлены как нужно
            else:
                ip += 1

        elif op == "mul":
            assert y is not None
            regs[x] = regs.get(x, 0) * _get_value(y, regs)
            ip += 1

        elif op == "jnz":
            assert y is not None
            cond = _get_value(x, regs)
            if cond != 0:
                ip += _get_value(y, regs)
            else:
                ip += 1

        else:
            raise ValueError(f"Неизвестная инструкция: {op!r}")

    if not visited_sub_c:
        raise RuntimeError("Не нашли инициализирующую 'sub c -N' при a=1 — формат программы другой?")

    b_start = regs.get("b", 0)
    c = regs.get("c", 0)
    return b_start, c


def _is_prime(n: int) -> bool:
    """
    Простая проверка на простоту.
    Хватает для диапазона значений из задачки.
    """
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def solve_part2(data: str) -> int:
    """
    Day 23, Part 2:
    При a = 1 программа по сути считает количество НЕпростых чисел
    в диапазоне [b_start, c] с шагом 17.
    Мы честно вытаскиваем b_start и c короткой симуляцией, а дальше
    считаем составные числа напрямую.
    """
    program = _parse_program(data)
    b_start, c = _init_bc_with_a1(program)

    h = 0
    for b in range(b_start, c + 1, 17):
        if not _is_prime(b):
            h += 1

    return h


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
