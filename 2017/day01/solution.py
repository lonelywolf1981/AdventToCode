def solve_part1(s: str) -> int:
    """
    Day 1, Part 1:
    Сумма цифр, которые совпадают со следующей (список циклический).
    """
    s = s.strip()
    if not s:
        return 0

    total = 0
    n = len(s)

    for i, ch in enumerate(s):
        nxt = s[(i + 1) % n]  # следующая позиция по кругу
        if ch == nxt:
            total += int(ch)

    return total


def solve_part2(s: str) -> int:
    """
    Day 1, Part 2:
    Сумма цифр, которые совпадают с цифрой через половину длины списка.
    """
    s = s.strip()
    if not s:
        return 0

    total = 0
    n = len(s)
    step = n // 2  # половина длины

    for i, ch in enumerate(s):
        nxt = s[(i + step) % n]  # цифра через половину длины по кругу
        if ch == nxt:
            total += int(ch)

    return total


def read_input(path: str = "input.txt") -> str:
    """
    Читаем весь input как одну строку.
    Обычно в этой задаче в файле только одна строка с цифрами.
    """
    with open(path, encoding="utf-8") as f:
        # Берём первую непустую строку, содержащую цифры
        for line in f:
            line = line.strip()
            if line:
                return line
    return ""


if __name__ == "__main__":
    data = read_input("input.txt")
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
