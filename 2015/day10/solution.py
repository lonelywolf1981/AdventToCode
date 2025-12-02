def look_and_say(s: str) -> str:
    if not s:
        return s

    res_chars = []
    current = s[0]
    count = 1

    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            # добавляем "count" + "current"
            res_chars.append(str(count))
            res_chars.append(current)
            current = ch
            count = 1

    # последняя группа
    res_chars.append(str(count))
    res_chars.append(current)

    return "".join(res_chars)


def solve_part1(data: str) -> str:
    s = data.strip()
    for _ in range(40):
        s = look_and_say(s)
    return str(len(s))


def solve_part2(data: str) -> str:
    s = data.strip()
    for _ in range(50):
        s = look_and_say(s)
    return str(len(s))


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
