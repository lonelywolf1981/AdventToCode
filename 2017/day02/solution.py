from pathlib import Path


def _parse_rows(data: str) -> list[list[int]]:
    """
    Преобразуем содержимое input.txt в таблицу чисел.
    Каждая непустая строка -> список int.
    """
    rows: list[list[int]] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        # split() сам порежет по любым пробелам/табам
        nums = [int(x) for x in line.split()]
        rows.append(nums)
    return rows


def solve_part1(data: str) -> int:
    """
    Day 2, Part 1:
    Для каждой строки: max(row) - min(row), затем суммируем.
    """
    rows = _parse_rows(data)
    total = 0
    for nums in rows:
        total += max(nums) - min(nums)
    return total


def solve_part2(data: str) -> int:
    """
    Day 2, Part 2:
    Для каждой строки найти единственную пару чисел,
    где одно делится на другое без остатка.
    Суммируем результаты деления по всем строкам.
    """
    rows = _parse_rows(data)
    total = 0

    for nums in rows:
        n = len(nums)
        found = False

        # Перебираем пары без повторов: (i, j), i < j
        for i in range(n):
            if found:
                break
            for j in range(i + 1, n):
                a = nums[i]
                b = nums[j]

                if a % b == 0:
                    total += a // b
                    found = True
                    break
                if b % a == 0:
                    total += b // a
                    found = True
                    break

    return total


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
