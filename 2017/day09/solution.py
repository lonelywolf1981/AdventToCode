from pathlib import Path


def _process_stream(data: str) -> tuple[int, int]:
    """
    Общий разбор потока для обеих частей.

    Возвращает:
      (group_score, garbage_count)

    group_score   — сумма очков всех групп (Part 1).
    garbage_count — количество символов мусора (Part 2).
    """
    stream = data.strip()

    in_garbage = False
    skip_next = False
    depth = 0
    score = 0
    garbage_count = 0

    for ch in stream:
        if skip_next:
            # Этот символ отменён '!' — не обрабатываем вообще
            skip_next = False
            continue

        if ch == "!":
            # Отменяем следующий символ
            skip_next = True
            continue

        if in_garbage:
            if ch == ">":
                # Конец мусора
                in_garbage = False
            else:
                # Всё прочее внутри мусора считается символами мусора
                garbage_count += 1
            continue

        # Не в мусоре:
        if ch == "<":
            in_garbage = True
        elif ch == "{":
            depth += 1
            score += depth
        elif ch == "}":
            depth -= 1
        else:
            # Запятые и прочие символы вне мусора игнорируем
            pass

    return score, garbage_count


def solve_part1(data: str) -> int:
    """
    Day 9, Part 1:
    Сумма очков всех групп.
    """
    score, _ = _process_stream(data)
    return score


def solve_part2(data: str) -> int:
    """
    Day 9, Part 2:
    Количество символов мусора.
    """
    _, garbage_count = _process_stream(data)
    return garbage_count


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
