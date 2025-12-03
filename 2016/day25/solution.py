# Advent of Code 2016 - Day 25
# Clock Signal
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# Язык assembunny с инструкциями:
#   cpy X Y
#   inc X
#   dec X
#   jnz X Y
#   tgl X
#   out X
#
# Наша задача: найти минимальное a >= 0 такое, что программа,
# запущенная с регистрами (a, b=0, c=0, d=0), выдаёт "clock signal"
# 0,1,0,1,... (чередующийся) достаточной длины.


from pathlib import Path


def _parse_program(data: str):
    """
    Разбираем вход в список инструкций.
    Каждая инструкция — [op, x, y], где y может быть None.
    """
    program = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        op = parts[0]
        if op in ("inc", "dec", "tgl", "out"):
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
    instr — [op, x, y].
    """
    op, x, y = instr
    if y is None:
        # инструкции с одним аргументом: inc/dec/tgl/out
        if op == "inc":
            instr[0] = "dec"
        else:
            instr[0] = "inc"
    else:
        # инструкции с двумя аргументами: cpy/jnz
        if op == "jnz":
            instr[0] = "cpy"
        else:
            instr[0] = "jnz"


def _produces_good_clock(program, a_init: int,
                         max_steps: int = 200000,
                         required_outputs: int = 20) -> bool:
    """
    Запускает программу с a = a_init, b=c=d=0.
    Возвращает True, если она выдаёт хотя бы required_outputs значений
    через команду out, образующих последовательность 0,1,0,1,..., начиная с 0.
    Иначе False (включая превышение max_steps или раннее завершение).
    """
    regs = {"a": a_init, "b": 0, "c": 0, "d": 0}
    prog = [instr[:] for instr in program]  # копия, чтобы tgl мог менять код
    ip = 0

    last_out = None
    out_count = 0
    steps = 0

    while 0 <= ip < len(prog) and steps < max_steps and out_count < required_outputs:
        steps += 1
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

        elif op == "out":
            val = _get_value(x, regs)
            # допустим только 0 или 1
            if val not in (0, 1):
                return False
            # первая должна быть 0
            if last_out is None:
                if val != 0:
                    return False
            else:
                # далее строго чередуемся
                if val == last_out:
                    return False

            last_out = val
            out_count += 1
            ip += 1

        else:
            raise RuntimeError(f"Неизвестная операция во время исполнения: {op!r}")

    # если набрали достаточно правильных выходов — считаем, что clock OK
    return out_count >= required_outputs


def solve_part1(data: str) -> int:
    """
    Part 1:
    Находим минимальное a >= 0, для которого программа выдаёт
    достаточную префиксную последовательность 0,1,0,1,...
    """
    program = _parse_program(data)

    a = 0
    while True:
        if _produces_good_clock(program, a):
            return a
        a += 1


def solve_part2(data: str) -> int:
    """
    Part 2:
    В Day 25 официально нет второй части, но для совместимости
    просто возвращаем тот же результат, что и Part 1.
    Если раннер игнорирует Part 2 — это тоже безопасно.
    """
    return solve_part1(data)


def main():
    # Локальный запуск: читаем input.txt из текущей папки
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
