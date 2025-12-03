# Advent of Code 2016 - Day 14
# One-Time Pad
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — одна строка: salt.

from pathlib import Path
import hashlib
from functools import lru_cache


def _get_salt(data: str) -> str:
    """
    Берём первую непустую строку как salt.
    """
    for line in data.splitlines():
        line = line.strip()
        if line:
            return line
    raise ValueError("Salt not found in input")


def _md5_hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def _stretched_hash(s: str, count: int) -> str:
    """
    md5-растяжка: count раз подряд.
    count=1 -> обычный md5.
    """
    h = s
    for _ in range(count):
        h = _md5_hex(h)
    return h


def _find_triplet(h: str):
    """
    Находит первый символ, который встречается три раза подряд.
    Возвращает этот символ или None.
    """
    for i in range(len(h) - 2):
        if h[i] == h[i + 1] == h[i + 2]:
            return h[i]
    return None


def _has_quintuple(h: str, ch: str) -> bool:
    """
    Проверяет, есть ли в хэше пятёрка из символа ch.
    """
    target = ch * 5
    return target in h


def _find_64th_key_index(salt: str, stretch_rounds: int) -> int:
    """
    Общая логика для Part 1 и Part 2.
    stretch_rounds:
      - 1    для обычного md5 (part1)
      - 2017 для растянутого md5 (part2: 1 базовый + 2016 доп. раз)
    """

    @lru_cache(maxsize=None)
    def get_hash(i: int) -> str:
        base = f"{salt}{i}"
        if stretch_rounds == 1:
            return _md5_hex(base)
        else:
            # сначала обычный md5, затем stretch_rounds-1 раз по цепочке
            h = _md5_hex(base)
            for _ in range(stretch_rounds - 1):
                h = _md5_hex(h)
            return h

    keys_found = 0
    i = 0

    while True:
        h = get_hash(i)
        ch = _find_triplet(h)
        if ch is not None:
            # ищем quintuple этого же символа в следующих 1000 хэшей
            for j in range(i + 1, i + 1001):
                if _has_quintuple(get_hash(j), ch):
                    keys_found += 1
                    if keys_found == 64:
                        return i
                    break
        i += 1


def solve_part1(data: str) -> int:
    """
    Part 1:
    Обычный MD5 — найти индекс 64-го ключа.
    """
    salt = _get_salt(data)
    return _find_64th_key_index(salt, stretch_rounds=1)


def solve_part2(data: str) -> int:
    """
    Part 2:
    Растянутый MD5 (2017 итераций) — индекс 64-го ключа.
    """
    salt = _get_salt(data)
    # 1 базовый + 2016 дополнительных = 2017 вызовов md5
    return _find_64th_key_index(salt, stretch_rounds=2017)


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
