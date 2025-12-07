def parse_input(data: str):
    parts = data.strip().split("\n\n")

    # первая секция — список семян
    seeds = list(map(int, parts[0].split()[1:]))

    # остальные секции — map-блоки
    maps = []
    for block in parts[1:]:
        lines = block.splitlines()[1:]
        rules = []
        for line in lines:
            dest, src, ln = map(int, line.split())
            rules.append((dest, src, ln))
        maps.append(rules)

    return seeds, maps


def apply_maps_single(value: int, maps):
    """Прогон одиночного значения через полный pipeline."""
    x = value
    for rules in maps:
        for dest, src, ln in rules:
            if src <= x < src + ln:
                x = dest + (x - src)
                break
    return x


def solve_part1(data: str) -> str:
    seeds, maps = parse_input(data)

    best = float("inf")
    for s in seeds:
        loc = apply_maps_single(s, maps)
        if loc < best:
            best = loc

    return str(best)


# ---------- Part 2: интервальное решение ----------

def apply_map_ranges(ranges, rules):
    """
    На входе ranges = список (start, end) — включительно-эксклюзивные интервалы.
    На выходе новые интервалы после применения одного map-блока.
    """
    out = []

    for start, end in ranges:
        cur = start
        while cur < end:
            applied = False
            for dest, src, ln in rules:
                src_end = src + ln
                # пересекается ли текущая точка с правилом?
                if cur >= src and cur < src_end:
                    # кусок который попадает в правило
                    take_end = min(end, src_end)
                    new_start = dest + (cur - src)
                    new_end = new_start + (take_end - cur)
                    out.append((new_start, new_end))
                    cur = take_end
                    applied = True
                    break

            if not applied:
                # кусок вне правил → он проходит без изменений
                # ищем ближайшую границу правила
                next_cut = end
                for _dest, src, ln in rules:
                    if src > cur:
                        next_cut = min(next_cut, src)
                out.append((cur, next_cut))
                cur = next_cut

    return out


def solve_part2(data: str) -> str:
    seeds, maps = parse_input(data)

    # seeds заданы парами: start, length
    ranges = []
    i = 0
    while i < len(seeds):
        start = seeds[i]
        ln = seeds[i + 1]
        ranges.append((start, start + ln))
        i += 2

    # прогоняем интервалы через pipeline
    for rules in maps:
        ranges = apply_map_ranges(ranges, rules)

    # находим минимальный location
    best = min(r[0] for r in ranges)
    return str(best)


# ---------- Точка входа ----------
if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
