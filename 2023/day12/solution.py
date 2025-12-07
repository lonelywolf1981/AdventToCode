from pathlib import Path
from functools import lru_cache


def parse_input(data: str):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    parsed = []
    for line in lines:
        left, right = line.split()
        groups = tuple(map(int, right.split(",")))
        parsed.append((left, groups))
    return parsed


# -------------------------------
#  DP решение для одной строки
# -------------------------------
def count_arrangements(pattern: str, groups: tuple[int, ...]) -> int:
    n = len(pattern)
    g_len = len(groups)

    @lru_cache(None)
    def dp(i, gi, run):
        """
        i   — позиция в pattern
        gi  — номер группы из groups
        run — текущая длина подряд идущих '#'
        """
        if i == n:  # конец строки
            # если мы в конце и есть незакрытая группа — она должна точно равняться groups[gi]
            if run > 0:
                return 1 if gi < g_len and run == groups[gi] and gi + 1 == g_len else 0
            # если никакой группы в процессе — мы должны быть на последней группе
            return 1 if gi == g_len else 0

        current = pattern[i]
        ways = 0

        # Попытка поставить '.'
        if current in ".?":
            # если сейчас идёт группа run > 0, то она должна ровно совпасть с groups[gi]
            if run > 0:
                if gi < g_len and run == groups[gi]:
                    # закрываем группу и идём дальше
                    ways += dp(i + 1, gi + 1, 0)
            else:
                # просто точка вне группы
                ways += dp(i + 1, gi, 0)

        # Попытка поставить '#'
        if current in "#?":
            # продолжаем группу
            if gi < g_len:  # если есть куда расширять
                if run + 1 <= groups[gi]:
                    ways += dp(i + 1, gi, run + 1)

        return ways

    return dp(0, 0, 0)


# -------------------------------
#  Part 1
# -------------------------------
def solve_part1(data: str) -> str:
    rows = parse_input(data)

    total = 0
    for pattern, groups in rows:
        total += count_arrangements(pattern, groups)

    return str(total)


# -------------------------------
#  Part 2
# -------------------------------
def solve_part2(data: str) -> str:
    rows = parse_input(data)

    total = 0
    for pattern, groups in rows:
        # повторяем 5 раз
        pattern2 = "?".join([pattern] * 5)
        groups2 = groups * 5
        total += count_arrangements(pattern2, groups2)

    return str(total)


# -------------------------------
#  Точка входа
# -------------------------------
if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
