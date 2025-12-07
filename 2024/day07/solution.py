def parse(data: str):
    tasks = []
    for line in data.splitlines():
        if not line.strip():
            continue
        left, right = line.split(":")
        target = int(left.strip())
        nums = list(map(int, right.split()))
        tasks.append((target, nums))
    return tasks


# --- Проверка Part 1 -----------------------------------------------------

def can_make_part1(target, nums):
    """
    Проверяем: можно ли получить target,
    используя только + и *.
    """

    def dfs(i, value):
        # если мы уже превысили target — смысла продолжать нет
        if value > target:
            return False

        # если дошли до конца
        if i == len(nums):
            return value == target

        x = nums[i]

        # пробуем +
        if dfs(i + 1, value + x):
            return True

        # пробуем *
        if dfs(i + 1, value * x):
            return True

        return False

    # стартуем с первого числа
    return dfs(1, nums[0])


# --- Проверка Part 2 (добавлена конкатенация) ----------------------------

def can_make_part2(target, nums):
    """
    Проверяем: можно ли получить target,
    используя +, *, ||.
    """

    def concat(a, b):
        # безопасная конкатенация целых чисел
        return int(str(a) + str(b))

    def dfs(i, value):
        if value > target:
            return False

        if i == len(nums):
            return value == target

        x = nums[i]

        # +
        if dfs(i + 1, value + x):
            return True

        # *
        if dfs(i + 1, value * x):
            return True

        # конкатенация
        c = concat(value, x)
        if dfs(i + 1, c):
            return True

        return False

    return dfs(1, nums[0])


# --- Part 1 --------------------------------------------------------------

def solve_part1(data: str) -> str:
    # Day 7 Part1: уравнения с + и *
    tasks = parse(data)
    total = 0
    for target, nums in tasks:
        if can_make_part1(target, nums):
            total += target
    return str(total)


# --- Part 2 --------------------------------------------------------------

def solve_part2(data: str) -> str:
    # Day 7 Part2: добавлена конкатенация ||
    tasks = parse(data)
    total = 0
    for target, nums in tasks:
        if can_make_part2(target, nums):
            total += target
    return str(total)


# --- Main ----------------------------------------------------------------

if __name__ == "__main__":
    from pathlib import Path
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
