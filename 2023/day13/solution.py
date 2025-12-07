from pathlib import Path


def parse_patterns(data: str):
    blocks = data.strip().split("\n\n")
    patterns = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if lines:
            patterns.append(lines)
    return patterns


def find_reflection(pattern, smudges_target: int):
    """
    Ищет линию отражения с заданным количеством несовпадений (smudges_target).
    Возвращает ("H", row_index) или ("V", col_index), где индекс 1-based.
    Если не найдено — (None, 0).
    """
    H = len(pattern)
    W = len(pattern[0])

    # --- Проверяем горизонтальные линии (между строками r-1 и r) ---
    for r in range(1, H):
        mismatches = 0
        top = r - 1
        bottom = r

        while top >= 0 and bottom < H:
            row_top = pattern[top]
            row_bottom = pattern[bottom]
            for c in range(W):
                if row_top[c] != row_bottom[c]:
                    mismatches += 1
            top -= 1
            bottom += 1

        if mismatches == smudges_target:
            return "H", r  # r — 1-based индекс линии

    # --- Проверяем вертикальные линии (между столбцами c-1 и c) ---
    for c in range(1, W):
        mismatches = 0
        left = c - 1
        right = c

        while left >= 0 and right < W:
            for r in range(H):
                if pattern[r][left] != pattern[r][right]:
                    mismatches += 1
            left -= 1
            right += 1

        if mismatches == smudges_target:
            return "V", c  # c — 1-based индекс линии

    return None, 0


def solve_part1(data: str) -> str:
    patterns = parse_patterns(data)
    total = 0

    for pat in patterns:
        kind, idx = find_reflection(pat, smudges_target=0)
        if kind == "H":
            total += 100 * idx
        elif kind == "V":
            total += idx
        else:
            # по условию AoC тут не должно быть, но на всякий случай
            pass

    return str(total)


def solve_part2(data: str) -> str:
    patterns = parse_patterns(data)
    total = 0

    for pat in patterns:
        kind, idx = find_reflection(pat, smudges_target=1)
        if kind == "H":
            total += 100 * idx
        elif kind == "V":
            total += idx
        else:
            # по условию AoC тут не должно быть, но на всякий случай
            pass

    return str(total)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
