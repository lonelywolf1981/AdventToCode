# Advent of Code 2016 - Day 10
# Balance Bots
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — строки вида:
# value 5 goes to bot 2
# bot 2 gives low to bot 1 and high to output 0
# ...

from pathlib import Path
import re
from collections import defaultdict
from math import prod


# Целевые значения для сравнения в Part 1
TARGET_LOW = 17
TARGET_HIGH = 61


VALUE_RE = re.compile(r"^value (\d+) goes to bot (\d+)$")
RULE_RE = re.compile(
    r"^bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)$"
)


def _parse_instructions(data: str):
    """
    Возвращает:
      - initial_chips: dict[bot_id] -> list[int]
      - rules: dict[bot_id] -> (low_type, low_id, high_type, high_id)
        где type = 'bot' или 'output'
    """
    initial_chips = defaultdict(list)
    rules = {}

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        m_val = VALUE_RE.match(line)
        if m_val:
            value, bot_id = m_val.groups()
            value = int(value)
            bot_id = int(bot_id)
            initial_chips[bot_id].append(value)
            continue

        m_rule = RULE_RE.match(line)
        if m_rule:
            (
                bot_id,
                low_type,
                low_id,
                high_type,
                high_id,
            ) = m_rule.groups()
            bot_id = int(bot_id)
            low_id = int(low_id)
            high_id = int(high_id)
            rules[bot_id] = (low_type, low_id, high_type, high_id)
            continue

        # Если строка не подошла ни под один формат — считаем это ошибкой
        raise ValueError(f"Неизвестный формат строки: {line!r}")

    return initial_chips, rules


def _run_simulation(data: str):
    """
    Запускает полную симуляцию раздачи чипов.
    Возвращает:
      - comparer_bot: int | None — бот, сравнивший TARGET_LOW и TARGET_HIGH
      - outputs: dict[output_id] -> list[int]
    """
    bot_chips, rules = _parse_instructions(data)

    outputs = defaultdict(list)
    comparer_bot = None

    # крутим, пока есть боты с 2+ чипами, по которым есть правила
    while True:
        progress = False

        # список, чтобы не менять словарь во время итерации
        bots_ready = [
            bot_id
            for bot_id, chips in bot_chips.items()
            if len(chips) >= 2 and bot_id in rules
        ]

        if not bots_ready:
            break

        for bot_id in bots_ready:
            chips = bot_chips[bot_id]
            if len(chips) < 2:
                continue  # на всякий случай

            # берём два минимальных (в AoC гарантируется ровно 2)
            low_val, high_val = sorted(chips[:2])
            # очищаем выданные чипы
            bot_chips[bot_id] = chips[2:]

            # проверка на «того самого» бота
            if (
                low_val == TARGET_LOW
                and high_val == TARGET_HIGH
                and comparer_bot is None
            ):
                comparer_bot = bot_id

            low_type, low_id, high_type, high_id = rules[bot_id]

            # отдаём низкий чип
            if low_type == "bot":
                bot_chips[low_id].append(low_val)
            else:  # output
                outputs[low_id].append(low_val)

            # отдаём высокий чип
            if high_type == "bot":
                bot_chips[high_id].append(high_val)
            else:  # output
                outputs[high_id].append(high_val)

            progress = True

        if not progress:
            break

    return comparer_bot, outputs


def solve_part1(data: str) -> int:
    """
    Part 1:
    Номер бота, который сравнил чипы TARGET_LOW и TARGET_HIGH.
    Если не найден — возвращаем -1.
    """
    comparer_bot, _ = _run_simulation(data)
    return comparer_bot if comparer_bot is not None else -1


def solve_part2(data: str) -> int:
    """
    Part 2:
    Произведение значений в выходах 0, 1 и 2.
    Если один из выходов пуст — считаем для него значение 1.
    (в нормальном AoC-входе там будет по одному значению).
    """
    _, outputs = _run_simulation(data)

    # берём первый чип из каждого выхода, если есть
    values = []
    for out_id in (0, 1, 2):
        if outputs[out_id]:
            values.append(outputs[out_id][0])
        else:
            values.append(1)  # безопасное значение, если вдруг пусто

    return prod(values)


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
