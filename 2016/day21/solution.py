# Advent of Code 2016 - Day 21
# Scrambled Letters and Hash
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> str
#   solve_part2(raw_input: str) -> str
#
# В файле input.txt — инструкции вида:
# swap position X with position Y
# swap letter a with letter b
# rotate left/right X steps
# rotate based on position of letter X
# reverse positions X through Y
# move position X to position Y

from pathlib import Path


# ---------- Вспомогательные функции ----------

def _rotate_left(s: str, steps: int) -> str:
    n = len(s)
    steps %= n
    return s[steps:] + s[:steps]


def _rotate_right(s: str, steps: int) -> str:
    n = len(s)
    steps %= n
    return s[-steps:] + s[:-steps]


def _parse_instructions(data: str):
    """
    Разбираем вход в список инструкций.
    Храним исходные строки и заранее распарсенные аргументы.
    """
    instructions = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        instructions.append(line)
    return instructions


# ---------- Прямое применение инструкций ----------

def _apply_instruction(password: str, instr: str) -> str:
    parts = instr.split()

    if instr.startswith("swap position"):
        # swap position X with position Y
        x = int(parts[2])
        y = int(parts[5])
        pw = list(password)
        pw[x], pw[y] = pw[y], pw[x]
        return "".join(pw)

    if instr.startswith("swap letter"):
        # swap letter a with letter b
        a = parts[2]
        b = parts[5]
        pw = list(password)
        for i, ch in enumerate(pw):
            if ch == a:
                pw[i] = b
            elif ch == b:
                pw[i] = a
        return "".join(pw)

    if instr.startswith("rotate left"):
        # rotate left X steps
        steps = int(parts[2])
        return _rotate_left(password, steps)

    if instr.startswith("rotate right"):
        # rotate right X steps
        steps = int(parts[2])
        return _rotate_right(password, steps)

    if instr.startswith("rotate based on position of letter"):
        # rotate based on position of letter X
        letter = parts[-1]
        idx = password.index(letter)
        steps = 1 + idx
        if idx >= 4:
            steps += 1
        return _rotate_right(password, steps)

    if instr.startswith("reverse positions"):
        # reverse positions X through Y
        x = int(parts[2])
        y = int(parts[4])
        if x > y:
            x, y = y, x
        return password[:x] + password[x:y+1][::-1] + password[y+1:]

    if instr.startswith("move position"):
        # move position X to position Y
        x = int(parts[2])
        y = int(parts[5])
        pw = list(password)
        ch = pw.pop(x)
        pw.insert(y, ch)
        return "".join(pw)

    raise ValueError(f"Unknown instruction: {instr!r}")


# ---------- Обратные операции (Part 2) ----------

def _apply_instruction_inverse(password: str, instr: str) -> str:
    """
    Применяет ОБРАТНУЮ операцию для одной инструкции.
    То есть такое преобразование, которое делает "undo".
    """
    parts = instr.split()

    if instr.startswith("swap position"):
        # swap position X with position Y — операция сама себе обратная
        x = int(parts[2])
        y = int(parts[5])
        pw = list(password)
        pw[x], pw[y] = pw[y], pw[x]
        return "".join(pw)

    if instr.startswith("swap letter"):
        # swap letter a with letter b — тоже обратима сама к себе
        a = parts[2]
        b = parts[5]
        pw = list(password)
        for i, ch in enumerate(pw):
            if ch == a:
                pw[i] = b
            elif ch == b:
                pw[i] = a
        return "".join(pw)

    if instr.startswith("rotate left"):
        # Прямая: rotate left X
        # Обратная: rotate right X
        steps = int(parts[2])
        return _rotate_right(password, steps)

    if instr.startswith("rotate right"):
        # Прямая: rotate right X
        # Обратная: rotate left X
        steps = int(parts[2])
        return _rotate_left(password, steps)

    if instr.startswith("rotate based on position of letter"):
        # Это самая хитрая обратка.
        # Прямая: rotate based on position of letter X.
        # Обратная: ищем такую строку before, что после прямой операции
        #           получим текущий password.
        letter = parts[-1]

        # brute-force: перебираем все возможные "предыдущие" строки,
        # которые могли привести к текущей.
        for k in range(len(password)):
            candidate = _rotate_left(password, k)
            # candidate -> apply forward; если получается password, значит это он.
            if _apply_instruction(candidate, instr) == password:
                return candidate

        raise RuntimeError("Inverse of rotate-based not found (unexpected)")

    if instr.startswith("reverse positions"):
        # reverse positions X through Y — сама себе обратная
        x = int(parts[2])
        y = int(parts[4])
        if x > y:
            x, y = y, x
        return password[:x] + password[x:y+1][::-1] + password[y+1:]

    if instr.startswith("move position"):
        # Прямая: move position X to position Y
        # Обратная: move position Y to position X
        x = int(parts[2])
        y = int(parts[5])
        # В обратном направлении меняем X и Y местами
        pw = list(password)
        ch = pw.pop(y)
        pw.insert(x, ch)
        return "".join(pw)

    raise ValueError(f"Unknown instruction: {instr!r}")


# ---------- Решения частей ----------

def solve_part1(data: str) -> str:
    """
    Part 1:
    Стартовый пароль: 'abcdefgh'.
    Применяем все инструкции последовательно, возвращаем итоговый пароль.
    """
    instructions = _parse_instructions(data)
    password = "abcdefgh"
    for instr in instructions:
        password = _apply_instruction(password, instr)
    return password


def solve_part2(data: str) -> str:
    """
    Part 2:
    Известен итоговый (перемешанный) пароль: 'fbgdceah'.
    Нужно найти исходный пароль:
      - идём по инструкциям в ОБРАТНОМ порядке,
      - для каждой применяем ОБРАТНУЮ операцию.
    """
    instructions = _parse_instructions(data)
    password = "fbgdceah"
    for instr in reversed(instructions):
        password = _apply_instruction_inverse(password, instr)
    return password


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
