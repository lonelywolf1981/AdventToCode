def solve_part1(data: str) -> str:
    nice = 0

    for s in data.strip().splitlines():
        s = s.strip()
        if not s:
            continue

        # Условие 1: минимум 3 гласные
        vowels = sum(s.count(v) for v in "aeiou")
        if vowels < 3:
            continue

        # Условие 2: есть двойная буква
        if not any(s[i] == s[i + 1] for i in range(len(s) - 1)):
            continue

        # Условие 3: нет запрещенных подстрок
        if any(bad in s for bad in ("ab", "cd", "pq", "xy")):
            continue

        nice += 1

    return str(nice)


def solve_part2(data: str) -> str:
    nice = 0

    for s in data.strip().splitlines():
        s = s.strip()
        if not s:
            continue

        # Условие 1: пара, которая появляется хотя бы дважды без перекрытия
        has_pair = False
        pairs = {}
        for i in range(len(s) - 1):
            pair = s[i:i + 2]
            if pair in pairs:
                # Проверяем, что текущее вхождение не перекрывается с первым
                if i - pairs[pair] >= 2:
                    has_pair = True
                    break
            else:
                # ВАЖНО: запоминаем только первую позицию пары,
                # чтобы не потерять более раннее вхождение
                pairs[pair] = i

        if not has_pair:
            continue

        # Условие 2: буква, повторяющаяся через одну (xyx)
        has_repeat = any(s[i] == s[i + 2] for i in range(len(s) - 2))
        if not has_repeat:
            continue

        nice += 1

    return str(nice)


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
