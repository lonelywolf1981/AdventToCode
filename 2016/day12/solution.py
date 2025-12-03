# Advent of Code 2016 - Day 12
# Leonardo's Monorail
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — инструкции вида:
# cpy 41 a
# inc a
# inc a
# dec a
# jnz a 2
# dec a

from pathlib import Path


def _parse_program(data: str):
    """
    Разбираем вход в список инструкций.
    Каждая инструкция — кортеж (op, x, y) или (op, x, None).
    x и y — строки (регистр или число).
    """
    program = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        op = parts[0]
        if op == "cpy":
            # cpy x y
            if len(parts) != 3:
                raise ValueError(f"Неверная cpy: {line!r}")
            x, y = parts[1], parts[2]
            program.append((op, x, y))
        elif op in ("inc", "dec"):
            # inc x / dec x
            if len(parts) != 2:
                raise ValueError(f"Неверная {op}: {line!r}")
            x = parts[1]
            program.append((op, x, None))
        elif op == "jnz":
            # jnz x y
            if len(parts) != 3:
                raise ValueError(f"Неверная jnz: {line!r}")
            x, y = parts[1], parts[2]
            program.append((op, x, y))
        else:
            raise ValueError(f"Неизвестная инструкция: {line!r}")
    return program


def _get_value(arg: str, regs: dict[str, int]) -> int:
    """
    Возвращает значение аргумента:
      - если это имя регистра (a-d), берём из regs
      - иначе парсим как int.
    """
    if arg in regs:
        return regs[arg]
    return int(arg)


def _run_program(program, initial_regs: dict[str, int]) -> dict[str, int]:
    """
    Выполняет программу, возвращает финальное состояние регистров.
    """
    regs = dict(initial_regs)  # копия, чтобы не портить вход
    ip = 0  # instruction pointer

    while 0 <= ip < len(program):
        op, x, y = program[ip]

        if op == "cpy":
            # cpy x y  (y должен быть регистром)
            val = _get_value(x, regs)
            if y in regs:  # на всякий случай игнорируем, если y не регистр
                regs[y] = val
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
        else:
            # сюда не должны попасть
            raise RuntimeError(f"Неизвестная операция во время исполнения: {op!r}")

    return regs


def solve_part1(data: str) -> int:
    """
    Part 1:
    Старт: a=b=c=d=0. Возвращаем значение регистра a после выполнения программы.
    """
    program = _parse_program(data)
    initial = {"a": 0, "b": 0, "c": 0, "d": 0}
    regs = _run_program(program, initial)
    return regs["a"]


def solve_part2(data: str) -> int:
    """
    Part 2:
    Старт: a=0, b=0, c=1, d=0. Возвращаем значение регистра a.
    """
    program = _parse_program(data)
    initial = {"a": 0, "b": 0, "c": 1, "d": 0}
    regs = _run_program(program, initial)
    return regs["a"]


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
