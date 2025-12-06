import re
from pathlib import Path
from typing import Dict, List, Tuple


def build_sleep_table(data: str) -> Dict[int, List[int]]:
    """
    Строит таблицу сна:
    { guard_id: [60 значений, сколько раз он спал в каждую минуту 0-59] }
    """
    # 1) убираем пустые строки и сортируем лог
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    lines.sort()

    # Регекс для получения минут и текста события
    line_re = re.compile(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)")
    guard_re = re.compile(r"#(\d+)")

    sleep_table: Dict[int, List[int]] = {}
    current_guard: int | None = None
    sleep_start: int | None = None

    for line in lines:
        m = line_re.match(line)
        if not m:
            continue

        minute = int(m.group(5))
        action = m.group(6)

        if "Guard #" in action:
            gm = guard_re.search(action)
            if gm:
                current_guard = int(gm.group(1))
                if current_guard not in sleep_table:
                    sleep_table[current_guard] = [0] * 60
            sleep_start = None
        elif action == "falls asleep":
            sleep_start = minute
        elif action == "wakes up":
            if current_guard is None or sleep_start is None:
                continue
            # отмечаем все минуты сна
            minutes_arr = sleep_table.setdefault(current_guard, [0] * 60)
            for mm in range(sleep_start, minute):
                minutes_arr[mm] += 1
            sleep_start = None

    return sleep_table


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    sleep_table = build_sleep_table(data)

    if not sleep_table:
        return "0"

    # Находим охранника с максимальным суммарным временем сна
    best_guard = None
    best_total = -1

    for guard_id, minutes in sleep_table.items():
        total = sum(minutes)
        if total > best_total:
            best_total = total
            best_guard = guard_id

    if best_guard is None:
        return "0"

    # Для этого охранника ищем минуту, когда он чаще всего спал
    minutes = sleep_table[best_guard]
    best_minute = max(range(60), key=lambda m: minutes[m])
    answer = best_guard * best_minute
    return str(answer)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    sleep_table = build_sleep_table(data)

    if not sleep_table:
        return "0"

    best_guard = None
    best_minute = None
    best_count = -1

    # Ищем глобально максимальную (охранник, минута)
    for guard_id, minutes in sleep_table.items():
        for minute, count in enumerate(minutes):
            if count > best_count:
                best_count = count
                best_guard = guard_id
                best_minute = minute

    if best_guard is None or best_minute is None:
        return "0"

    answer = best_guard * best_minute
    return str(answer)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
