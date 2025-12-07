from pathlib import Path
from collections import deque

# Направления: (dr, dc)
# up, down, left, right
DIRS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

# Для каждой трубы — какие сдвиги (dr, dc) она соединяет
PIPE_DIRS = {
    "|": [DIRS["U"], DIRS["D"]],
    "-": [DIRS["L"], DIRS["R"]],
    "L": [DIRS["U"], DIRS["R"]],  # └ (сверху и справа)
    "J": [DIRS["U"], DIRS["L"]],  # ┘ (сверху и слева)
    "7": [DIRS["D"], DIRS["L"]],  # ┐ (снизу и слева)
    "F": [DIRS["D"], DIRS["R"]],  # ┌ (снизу и справа)
    "S": [],  # определим отдельно
}


def parse_map(data: str):
    grid = [list(line) for line in data.splitlines() if line.strip()]
    n = len(grid)
    m = len(grid[0])
    return grid, n, m


def find_start(grid, n, m):
    for r in range(n):
        for c in range(m):
            if grid[r][c] == "S":
                return r, c
    return None


def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def determine_start_pipe(grid, sr, sc):
    """
    Определяем, каким символом трубы должна быть S:
    подбираем такой, чтобы её две "ножки" реально соединялись
    с соседними трубами.
    """
    connections = []

    for dr, dc in DIRS.values():
        nr, nc = sr + dr, sc + dc
        if not in_bounds(grid, nr, nc):
            continue
        ch = grid[nr][nc]
        if ch == ".":
            continue
        if ch == "S":
            continue

        # Смотрим, может ли сосед соединиться обратно с S
        for ndr, ndc in PIPE_DIRS.get(ch, []):
            if nr + ndr == sr and nc + ndc == sc:
                connections.append((dr, dc))
                break

    if len(connections) != 2:
        # В корректном инпуте всегда 2
        # но если что-то не так — хотя бы не падаем
        pass

    conn_set = set(connections)
    for symbol, dirs in PIPE_DIRS.items():
        if symbol == "S":
            continue
        if set(dirs) == conn_set:
            return symbol

    # fallback, не должен понадобиться
    return "|"


def neighbors_from(grid, r, c):
    """Возвращает соседей, куда можно пойти по трубе из (r,c)."""
    ch = grid[r][c]
    res = []
    for dr, dc in PIPE_DIRS.get(ch, []):
        nr, nc = r + dr, c + dc
        if in_bounds(grid, nr, nc):
            # проверим, что сосед может соединиться обратно
            nch = grid[nr][nc]
            for ndr, ndc in PIPE_DIRS.get(nch, []):
                if nr + ndr == r and nc + ndc == c:
                    res.append((nr, nc))
                    break
    return res


def build_loop(grid, start):
    """
    Строит замкнутый цикл по трубам, начиная от start.
    Возвращает список координат (r,c) по порядку обхода, без повторного добавления start в конце.
    """
    sr, sc = start
    path = []
    visited = set()

    prev = None
    cur = (sr, sc)

    while True:
        path.append(cur)
        visited.add(cur)

        r, c = cur
        nbrs = neighbors_from(grid, r, c)

        # идём в соседа, который не prev
        nxt = None
        for cand in nbrs:
            if cand == prev:
                continue
            nxt = cand
            break

        if nxt is None:
            break

        if nxt == (sr, sc):
            # цикл замкнулся, не добавляем второй раз
            break

        prev, cur = cur, nxt

    return path


def solve_part1(data: str) -> str:
    grid, n, m = parse_map(data)
    start = find_start(grid, n, m)
    sr, sc = start

    # Определяем, чем должна быть S, и подменяем её
    s_pipe = determine_start_pipe(grid, sr, sc)
    grid[sr][sc] = s_pipe

    loop = build_loop(grid, start)

    # длина цикла / 2 (расстояние до самой дальней точки от S)
    return str(len(loop) // 2)


def solve_part2(data: str) -> str:
    grid, n, m = parse_map(data)
    start = find_start(grid, n, m)
    sr, sc = start

    # Подменяем S на реальную трубу
    s_pipe = determine_start_pipe(grid, sr, sc)
    grid[sr][sc] = s_pipe

    loop = set(build_loop(grid, start))

    # Строим "увеличенную" сетку 3x3 на каждую клетку
    H = n * 3
    W = m * 3
    big = [["." for _ in range(W)] for _ in range(H)]

    def mark(r, c, rr, cc):
        """Помечаем точку в big-сетке как стену трубы."""
        if 0 <= rr < H and 0 <= cc < W:
            big[rr][cc] = "#"

    for (r, c) in loop:
        ch = grid[r][c]
        br = r * 3 + 1
        bc = c * 3 + 1

        # центр трубы
        mark(r, c, br, bc)

        if ch == "|":
            mark(r, c, br - 1, bc)
            mark(r, c, br + 1, bc)
        elif ch == "-":
            mark(r, c, br, bc - 1)
            mark(r, c, br, bc + 1)
        elif ch == "L":  # вверх и вправо
            mark(r, c, br - 1, bc)
            mark(r, c, br, bc + 1)
        elif ch == "J":  # вверх и влево
            mark(r, c, br - 1, bc)
            mark(r, c, br, bc - 1)
        elif ch == "7":  # вниз и влево
            mark(r, c, br + 1, bc)
            mark(r, c, br, bc - 1)
        elif ch == "F":  # вниз и вправо
            mark(r, c, br + 1, bc)
            mark(r, c, br, bc + 1)
        # S уже заменена на одну из этих форм

    # Заливаем "снаружи" по big-сетке, считая '.' как пространство, '#' как стены
    visited = [[False for _ in range(W)] for _ in range(H)]
    q = deque()

    # стартуем с границы
    for x in range(W):
        if big[0][x] == ".":
            q.append((0, x))
            visited[0][x] = True
        if big[H - 1][x] == ".":
            q.append((H - 1, x))
            visited[H - 1][x] = True

    for y in range(H):
        if big[y][0] == ".":
            q.append((y, 0))
            visited[y][0] = True
        if big[y][W - 1] == ".":
            q.append((y, W - 1))
            visited[y][W - 1] = True

    while q:
        r, c = q.popleft()
        for dr, dc in DIRS.values():
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                if not visited[nr][nc] and big[nr][nc] == ".":
                    visited[nr][nc] = True
                    q.append((nr, nc))

    # Теперь все '.' в big, которые НЕ посещены — это "внутри контура".
    # Считаем исходные клетки, чьи центры принадлежат непосещённым точкам
    inside_count = 0
    for r in range(n):
        for c in range(m):
            if (r, c) in loop:
                continue
            br = r * 3 + 1
            bc = c * 3 + 1
            if not visited[br][bc] and big[br][bc] == ".":
                inside_count += 1

    return str(inside_count)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
