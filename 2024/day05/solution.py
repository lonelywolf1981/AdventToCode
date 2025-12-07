def parse(data: str):
    rules = []
    updates = []

    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        if "|" in line:
            a, b = map(int, line.split("|"))
            rules.append((a, b))
        elif "," in line:
            updates.append(list(map(int, line.split(","))))

    return rules, updates


def is_valid(update, must_before):
    """Проверяет, что последовательность не нарушает ни одно правило."""
    pos = {v: i for i, v in enumerate(update)}
    for a, b in must_before:
        if a in pos and b in pos:
            if pos[a] > pos[b]:
                return False
    return True


def fix_update(update, must_before):
    """Топологическая сортировка только по элементам update."""
    items = set(update)

    # строим граф только для элементов этой строки
    from collections import defaultdict, deque

    indeg = defaultdict(int)
    g = defaultdict(list)

    for a, b in must_before:
        if a in items and b in items:
            g[a].append(b)
            indeg[b] += 1
            if a not in indeg:
                indeg[a] = 0

    # топологическая сортировка Кана
    q = deque([x for x in items if indeg[x] == 0])
    res = []

    while q:
        x = q.popleft()
        res.append(x)
        for nx in g[x]:
            indeg[nx] -= 1
            if indeg[nx] == 0:
                q.append(nx)

    # res содержит элементы в порядке разрешённых правил
    # но возможно их меньше (если цикл, но в AoC такого нет)
    return res


def solve_part1(data: str) -> str:
    # Day 5 Part 1: берём только корректные строки updates и суммируем middle.

    rules, updates = parse(data)
    must_before = rules

    total = 0

    for upd in updates:
        if is_valid(upd, must_before):
            mid = upd[len(upd)//2]
            total += mid

    return str(total)


def solve_part2(data: str) -> str:
    # Day 5 Part 2: исправить некорректные строки топологической сортировкой.

    rules, updates = parse(data)
    must_before = rules

    total = 0

    for upd in updates:
        if not is_valid(upd, must_before):
            fixed = fix_update(upd, must_before)
            mid = fixed[len(fixed)//2]
            total += mid

    return str(total)


if __name__ == "__main__":
    from pathlib import Path
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
