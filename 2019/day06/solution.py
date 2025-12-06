from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, Set


def parse_orbits(data: str) -> Dict[str, str]:
    """
    Разбор входных данных.
    Каждая строка вида AAA)BBB означает: BBB орбитирует AAA.
    Возвращаем словарь: child -> parent.
    """
    parent: Dict[str, str] = {}
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        center, orbiter = line.split(")")
        parent[orbiter] = center
    return parent


def count_total_orbits(parent: Dict[str, str]) -> int:
    """
    Подсчитываем общее количество прямых и непрямых орбит.
    Для каждого объекта считаем расстояние до COM.
    """
    depth_cache: Dict[str, int] = {}

    def depth(obj: str) -> int:
        if obj == "COM":
            return 0
        if obj in depth_cache:
            return depth_cache[obj]
        p = parent[obj]
        d = 1 + depth(p)
        depth_cache[obj] = d
        return d

    total = 0
    # Имеет смысл пройти по всем объектам, которые являются "детьми"
    # (они все есть в словаре parent)
    for obj in list(parent.keys()):
        total += depth(obj)
    return total


def build_undirected_graph(parent: Dict[str, str]) -> Dict[str, Set[str]]:
    """
    Строим неориентированный граф для поиска кратчайшего пути
    (используется в части 2).
    Рёбра: child <-> parent.
    """
    graph: Dict[str, Set[str]] = {}
    for child, p in parent.items():
        graph.setdefault(child, set()).add(p)
        graph.setdefault(p, set()).add(child)
    return graph


def shortest_path_length(graph: Dict[str, Set[str]], start: str, target: str) -> int:
    """
    Находим длину кратчайшего пути между start и target (в рёбрах)
    с помощью BFS.
    """
    if start == target:
        return 0

    visited: Set[str] = {start}
    queue: deque[tuple[str, int]] = deque()
    queue.append((start, 0))

    while queue:
        node, dist = queue.popleft()
        for neigh in graph.get(node, ()):
            if neigh in visited:
                continue
            if neigh == target:
                return dist + 1
            visited.add(neigh)
            queue.append((neigh, dist + 1))

    raise RuntimeError(f"Путь от {start} до {target} не найден")


def solve_part1(data: str) -> str:
    """
    Part 1: общее количество прямых и непрямых орбит.
    """
    parent = parse_orbits(data)
    total = count_total_orbits(parent)
    return str(total)


def solve_part2(data: str) -> str:
    """
    Part 2: минимальное количество орбитальных переходов
    между объектами, вокруг которых вращаются YOU и SAN.
    """
    parent = parse_orbits(data)

    if "YOU" not in parent or "SAN" not in parent:
        raise RuntimeError("Во входных данных должны присутствовать YOU и SAN")

    # YOU и SAN сами не считаются — стартуем от их центров
    start = parent["YOU"]
    target = parent["SAN"]

    graph = build_undirected_graph(parent)
    steps = shortest_path_length(graph, start, target)
    return str(steps)


if __name__ == "__main__":
    import pathlib
    import sys

    input_path = pathlib.Path("input.txt")
    data = input_path.read_text(encoding="utf-8").strip("\n")

    part = sys.argv[1] if len(sys.argv) > 1 else "both"

    if part in ("1", "one", "part1", "both"):
        print("Part 1:", solve_part1(data))
    if part in ("2", "two", "part2", "both"):
        print("Part 2:", solve_part2(data))
