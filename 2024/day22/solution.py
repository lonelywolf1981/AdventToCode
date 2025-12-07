def parse(data: str):
    seeds = []
    for line in data.splitlines():
        line = line.strip()
        if line:
            seeds.append(int(line))
    return seeds


MASK = 0xFFFFFF  # 2^24 - 1


def next_num(n: int) -> int:
    """
    Генерация следующего секретного числа по формуле из задачи:

        n = (n * 64  ^ n) % 16777216
        n = (n // 32 ^ n) % 16777216
        n = (n * 2048 ^ n) % 16777216
    """
    n = (n * 64 ^ n) & MASK
    n = (n // 32 ^ n) & MASK
    n = (n * 2048 ^ n) & MASK
    return n


def solve_part1(data: str) -> str:
    """
    Part 1:
    Для каждого покупателя 2000 раз применяем next_num(seeds[i]),
    и в сумму добавляем ИМЕННО 2000-е секретное число (а не цифры цен).

    Ответ = сумма этих 2000-х секретов по всем покупателям.
    """
    seeds = parse(data)
    total = 0

    for seed in seeds:
        n = seed
        for _ in range(2000):
            n = next_num(n)
        total += n

    return str(total)


def solve_part2(data: str) -> str:
    """
    Part 2:
    Для каждого покупателя:

      - считаем 2000 секретов и их последние цифры (цены),
      - строим последовательность изменений цен (дельты),
      - для каждой последовательности из 4 дельт берём первую появившуюся цену,
      - глобально суммируем цены по одинаковым ключам (4 дельты),
      - берём максимальную сумму.
    """
    from collections import defaultdict

    seeds = parse(data)
    key_sum = defaultdict(int)  # key(4 дельты) -> суммарные бананы

    for seed in seeds:
        n = seed
        prices = []
        for _ in range(2000):
            n = next_num(n)
            prices.append(n % 10)

        # diffs[i] = prices[i+1] - prices[i], длина 1999
        diffs = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]

        # для этого покупателя запоминаем первую цену для каждого ключа
        seen_first = {}  # key -> price

        # окно по 4 дельтам: (diffs[i-3], ..., diffs[i])
        # цена при этом — prices[i+1]
        for i in range(3, len(diffs)):
            key = (diffs[i - 3], diffs[i - 2], diffs[i - 1], diffs[i])
            if key not in seen_first:
                price_at_first = prices[i + 1]
                seen_first[key] = price_at_first

        # добавляем в глобальную сумму
        for key, price in seen_first.items():
            key_sum[key] += price

    best = max(key_sum.values()) if key_sum else 0
    return str(best)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text().strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
