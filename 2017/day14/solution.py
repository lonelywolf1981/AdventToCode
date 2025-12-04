from pathlib import Path
from typing import List, Tuple, Set


# ---------- Knot Hash из Day 10 ----------

def _single_round(
    nums: List[int],
    lengths: List[int],
    current_pos: int = 0,
    skip_size: int = 0,
) -> Tuple[int, int]:
    """
    Один раунд алгоритма Knot Hash.
    """
    n = len(nums)

    for length in lengths:
        if length > n:
            continue

        indices = [(current_pos + i) % n for i in range(length)]
        values = [nums[i] for i in indices][::-1]
        for idx, val in zip(indices, values):
            nums[idx] = val

        current_pos = (current_pos + length + skip_size) % n
        skip_size += 1

    return current_pos, skip_size


def _knot_hash_full(input_line: str) -> str:
    """
    Полный Knot Hash (64 раунда, dense hash, hex-строка из 32 символов).
    """
    lengths = [ord(c) for c in input_line] + [17, 31, 73, 47, 23]

    nums = list(range(256))
    current_pos = 0
    skip_size = 0

    for _ in range(64):
        current_pos, skip_size = _single_round(nums, lengths, current_pos, skip_size)

    dense: List[int] = []
    for block_start in range(0, 256, 16):
        x = 0
        for i in range(block_start, block_start + 16):
            x ^= nums[i]
        dense.append(x)

    return "".join(f"{b:02x}" for b in dense)


# ---------- Day 14 логика ----------

def _parse_key(data: str) -> str:
    """
    В Day 14 вход — одна строка-ключ. Берём первую непустую строку.
    """
    for line in data.splitlines():
        line = line.rstrip("\n\r")
        if line.strip() == "":
            continue
        # важен сам текст, без внешних пробельных строк,
        # но реальные AoC-входы тут без пробелов
        return line.strip()
    raise ValueError("Пустой input для Day 14")


def _build_grid(key: str) -> List[str]:
    """
    Строим 128 строк по 128 бит.
    Возвращаем список строк, каждая состоит из '0' и '1'.
    """
    grid: List[str] = []

    for row in range(128):
        row_input = f"{key}-{row}"
        h = _knot_hash_full(row_input)  # 32 hex-символа

        # hex -> 4 бита
        bits = "".join(f"{int(ch, 16):04b}" for ch in h)
        # bits длиной 128
        grid.append(bits)

    return grid


def solve_part1(data: str) -> int:
    """
    Day 14, Part 1:
    Общее количество использованных квадратов (бит '1') в 128x128 поле.
    """
    key = _parse_key(data)
    grid = _build_grid(key)
    return sum(row.count("1") for row in grid)


def solve_part2(data: str) -> int:
    """
    Day 14, Part 2:
    Количество регионов из '1' (связность по сторонам).
    """
    key = _parse_key(data)
    grid = _build_grid(key)

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    visited: Set[Tuple[int, int]] = set()

    def neighbors(r: int, c: int):
        if r > 0:
            yield r - 1, c
        if r < rows - 1:
            yield r + 1, c
        if c > 0:
            yield r, c - 1
        if c < cols - 1:
            yield r, c + 1

    def flood_fill(sr: int, sc: int) -> None:
        stack = [(sr, sc)]
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for nr, nc in neighbors(r, c):
                if (nr, nc) not in visited and grid[nr][nc] == "1":
                    stack.append((nr, nc))

    regions = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                regions += 1
                flood_fill(r, c)

    return regions


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
