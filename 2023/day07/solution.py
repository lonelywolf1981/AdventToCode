from pathlib import Path
from collections import Counter


# -----------------------------
#  Вспомогалки
# -----------------------------

CARD_ORDER_1 = {c: i for i, c in enumerate("23456789TJQKA")}
# Для части 2 J — самая слабая карта
CARD_ORDER_2 = {c: i for i, c in enumerate("J23456789TQKA")}


def hand_type_part1(hand: str) -> tuple:
    """
    Определяем тип руки (без джокеров).
    Возвращает кортеж, который можно использовать в сортировке.
    Чем больше число — тем сильнее комбинация.
      6 — пять одинаковых
      5 — каре
      4 — фулл-хаус
      3 — сет
      2 — две пары
      1 — одна пара
      0 — все разные
    """
    cnt = Counter(hand)
    counts = sorted(cnt.values(), reverse=True)

    if counts == [5]:
        return (6,)
    if counts == [4, 1]:
        return (5,)
    if counts == [3, 2]:
        return (4,)
    if counts == [3, 1, 1]:
        return (3,)
    if counts == [2, 2, 1]:
        return (2,)
    if counts == [2, 1, 1, 1]:
        return (1,)
    return (0,)


def hand_type_part2(hand: str) -> tuple:
    """
    Тип руки с джокером J.
    J можно превратить в любой ранг так, чтобы рука стала максимально сильной.
    При сравнении карт J — самая слабая.
    """
    cnt = Counter(hand)
    jokers = cnt.get("J", 0)

    if jokers == 0:
        # нет джокеров — обычная логика
        return hand_type_part1(hand)

    # убираем J для анализа
    cnt.pop("J")

    if not cnt:
        # все карты — J → пять одинаковых
        return (6,)

    counts = list(cnt.values())
    # найдём одну из самых больших групп и добавим к ней все джокеры
    max_val = max(counts)
    idx = counts.index(max_val)
    counts[idx] += jokers
    counts_sorted = sorted(counts, reverse=True)

    # дальше такая же классификация, как в части 1, только по новым counts
    if counts_sorted == [5]:
        return (6,)
    if counts_sorted == [4, 1]:
        return (5,)
    if counts_sorted == [3, 2]:
        return (4,)
    if counts_sorted == [3, 1, 1]:
        return (3,)
    if counts_sorted == [2, 2, 1]:
        return (2,)
    if counts_sorted == [2, 1, 1, 1]:
        return (1,)
    return (0,)


def solve_part1(data: str) -> str:
    lines = [line.split() for line in data.splitlines() if line.strip()]

    hands = []
    for hand, bid in lines:
        t = hand_type_part1(hand)
        card_rank = tuple(CARD_ORDER_1[c] for c in hand)
        hands.append((t, card_rank, hand, int(bid)))

    hands.sort()

    total = 0
    for rank, (_, _, _, bid) in enumerate(hands, start=1):
        total += rank * bid

    return str(total)


def solve_part2(data: str) -> str:
    lines = [line.split() for line in data.splitlines() if line.strip()]

    hands = []
    for hand, bid in lines:
        t = hand_type_part2(hand)
        card_rank = tuple(CARD_ORDER_2[c] for c in hand)
        hands.append((t, card_rank, hand, int(bid)))

    hands.sort()

    total = 0
    for rank, (_, _, _, bid) in enumerate(hands, start=1):
        total += rank * bid

    return str(total)


# -----------------------------
#  Точка входа
# -----------------------------
if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
