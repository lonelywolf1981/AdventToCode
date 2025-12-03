# Advent of Code 2016 - Day 23
# Safe Cracking
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — программа на assembunny с инструкциями:
# cpy, inc, dec, jnz, tgl

from pathlib import Path


def _parse_program(data: str):
    """
    Разбираем вход в список инструкций.
    Каждая инструкция — список: [op, x, y], где y может быть None.
    """
    program = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        op = parts[0]
        if op in ("inc", "dec", "tgl"):
            if len(parts) != 2:
                raise ValueError(f"Неверная {op}-инструкция: {line!r}")
            program.append([op, parts[1], None])
        elif op in ("cpy", "jnz"):
            if len(parts) != 3:
                raise ValueError(f"Неверная {op}-инструкция: {line!r}")
            program.append([op, parts[1], parts[2]])
        else:
            raise ValueError(f"Неизвестная инструкция: {line!r}")
    return program


def _get_value(arg: str, regs: dict) -> int:
    """
    Если arg — имя регистра, возвращаем regs[arg],
    иначе парсим как целое число.
    """
    if arg in regs:
        return regs[arg]
    return int(arg)


def _toggle_instruction(instr: list[str]):
    """
    Применяет правило tgl к одной инструкции (in place).
    instr — список [op, x, y].
    """
    op, x, y = instr
    if y is None:
        # одна аргументная
        if op == "inc":
            instr[0] = "dec"
        else:
            instr[0] = "inc"
    else:
        # два аргумента
        if op == "jnz":
            instr[0] = "cpy"
        else:
            instr[0] = "jnz"


def _try_mul_optimization(ip: int, prog: list[list[str]], regs: dict) -> bool:
    """
    Пытаемся распознать в prog[ip:ip+6] шаблон "двойного цикла умножения":
        cpy X Y
        inc Z
        dec Y
        jnz Y -2
        dec W
        jnz W -5

    Если совпало — выполняем эквивалентную операцию:
        Z += value(X) * regs[W]
        regs[Y] = 0
        regs[W] = 0
        ip += 6

    Возвращаем True, если оптимизация применена,
    иначе False (нужно исполнять обычный шаг).
    """
    if ip < 0 or ip + 5 >= len(prog):
        return False

    i0 = prog[ip]
    i1 = prog[ip + 1]
    i2 = prog[ip + 2]
    i3 = prog[ip + 3]
    i4 = prog[ip + 4]
    i5 = prog[ip + 5]

    # Проверяем форму инструкций
    if not (i0[0] == "cpy" and i1[0] == "inc" and i2[0] == "dec" and
            i3[0] == "jnz" and i4[0] == "dec" and i5[0] == "jnz"):
        return False

    X, Y = i0[1], i0[2]      # cpy X Y
    Z = i1[1]                # inc Z
    Y2 = i2[1]               # dec Y
    Y3, off1 = i3[1], i3[2]  # jnz Y -2
    W = i4[1]                # dec W
    W2, off2 = i5[1], i5[2]  # jnz W -5

    # Проверяем, что это именно тот цикл:
    # dec Y; jnz Y -2
    # dec W; jnz W -5
    if not (Y == Y2 == Y3 and W == W2):
        return False
    if off1 != "-2" or off2 != "-5":
        return False
    # Все регистровые аргументы должны быть регистрами
    if any(reg not in regs for reg in (Y, Z, W)):
        return False

    # Теперь выполняем оптимизацию:
    # Z += value(X) * regs[W]; Y = 0; W = 0
    val_x = _get_value(X, regs)
    regs[Z] += val_x * regs[W]
    regs[Y] = 0
    regs[W] = 0

    # ip будет увеличен на 6 снаружи в _run_program,
    # поэтому здесь ничего не меняем, а просто скажем,
    # что мы "съели" этот блок.
    return True


def _run_program(program, initial_regs: dict) -> dict:
    """
    Выполняет программу с поддержкой tgl и peephole-оптимизацией.
    Возвращает финальное состояние регистров.
    """
    regs = dict(initial_regs)
    prog = [instr[:] for instr in program]  # копия, т.к. tgl меняет код
    ip = 0

    while 0 <= ip < len(prog):
        # Пытаемся применить оптимизацию умножающего цикла
        if _try_mul_optimization(ip, prog, regs):
            ip += 6
            continue

        op, x, y = prog[ip]

        if op == "cpy":
            if y in regs:
                regs[y] = _get_value(x, regs)
            ip += 1

        elif op == "inc":
            if x in regs:
                regs[x] += 1
            ip += 1

        elif op == "dec":
            if x in regs:
                regs[x] -= 1
            ip += 1

        elif op == "jnz":
            val = _get_value(x, regs)
            offset = _get_value(y, regs)
            if val != 0:
                ip += offset
            else:
                ip += 1

        elif op == "tgl":
            target_ip = ip + _get_value(x, regs)
            if 0 <= target_ip < len(prog):
                _toggle_instruction(prog[target_ip])
            ip += 1

        else:
            raise RuntimeError(f"Неизвестная операция во время исполнения: {op!r}")

    return regs


def solve_part1(data: str) -> int:
    """
    Part 1:
    Старт: a=7, b=c=d=0.
    Возвращаем значение регистра a после завершения программы.
    """
    program = _parse_program(data)
    initial = {"a": 7, "b": 0, "c": 0, "d": 0}
    regs = _run_program(program, initial)
    return regs["a"]


def solve_part2(data: str) -> int:
    """
    Part 2:
    Старт: a=12, b=c=d=0.
    Возвращаем значение регистра a.
    Благодаря peephole-оптимизации всё выполняется быстро.
    """
    program = _parse_program(data)
    initial = {"a": 12, "b": 0, "c": 0, "d": 0}
    regs = _run_program(program, initial)
    return regs["a"]


def main():
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
