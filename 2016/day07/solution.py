# Advent of Code 2016 - Day 7
# Internet Protocol Version 7
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# В файле input.txt — строки вида:
# abba[mnop]qrst

from pathlib import Path


def _parse_line(line: str):
    """
    Разбирает строку IP-адреса на два списка:
      supernets: части вне []
      hypernets: части внутри []
    Всегда начинаем с supernet (возможно пустого).
    """
    supernets = []
    hypernets = []

    current = []
    in_brackets = False

    for ch in line:
        if ch == '[':
            # закрываем текущий сегмент
            segment = "".join(current)
            if in_brackets:
                hypernets.append(segment)
            else:
                supernets.append(segment)
            current = []
            in_brackets = True
        elif ch == ']':
            segment = "".join(current)
            if in_brackets:
                hypernets.append(segment)
            else:
                supernets.append(segment)
            current = []
            in_brackets = False
        else:
            current.append(ch)

    # хвост
    if current:
        segment = "".join(current)
        if in_brackets:
            hypernets.append(segment)
        else:
            supernets.append(segment)

    return supernets, hypernets


def _has_abba(s: str) -> bool:
    """
    Проверяет, есть ли в строке шаблон ABBA:
      - длина 4,
      - s[0] != s[1],
      - s[0:4] == s[3: -1: -1] грубо говоря 'xyyx'.
    """
    for i in range(len(s) - 3):
        a, b, c, d = s[i:i+4]
        if a != b and a == d and b == c:
            return True
    return False


def _supports_tls(supernets, hypernets) -> bool:
    """
    TLS:
      - хотя бы один ABBA во внешних частях
      - ни одного ABBA во внутренних.
    """
    return any(_has_abba(s) for s in supernets) and not any(
        _has_abba(h) for h in hypernets
    )


def _find_abas(s: str):
    """
    Генерирует все ABA в строке как пары (a, b),
    соответствующие шаблону a b a, где a != b.
    """
    for i in range(len(s) - 2):
        a, b, c = s[i:i+3]
        if a == c and a != b:
            yield a, b


def _supports_ssl(supernets, hypernets) -> bool:
    """
    SSL:
      - ищем все ABA во внешних частях (supernets)
      - строим для них все возможные BAB
      - если какой-либо BAB встречается в любой hypernet-части -> True
    """
    abas = set()
    for s in supernets:
        for a, b in _find_abas(s):
            abas.add((a, b))

    if not abas:
        return False

    # строим все BAB для найденных ABA
    babs = {b + a + b for a, b in abas}

    for h in hypernets:
        if any(bab in h for bab in babs):
            return True

    return False


def solve_part1(data: str) -> int:
    """
    Считает количество IP, поддерживающих TLS.
    """
    count = 0
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        supernets, hypernets = _parse_line(line)
        if _supports_tls(supernets, hypernets):
            count += 1
    return count


def solve_part2(data: str) -> int:
    """
    Считает количество IP, поддерживающих SSL.
    """
    count = 0
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        supernets, hypernets = _parse_line(line)
        if _supports_ssl(supernets, hypernets):
            count += 1
    return count


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

