from collections import deque


# Размер поля по условию (координаты 0..70)
N = 71


def parse(data: str):
    pts = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        x, y = map(int, line.split(","))
        pts.append((x, y))
    return pts


# 4-соседство
DIRS = [(1,0), (-1,0), (0,1), (0,-1)]


def bfs(blocked) -> int | None:
    """
    BFS от (0,0) до (70,70).
    blocked — множество запрещённых клеток.
    Возвращает длину пути или None, если путь невозможен.
    """
    if (0,0) in blocked:
        return None

    q = deque([(0,0,0)])  # r, c, dist
    seen = {(0,0)}

    while q:
        r, c, d = q.popleft()
        if (r, c) == (N-1, N-1):
            return d

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                if (nr, nc) not in blocked and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc, d+1))

    return None


def solve_part1(data: str) -> str:
    pts = parse(data)

    # первые 1024 байта блокируем
    blocked = set(pts[:1024])

    dist = bfs(blocked)
    return str(dist if dist is not None else "0")


def solve_part2(data: str) -> str:
    pts = parse(data)

    blocked = set()
    for (x, y) in pts:
        blocked.add((x, y))
        # Проверяем после каждого добавления
        if bfs(blocked) is None:
            # путь стал невозможен
            return f"{x},{y}"

    # по условию точно будет ответ
    return "0,0"


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
