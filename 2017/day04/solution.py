from pathlib import Path


def _parse_lines(data: str) -> list[list[str]]:
    """
    Преобразуем содержимое input.txt в список passphrase:
    каждая непустая строка -> список слов (строк без пробелов).
    """
    phrases: list[list[str]] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        words = line.split()
        phrases.append(words)
    return phrases


def solve_part1(data: str) -> int:
    """
    Day 4, Part 1:
    Считаем количество passphrase, в которых нет повторяющихся слов.
    """
    phrases = _parse_lines(data)
    valid_count = 0

    for words in phrases:
        # Если размер множества равен длине списка — повторов нет
        if len(set(words)) == len(words):
            valid_count += 1

    return valid_count


def solve_part2(data: str) -> int:
    """
    Day 4, Part 2:
    Считаем количество passphrase, в которых:
    - нет повторяющихся слов;
    - нет слов, являющихся анаграммами друг друга.
    Для проверки анаграмм нормализуем каждое слово сортировкой букв.
    """
    phrases = _parse_lines(data)
    valid_count = 0

    for words in phrases:
        # Нормализуем слова: сортируем буквы в каждом слове
        normalized = ["".join(sorted(w)) for w in words]
        if len(set(normalized)) == len(normalized):
            valid_count += 1

    return valid_count


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
