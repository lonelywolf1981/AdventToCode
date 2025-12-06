from pathlib import Path
from typing import List


def parse_number(data: str) -> int:
    """
    Парсим число из input.txt (обычно там просто 2018 или 890691).
    Берём первые подряд идущие цифры.
    """
    data = data.strip()
    digits = []
    for ch in data:
        if ch.isdigit():
            digits.append(ch)
    if not digits:
        return 0
    return int("".join(digits))


def make_scores_until(count: int) -> List[int]:
    """
    Строим список рецептов, пока длина не станет >= count.
    Возвращаем весь список.
    """
    scores = [3, 7]
    elf1 = 0
    elf2 = 1

    while len(scores) < count:
        s = scores[elf1] + scores[elf2]
        if s >= 10:
            scores.append(s // 10)
            scores.append(s % 10)
        else:
            scores.append(s)

        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

    return scores


def find_pattern(pattern: List[int]) -> int:
    """
    Ищем первую позицию, где в ленте рецептов встречается последовательность pattern.
    Возвращаем индекс (считая от 0).
    """
    scores = [3, 7]
    elf1 = 0
    elf2 = 1

    L = len(pattern)

    # Проверяем на каждом шаге только два возможных места:
    # - окончание списка (последние L)
    # - и сдвиг на 1 (последние L, начиная с len-1-L)
    while True:
        s = scores[elf1] + scores[elf2]

        # Добавляем первую цифру
        if s >= 10:
            scores.append(s // 10)
            # проверяем варианты
            if len(scores) >= L and scores[-L:] == pattern:
                return len(scores) - L
            if len(scores) > L and scores[-L-1:-1] == pattern:
                return len(scores) - L - 1

            # добавляем вторую цифру
            scores.append(s % 10)
            if len(scores) >= L and scores[-L:] == pattern:
                return len(scores) - L
        else:
            scores.append(s)
            if len(scores) >= L and scores[-L:] == pattern:
                return len(scores) - L

        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    n = parse_number(data)
    if n <= 0:
        return ""

    scores = make_scores_until(n + 10)
    tail = scores[n:n + 10]
    return "".join(str(d) for d in tail)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    data = data.strip()
    # шаблон — это последовательность цифр из входа
    pattern_digits = [int(ch) for ch in data if ch.isdigit()]
    if not pattern_digits:
        return "0"

    pos = find_pattern(pattern_digits)
    return str(pos)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
