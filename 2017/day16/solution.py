from pathlib import Path
from typing import List


def _parse_moves(data: str) -> List[str]:
    """
    Берём первую непустую строку и разбиваем по запятой
    в список команд танца.
    """
    line = ""
    for l in data.splitlines():
        l = l.strip()
        if l:
            line = l
            break

    if not line:
        return []

    return [m.strip() for m in line.split(",") if m.strip()]


def _dance_once(programs: List[str], moves: List[str]) -> List[str]:
    """
    Выполнить один полный проход танца над списком символов programs.
    Возвращает НОВЫЙ список (не модифицирует исходный).
    """
    arr = programs[:]  # копия

    for move in moves:
        mtype = move[0]

        if mtype == "s":
            # spin X
            x = int(move[1:])
            x %= len(arr)
            if x:
                arr = arr[-x:] + arr[:-x]

        elif mtype == "x":
            # exchange A/B (по индексам)
            a_str, b_str = move[1:].split("/")
            a = int(a_str)
            b = int(b_str)
            arr[a], arr[b] = arr[b], arr[a]

        elif mtype == "p":
            # partner A/B (по именам)
            name_a, name_b = move[1:].split("/")
            ia = arr.index(name_a)
            ib = arr.index(name_b)
            arr[ia], arr[ib] = arr[ib], arr[ia]

        else:
            raise ValueError(f"Неизвестная команда танца: {move!r}")

    return arr


def solve_part1(data: str) -> str:
    """
    Day 16, Part 1:
    Один проход танца над 'abcdefghijklmnop'.
    Возвращаем итоговую строку.
    """
    moves = _parse_moves(data)
    programs = list("abcdefghijklmnop")
    result = _dance_once(programs, moves)
    return "".join(result)


def solve_part2(data: str) -> str:
    """
    Day 16, Part 2:
    Повторяем тот же танец 1_000_000_000 раз,
    используя обнаружение цикла.
    """
    moves = _parse_moves(data)
    start = "abcdefghijklmnop"

    seen: List[str] = [start]
    current = start

    while True:
        current = "".join(_dance_once(list(current), moves))
        if current in seen:
            # Нашли цикл
            cycle_start = seen.index(current)
            cycle_len = len(seen) - cycle_start

            total = 1_000_000_000
            # Поскольку до cycle_start все уникальные, а дальше цикл:
            # нам нужна позиция внутри цикла.
            if total < len(seen):
                return seen[total]

            # Сдвигаемся от начала цикла
            offset = (total - cycle_start) % cycle_len
            answer = seen[cycle_start + offset]
            return answer
        else:
            seen.append(current)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
