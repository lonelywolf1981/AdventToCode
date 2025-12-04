from pathlib import Path


def _parse_input(data: str) -> list[int]:
    """
    Преобразуем содержимое input.txt в список целых чисел.
    Каждая непустая строка должна содержать одно целое число.
    """
    jumps: list[int] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        jumps.append(int(line))
    return jumps


def solve_part1(data: str) -> int:
    """
    Day 5, Part 1:
    Идём по списку смещений, каждый шаг:
      - берём offset по текущему индексу,
      - прыгаем на index + offset,
      - старый offset увеличиваем на 1,
      - считаем шаги, пока индекс не выйдет за пределы.
    Возвращаем количество шагов.
    """
    jumps = _parse_input(data)
    index = 0
    steps = 0
    n = len(jumps)

    while 0 <= index < n:
        offset = jumps[index]
        jumps[index] += 1  # правило Part 1
        index += offset
        steps += 1

    return steps


def solve_part2(data: str) -> int:
    """
    Day 5, Part 2:
    То же, но правило изменения offset:
      - если offset >= 3 -> offset -= 1
      - иначе           -> offset += 1
    """
    jumps = _parse_input(data)
    index = 0
    steps = 0
    n = len(jumps)

    while 0 <= index < n:
        offset = jumps[index]
        if offset >= 3:
            jumps[index] -= 1
        else:
            jumps[index] += 1
        index += offset
        steps += 1

    return steps


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
