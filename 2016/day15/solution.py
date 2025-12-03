# Advent of Code 2016 - Day 15
# Timing is Everything
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# Пример строки:
# Disc #1 has 5 positions; at time=0, it is at position 4.
# Disc #2 has 2 positions; at time=0, it is at position 1.

from pathlib import Path
import re


LINE_RE = re.compile(
    r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).?"
)


def _parse(data: str):
    """
    Парсим вход в список дисков.
    Возвращаем список кортежей (disc_index, positions, start_pos),
    где disc_index — как в строке (1, 2, 3, ...).
    """
    disks = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        m = LINE_RE.match(line)
        if not m:
            raise ValueError(f"Неверный формат строки: {line!r}")
        disc_idx, positions, start = m.groups()
        disks.append((int(disc_idx), int(positions), int(start)))
    return disks


def _find_earliest_time(disks):
    """
    Ищем минимальное t >= 0 такое, что для каждого диска:
      (start + t + disc_index) % positions == 0
    Простым перебором t.
    """
    t = 0
    while True:
        ok = True
        for disc_idx, positions, start in disks:
            if (start + t + disc_idx) % positions != 0:
                ok = False
                break
        if ok:
            return t
        t += 1


def solve_part1(data: str) -> int:
    """
    Part 1:
    Находим минимальное t для исходного набора дисков.
    """
    disks = _parse(data)
    return _find_earliest_time(disks)


def solve_part2(data: str) -> int:
    """
    Part 2:
    Добавляем новый диск:
      Disc #(N+1) has 11 positions; at time=0, it is at position 0.
    И ищем минимальное t.
    """
    disks = _parse(data)
    if not disks:
        return 0

    # номер нового диска = последний индекс + 1
    max_idx = max(d[0] for d in disks)
    disks.append((max_idx + 1, 11, 0))

    return _find_earliest_time(disks)


def main():
    # Локальный запуск: читаем input.txt из текущей папки
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
