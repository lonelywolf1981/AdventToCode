# Advent of Code 2016 - Day 5
# How About a Nice Game of Chess?
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> str
#   solve_part2(raw_input: str) -> str
#
# В файле input.txt — одна строка: door ID.

from pathlib import Path
import hashlib


def _get_door_id(data: str) -> str:
    """
    Берём первую непустую строку как door ID.
    """
    for line in data.splitlines():
        line = line.strip()
        if line:
            return line
    raise ValueError("Door ID not found in input")


def solve_part1(data: str) -> str:
    """
    Part 1:
    Ищем хэши MD5(door_id + i), начинающиеся с '00000'.
    Собираем пароль из 8 символов: берем 6-й символ (hash[5]) каждого подходящего хэша.
    Возвращаем пароль в виде строки.
    """
    door_id = _get_door_id(data)

    password_chars = []
    i = 0

    while len(password_chars) < 8:
        to_hash = f"{door_id}{i}".encode("utf-8")
        h = hashlib.md5(to_hash).hexdigest()
        if h.startswith("00000"):
            password_chars.append(h[5])
        i += 1

    return "".join(password_chars)


def solve_part2(data: str) -> str:
    """
    Part 2:
    Всё то же, но:
      - hash[5] -> позиция (0-7),
      - hash[6] -> символ пароля.
    Заполняем каждую позицию только один раз.
    Возвращаем пароль в виде строки.
    """
    door_id = _get_door_id(data)

    password = ["_"] * 8   # временно заполняем плейсхолдерами
    filled = 0
    i = 0

    while filled < 8:
        to_hash = f"{door_id}{i}".encode("utf-8")
        h = hashlib.md5(to_hash).hexdigest()

        if h.startswith("00000"):
            pos_char = h[5]
            if pos_char.isdigit():
                pos = int(pos_char)
                if 0 <= pos <= 7 and password[pos] == "_":
                    password[pos] = h[6]
                    filled += 1
        i += 1

    return "".join(password)


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
