def parse(data: str):
    grid = [list(line.rstrip("\n")) for line in data.splitlines() if line.strip()]
    return grid


def solve_part1(data: str) -> str:
    grid = parse(data)
    R = len(grid)
    C = len(grid[0])

    # собираем координаты по частотам
    from collections import defaultdict
    freq = defaultdict(list)

    for r in range(R):
        for c in range(C):
            ch = grid[r][c]
            if ch != '.':
                freq[ch].append((r, c))

    antinodes = set()

    for points in freq.values():
        n = len(points)
        for i in range(n):
            r1, c1 = points[i]
            for j in range(i + 1, n):
                r2, c2 = points[j]

                dr = r1 - r2
                dc = c1 - c2

                # первая симметричная точка
                a1 = (r1 + dr, c1 + dc)
                # вторая симметричная точка
                a2 = (r2 - dr, c2 - dc)

                if 0 <= a1[0] < R and 0 <= a1[1] < C:
                    antinodes.add(a1)
                if 0 <= a2[0] < R and 0 <= a2[1] < C:
                    antinodes.add(a2)

    return str(len(antinodes))


def solve_part2(data: str) -> str:
    grid = parse(data)
    R = len(grid)
    C = len(grid[0])

    from collections import defaultdict
    freq = defaultdict(list)

    for r in range(R):
        for c in range(C):
            ch = grid[r][c]
            if ch != '.':
                freq[ch].append((r, c))

    antinodes = set()

    for points in freq.values():
        n = len(points)
        for i in range(n):
            r1, c1 = points[i]
            for j in range(i + 1, n):
                r2, c2 = points[j]

                dr = r2 - r1
                dc = c2 - c1

                # k идёт вперёд по линии
                # проверяем +k*(dr,dc)
                rr, cc = r1, c1
                while 0 <= rr < R and 0 <= cc < C:
                    antinodes.add((rr, cc))
                    rr += dr
                    cc += dc

                # k идёт назад по линии
                rr, cc = r1 - dr, c1 - dc
                while 0 <= rr < R and 0 <= cc < C:
                    antinodes.add((rr, cc))
                    rr -= dr
                    cc -= dc

    return str(len(antinodes))


if __name__ == "__main__":
    from pathlib import Path
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
