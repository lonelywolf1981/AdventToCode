def solve_part1(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        s = line.strip()
        if not s:
            continue

        # Количество символов в коде (включая кавычки и экранирование)
        code_len = len(s)

        # Считаем количество символов в памяти, разбирая строку вручную
        i = 0
        mem_len = 0

        # Пропускаем первые и последние кавычки
        s_inner = s[1:-1]

        while i < len(s_inner):
            if s_inner[i] == "\\":
                # Экранирование
                if s_inner[i:i+2] in ("\\\\", "\\\""):
                    mem_len += 1
                    i += 2
                elif s_inner[i:i+2] == "\\x" and i + 3 < len(s_inner):
                    # \xAB — один символ в памяти
                    mem_len += 1
                    i += 4
                else:
                    # На всякий случай, если встретится что-то нестандартное
                    mem_len += 1
                    i += 2
            else:
                mem_len += 1
                i += 1

        total += code_len - mem_len

    return str(total)


def solve_part2(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        s = line.strip()
        if not s:
            continue

        # При повторном кодировании:
        # - добавятся 2 внешние кавычки
        # - каждый '\' превратится в '\\' => +1 символ на каждый '\'
        # - каждый '"' превратится в '\"' => +1 символ на каждый '"'
        extra = 2  # новые внешние кавычки
        extra += s.count("\\")
        extra += s.count("\"")

        total += extra

    return str(total)


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
