# Advent of Code 2016 - Day 4
# Security Through Obscurity
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — строки вида:
# aaaaa-bbb-z-y-x-123[abxyz]

from pathlib import Path
import re
from collections import Counter


LINE_RE = re.compile(r"^([a-z\-]+)-(\d+)\[([a-z]+)\]$")


def _parse_input(data: str):
    """
    Возвращает список кортежей:
      (name_with_dashes: str, sector_id: int, checksum: str)
    """
    rooms = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        m = LINE_RE.match(line)
        if not m:
            raise ValueError(f"Неверный формат строки: {line!r}")
        name, sector_str, checksum = m.groups()
        rooms.append((name, int(sector_str), checksum))
    return rooms


def _compute_checksum(name: str) -> str:
    """
    Считает «правильный» checksum по правилам AoC:
    - учитываем только буквы, без '-';
    - сортируем по частоте (убывание), при равенстве — по алфавиту;
    - берем первые 5.
    """
    letters = name.replace("-", "")
    counts = Counter(letters)

    # сортировка: сначала по -count (убывание), затем по букве (возрастание)
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return "".join(ch for ch, _ in ordered[:5])


def _is_real_room(name: str, checksum: str) -> bool:
    return _compute_checksum(name) == checksum


def _decrypt_name(name: str, sector_id: int) -> str:
    """
    Сдвиг каждой буквы на sector_id по алфавиту, '-' -> пробел.
    """
    shift = sector_id % 26
    res_chars = []
    for ch in name:
        if ch == "-":
            res_chars.append(" ")
        elif "a" <= ch <= "z":
            new_pos = (ord(ch) - ord("a") + shift) % 26
            res_chars.append(chr(ord("a") + new_pos))
        else:
            # на всякий случай просто добавим как есть
            res_chars.append(ch)
    return "".join(res_chars)


def solve_part1(data: str) -> int:
    """
    Сумма sector ID всех реальных комнат.
    """
    rooms = _parse_input(data)
    total = 0
    for name, sector_id, checksum in rooms:
        if _is_real_room(name, checksum):
            total += sector_id
    return total


def solve_part2(data: str) -> int:
    """
    Находим реальную комнату, в расшифрованном имени которой есть 'northpole'.
    Возвращаем её sector ID.
    Если ничего не нашли — возвращаем -1.
    """
    rooms = _parse_input(data)

    for name, sector_id, checksum in rooms:
        if not _is_real_room(name, checksum):
            continue
        decrypted = _decrypt_name(name, sector_id)
        if "northpole" in decrypted.lower():
            return sector_id

    # если по какой-то причине не нашли — вернём -1
    return -1


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

