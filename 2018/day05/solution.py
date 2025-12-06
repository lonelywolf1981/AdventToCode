from pathlib import Path


def parse_input(data: str) -> str:
    """
    Берём полимер как одну строку:
    - убираем лишние пустые строки
    - склеиваем, если почему-то несколько строк
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""
    if len(lines) == 1:
        return lines[0]
    # На всякий случай, если кто-то перенёс полимер на несколько строк
    return "".join(lines)


def react_polymer(polymer: str) -> str:
    """
    Выполняет полную реакцию полимера.
    Идея: идём по символам и используем стек.
    Если текущий символ и верх стека одной буквы, но разного регистра — убираем пару.
    Иначе кладём символ в стек.
    """
    stack: list[str] = []

    for ch in polymer:
        if stack:
            top = stack[-1]
            # проверка "одинаковая буква, разный регистр":
            # в ASCII разница между 'a' и 'A' = 32
            if abs(ord(ch) - ord(top)) == 32:
                stack.pop()
                continue
        stack.append(ch)

    return "".join(stack)


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    polymer = parse_input(data)
    reacted = react_polymer(polymer)
    return str(len(reacted))


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    polymer = parse_input(data)
    if not polymer:
        return "0"

    base_polymer = polymer
    best = None

    for unit in "abcdefghijklmnopqrstuvwxyz":
        # выкидываем оба регистра этой буквы
        filtered = [
            ch
            for ch in base_polymer
            if ch.lower() != unit
        ]
        reacted = react_polymer("".join(filtered))
        length = len(reacted)

        if best is None or length < best:
            best = length

    return str(best if best is not None else 0)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
