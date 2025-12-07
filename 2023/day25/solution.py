from collections import defaultdict, deque
import random


def parse_graph(data: str):
    g = defaultdict(set)
    for line in data.splitlines():
        if not line.strip():
            continue
        left, right = line.split(":")
        node = left.strip()
        for tgt in right.split():
            tgt = tgt.strip()
            g[node].add(tgt)
            g[tgt].add(node)
    return g


def bfs_path(g, start, end):
    """Находит один кратчайший путь между двумя вершинами."""
    q = deque([start])
    parent = {start: None}

    while q:
        cur = q.popleft()
        if cur == end:
            break
        for nx in g[cur]:
            if nx not in parent:
                parent[nx] = cur
                q.append(nx)

    if end not in parent:
        return []

    # восстановление пути
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def solve_min_cut(g):
    """
    Ищем 3-реберный min-cut через частотный анализ рёбер в кратчайших путях.
    Работает надёжно для входа Day 25.
    """
    nodes = list(g.keys())
    edge_count = defaultdict(int)

    # много случайных пар → считаем, какие рёбра встречаются чаще
    for _ in range(4000):
        a, b = random.sample(nodes, 2)
        path = bfs_path(g, a, b)
        if not path:
            continue
        for u, v in zip(path, path[1:]):
            e = tuple(sorted((u, v)))
            edge_count[e] += 1

    # выбираем 3 самых часто встречающихся ребра
    sorted_edges = sorted(edge_count.items(), key=lambda x: -x[1])
    cut_edges = [e for e, _ in sorted_edges[:3]]

    # удаляем их
    g2 = {k: set(v) for k, v in g.items()}
    for u, v in cut_edges:
        g2[u].remove(v)
        g2[v].remove(u)

    # ищем размер компонент
    seen = set()
    comp_sizes = []

    for node in g2:
        if node in seen:
            continue
        q = deque([node])
        seen.add(node)
        size = 1
        while q:
            cur = q.popleft()
            for nx in g2[cur]:
                if nx not in seen:
                    seen.add(nx)
                    size += 1
                    q.append(nx)
        comp_sizes.append(size)

    if len(comp_sizes) != 2:
        # если рандом не попал → повторим
        return None

    return comp_sizes[0] * comp_sizes[1]


def solve_part1(data: str) -> str:
    g = parse_graph(data)

    # повторяем поиск, пока не поймаем корректный min-cut
    for _ in range(50):
        res = solve_min_cut(g)
        if res is not None:
            return str(res)

    # fallback — крайне маловероятно
    return "failed"


def solve_part2(data: str) -> str:
    # В День 25 нет второй части
    return "0"


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip("\n")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
