from functools import lru_cache


def parse(data: str) -> list[int]:
    """
    Вход: одна строка чисел через пробел.
    Пример: "125 17"
    """
    return [int(x) for x in data.split() if x.strip()]


@lru_cache(maxsize=None)
def count_stones(value: int, steps: int) -> int:
    """
    Сколько камней будет из одного камня со значением `value`
    после `steps` мигов.
    """
    if steps == 0:
        # шагов больше нет — это один камень
        return 1

    # Правило 1: 0 -> 1
    if value == 0:
        return count_stones(1, steps - 1)

    s = str(value)

    # Правило 2: чётное число цифр — разделение на два камня
    if len(s) % 2 == 0:
        mid = len(s) // 2
        left = int(s[:mid])   # int уберёт ведущие нули
        right = int(s[mid:])
        return (
            count_stones(left, steps - 1)
            + count_stones(right, steps - 1)
        )

    # Правило 3: иначе умножаем на 2024
    return count_stones(value * 2024, steps - 1)


def solve_part1(data: str) -> str:
    # Day 11 Part 1:
    # Посчитать количество камней после 25 мигов.
    stones = parse(data)
    total = sum(count_stones(v, 25) for v in stones)
    return str(total)


def solve_part2(data: str) -> str:
    # Day 11 Part 2:
    # То же, но 75 мигов.
    stones = parse(data)
    total = sum(count_stones(v, 75) for v in stones)
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
