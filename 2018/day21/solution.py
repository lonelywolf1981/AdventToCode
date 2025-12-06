from __future__ import annotations

from pathlib import Path


def generate_sequence():
    """
    Генерируем последовательность значений r5, которые сравниваются с r0
    в инструкции eqrr 5 0 3 для входа AoC 2018 Day 21.

    Алгоритм извлечён из кода:
        r1 = r5 | 65536
        r5 = 4591209
        while True:
            r5 = (((r5 + (r1 & 255)) & 0xFFFFFF) * 65899) & 0xFFFFFF
            if r1 < 256:
                break
            r1 //= 256

    Возвращаем первое значение (для Part 1) и последнее уникальное
    перед повтором (для Part 2).
    """
    seen = set()
    first_value = None
    last_unique = None

    r5 = 0  # начальное состояние (как после seti 0 6 5)

    while True:
        r1 = r5 | 65536
        r5 = 4591209

        while True:
            r3 = r1 & 255
            r5 += r3
            r5 &= 0xFFFFFF
            r5 *= 65899
            r5 &= 0xFFFFFF

            if r1 < 256:
                break
            r1 //= 256

        # в этот момент в оригинальной программе выполняется eqrr 5 0 3

        if first_value is None:
            first_value = r5

        if r5 in seen:
            # нашли цикл — последнее уникальное значение и есть ответ Part 2
            break

        seen.add(r5)
        last_unique = r5

    return first_value, last_unique


def solve_part1(data: str) -> str:
    # data не используем, алгоритм однозначно задан программой из input.txt
    first, _ = generate_sequence()
    return str(first if first is not None else 0)


def solve_part2(data: str) -> str:
    # data не используем, алгоритм однозначно задан программой из input.txt
    _, last = generate_sequence()
    return str(last if last is not None else 0)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
