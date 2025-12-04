from pathlib import Path


def _parse_step(data: str) -> int:
    """
    Вход — одно число (step size), возможно с переводами строк.
    Берём первую непустую строку и парсим как int.
    """
    for line in data.splitlines():
        line = line.strip()
        if line:
            return int(line)
    raise ValueError("Пустой input для Day 17")


def solve_part1(data: str) -> int:
    """
    Day 17, Part 1:
    Классическая симуляция spinlock:
    - step из input
    - вставляем числа 1..2017
    - возвращаем значение, стоящее сразу ПОСЛЕ 2017 в буфере.
    """
    step = _parse_step(data)

    buffer = [0]
    pos = 0

    for value in range(1, 2017 + 1):
        pos = (pos + step) % len(buffer)
        pos += 1
        buffer.insert(pos, value)

    # Находим индекс 2017 и смотрим, что после него
    idx = buffer.index(2017)
    return buffer[(idx + 1) % len(buffer)]


def solve_part2(data: str) -> int:
    """
    Day 17, Part 2:
    Вставляем 1..50_000_000, но буфер не строим полностью.
    Нас интересует только число, которое оказывается сразу после 0.
    0 всегда в позиции 0, поэтому:
      - следим за текущим size (длина буфера),
      - считаем позицию вставки,
      - если вставка идёт в позицию 1 -> обновляем ответ.
    """
    step = _parse_step(data)

    pos = 0
    size = 1  # в буфере изначально только [0]
    value_after_zero = 0  # запасной, если вдруг ни разу не вставим после 0

    for value in range(1, 50_000_000 + 1):
        pos = (pos + step) % size
        insert_pos = pos + 1

        if insert_pos == 1:
            # Новое значение встаёт сразу после 0 (который в позиции 0)
            value_after_zero = value

        pos = insert_pos
        size += 1

    return value_after_zero


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
