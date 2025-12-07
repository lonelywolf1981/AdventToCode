from __future__ import annotations
from typing import Dict, Set, List


def parse(data: str):
    edges = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        a, b = line.split("-")
        edges.append((a, b))
    return edges


def build_graph(edges) -> Dict[str, Set[str]]:
    g: Dict[str, Set[str]] = {}
    for a, b in edges:
        g.setdefault(a, set()).add(b)
        g.setdefault(b, set()).add(a)
    return g


# ==============================
# Part 1 — count 3-cliques T-containing
# ==============================

def solve_part1(data: str) -> str:
    edges = parse(data)
    g = build_graph(edges)

    nodes = list(g.keys())
    count = 0

    # Перебираем тройки (i<j<k)
    n = len(nodes)
    for i in range(n):
        a = nodes[i]
        for j in range(i + 1, n):
            b = nodes[j]
            if b not in g[a]:
                continue
            for k in range(j + 1, n):
                c = nodes[k]
                # Проверяем полную связность
                if c in g[a] and c in g[b]:
                    # Условие про букву 't'
                    if a.startswith("t") or b.startswith("t") or c.startswith("t"):
                        count += 1

    return str(count)


# ==============================
# Part 2 — find maximum clique
# Используем Bron–Kerbosch c pivoting.
# ==============================

def bron_kerbosch(R: Set[str], P: Set[str], X: Set[str], g: Dict[str, Set[str]],
                  best: List[Set[str]]):
    """
    Алгоритм Bron–Kerbosch с пивотом.
    R — текущая клика.
    P — кандидаты.
    X — исключённые.
    best — список, best[0] — лучшая найденная клика.
    """
    if not P and not X:
        # нашли максимальную клику
        if len(R) > len(best[0]):
            best[0] = set(R)
        return

    # Пивот: узел, объединяющий P и X
    # уменьшает количество рекурсий
    if P:
        u = next(iter(P))
        # пробуем только кандидатов не в соседях u
        for v in list(P - g[u]):
            bron_kerbosch(R | {v}, P & g[v], X & g[v], g, best)
            P.remove(v)
            X.add(v)


def solve_part2(data: str) -> str:
    edges = parse(data)
    g = build_graph(edges)

    all_nodes = set(g.keys())
    best = [set()]  # храним одну ссылку

    bron_kerbosch(set(), set(all_nodes), set(), g, best)

    clique = sorted(best[0])
    return ",".join(clique)


# ==============================
# Runner
# ==============================

if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text().strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
