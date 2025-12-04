from pathlib import Path
from typing import Dict, List, Set


def _parse_input(data: str) -> Dict[int, List[int]]:
    """
    Парсим строки вида:
      2 <-> 0, 3, 4
    Возвращаем словарь:
      {2: [0,3,4], ...}
    """
    graph: Dict[int, List[int]] = {}

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        # Разделяем "2 <-> 0, 3, 4"
        left, right = line.split("<->")
        node = int(left.strip())
        neighbors = [int(x.strip()) for x in right.strip().split(",")]

        graph[node] = neighbors

    return graph


def _dfs(start: int, graph: Dict[int, List[int]], visited: Set[int]) -> None:
    """
    Обычный DFS (глубинный обход).
    Помечает все достижимые из start вершины.
    """
    stack = [start]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        for nei in graph.get(v, []):
            if nei not in visited:
                stack.append(nei)


def solve_part1(data: str) -> int:
    """
    Day 12, Part 1:
    Размер компоненты связности, содержащей программу 0.
    """
    graph = _parse_input(data)
    visited: Set[int] = set()
    _dfs(0, graph, visited)
    return len(visited)


def solve_part2(data: str) -> int:
    """
    Day 12, Part 2:
    Количество компонент связности (групп).
    """
    graph = _parse_input(data)
    visited: Set[int] = set()
    groups = 0

    for node in graph.keys():
        if node not in visited:
            groups += 1
            _dfs(node, graph, visited)

    return groups


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
