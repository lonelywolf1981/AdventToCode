def solve_part1(data: str) -> str:
    total = 0

    for line in data.splitlines():
        digits = [ch for ch in line if ch.isdigit()]
        if digits:
            total += int(digits[0] + digits[-1])

    return str(total)


def solve_part2(data: str) -> str:
    words = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    total = 0

    for line in data.splitlines():
        found = []

        i = 0
        while i < len(line):
            ch = line[i]

            # Если цифра — просто записываем
            if ch.isdigit():
                found.append(ch)
            else:
                # Проверяем все словесные варианты
                for w, d in words.items():
                    if line.startswith(w, i):
                        found.append(d)
                        # ВАЖНО! Не пропускаем символы — могут быть оверлап
                        # т.е. i += 1 — НЕЛЬЗЯ
                        break

            i += 1

        if found:
            total += int(found[0] + found[-1])

    return str(total)
