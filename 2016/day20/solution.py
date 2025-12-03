# Advent of Code 2016 - Day 20
# Firewall Rules
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — строки вида:
# 5-8
# 0-2
# 4-7
#
# Всегда работаем в диапазоне IP: 0..4294967295 (32-бит беззнаковый).

from pathlib import Path


MAX_IP = 4294967295


def _parse_ranges(data: str):
    """
    Парсит вход в список диапазонов [(start, end), ...],
    где start и end включительны.
    """
    ranges = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("-")
        if len(parts) != 2:
            raise ValueError(f"Неверный формат диапазона: {line!r}")
        start = int(parts[0])
        end = int(parts[1])
        if start > end:
            start, end = end, start
        ranges.append((start, end))
    return ranges


def _merge_ranges(ranges):
    """
    Сливает пересекающиеся и соприкасающиеся диапазоны.
    На входе список (start, end) в любом порядке.
    На выходе отсортированный по start список непересекающихся диапазонов.
    """
    if not ranges:
        return []

    ranges = sorted(ranges, key=lambda r: r[0])
    merged = []
    cur_start, cur_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= cur_end + 1:
            # пересекаются или соприкасаются -> расширяем текущий диапазон
            cur_end = max(cur_end, end)
        else:
            # разрыв -> фиксируем текущий и начинаем новый
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end

    merged.append((cur_start, cur_end))
    return merged


def solve_part1(data: str) -> int:
    """
    Part 1:
    Наименьший разрешённый IP (не попадающий ни в один заблокированный диапазон).
    Если такого нет — вернём -1 (теоретически для AoC не случается).
    """
    ranges = _parse_ranges(data)
    blocked = _merge_ranges(ranges)

    candidate = 0
    for start, end in blocked:
        if candidate < start:
            # нашли дырку: candidate не попадает ни в один диапазон
            return candidate
        if start <= candidate <= end:
            # candidate заблокирован -> перепрыгиваем за диапазон
            candidate = end + 1
            if candidate > MAX_IP:
                break

    # если вышли за все диапазоны, но не за пределы MAX_IP, это тоже валидный IP
    if candidate <= MAX_IP:
        return candidate

    return -1


def solve_part2(data: str) -> int:
    """
    Part 2:
    Общее количество разрешённых IP-адресов в диапазоне 0..MAX_IP.
    """
    ranges = _parse_ranges(data)
    blocked = _merge_ranges(ranges)

    allowed = 0
    current = 0

    for start, end in blocked:
        if current < start:
            # от current до start-1 — разрешённые адреса
            allowed += start - current
        # переходим за текущий блок
        current = max(current, end + 1)
        if current > MAX_IP:
            break

    # после последнего диапазона, если ещё остались адреса
    if current <= MAX_IP:
        allowed += MAX_IP + 1 - current

    return allowed


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
