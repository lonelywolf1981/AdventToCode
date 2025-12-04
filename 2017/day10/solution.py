from pathlib import Path
from typing import List


def _parse_lengths_part1(data: str) -> List[int]:
    """
    Для Part 1: берём первую непустую строку и парсим из неё числа,
    разделённые запятыми/пробелами.
    """
    line = ""
    for l in data.splitlines():
        l = l.strip()
        if l:
            line = l
            break

    if not line:
        raise ValueError("Пустой input для Day 10")

    # "34, 88, 2" -> [34, 88, 2]
    parts = line.replace(",", " ").split()
    return [int(x) for x in parts]


def _single_round(
    nums: List[int],
    lengths: List[int],
    current_pos: int = 0,
    skip_size: int = 0,
) -> tuple[int, int]:
    """
    Выполняет один "раунд" алгоритма Knot Hash над nums.
    Возвращает (новая_позиция, новый_skip_size).
    """
    n = len(nums)

    for length in lengths:
        if length > n:
            # В классической задаче такого нет, но на всякий случай
            continue

        # Собираем индексы отрезка по кругу
        indices = [(current_pos + i) % n for i in range(length)]
        # Берём значения, разворачиваем
        values = [nums[i] for i in indices][::-1]
        # Записываем обратно
        for idx, val in zip(indices, values):
            nums[idx] = val

        # Обновляем позицию и skip
        current_pos = (current_pos + length + skip_size) % n
        skip_size += 1

    return current_pos, skip_size


def _knot_hash_full(input_line: str) -> str:
    """
    Полный Knot Hash (Part 2):
    - длины = ASCII-коды символов + стандартный суффикс [17,31,73,47,23]
    - 64 раунда
    - dense hash из 16 блоков по 16 чисел (XOR)
    - hex-строка длиной 32 символа
    """
    # Важно: НЕ обрезаем пробелы в начале/конце строки;
    # используем ровно то, что в строке до \n.
    lengths = [ord(c) for c in input_line] + [17, 31, 73, 47, 23]

    nums = list(range(256))
    current_pos = 0
    skip_size = 0

    for _ in range(64):
        current_pos, skip_size = _single_round(nums, lengths, current_pos, skip_size)

    # dense hash: XOR по блокам по 16 чисел
    dense: List[int] = []
    for block_start in range(0, 256, 16):
        x = 0
        for i in range(block_start, block_start + 16):
            x ^= nums[i]
        dense.append(x)

    # в hex-строку
    return "".join(f"{b:02x}" for b in dense)


def solve_part1(data: str) -> int:
    """
    Day 10, Part 1:
    Один раунд алгоритма Knot Hash по длинам из input,
    вернуть nums[0] * nums[1].
    """
    lengths = _parse_lengths_part1(data)
    nums = list(range(256))

    _single_round(nums, lengths)  # позиция и skip нам в Part 1 не нужны
    return nums[0] * nums[1]


def solve_part2(data: str) -> str:
    """
    Day 10, Part 2:
    Полный Knot Hash.
    Возвращаем 32-символьную hex-строку.
    """
    # Берём первую строку input без завершающего \n, но не трогаем пробелы.
    lines = data.splitlines()
    if lines:
        # убираем только \r/\n, но не strip() пробелов
        # splitlines уже отрезал \n, остаётся сама строка
        input_line = lines[0]
    else:
        input_line = ""

    return _knot_hash_full(input_line)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
