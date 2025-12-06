from __future__ import annotations

from pathlib import Path
from collections import deque
from typing import Dict, Set, Tuple


Pos = Tuple[int, int]


def parse_input(data: str) -> str:
    """
    В input.txt обычно одна строка вида:
    ^ENWWW(NEEE|SSE(EE|N))$
    Берём первую непустую строку и обрезаем пробелы.
    """
    for line in data.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def build_graph(regex: str) -> Dict[Pos, Set[Pos]]:
    """
    Парсим "регулярку" и строим граф комнат:
      graph[pos] -> множество соседей-pos, соединённых дверями.

    Алгоритм:
      - current_positions: множество текущих позиций (может быть несколько из-за ветвлений).
      - стек для групп: элементы вида (group_start_positions, group_ends_so_far).
      - N/S/E/W двигают все позиции из current_positions, строим рёбра.
      - '(' — пушим на стек (текущие позиции, пустое множество концов).
      - '|' — добавляем текущие позиции в множество концов группы, откатываемся на старт группы.
      - ')' — объединяем текущие позиции с уже накопленными концами группы.
    """
    graph: Dict[Pos, Set[Pos]] = {}

    def add_edge(a: Pos, b: Pos) -> None:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)

    # стартовая комната
    start: Pos = (0, 0)
    current_positions: Set[Pos] = {start}

    # стек групп: [(group_start_positions, group_ends_so_far), ...]
    stack: list[tuple[Set[Pos], Set[Pos]]] = []

    # пропускаем ведущий '^' и финальный '$', если они есть
    if regex.startswith("^"):
        regex = regex[1:]
    if regex.endswith("$"):
        regex = regex[:-1]

    for ch in regex:
        if ch in "NSEW":
            # движение по всем текущим позициям
            new_positions: Set[Pos] = set()
            for (x, y) in current_positions:
                if ch == "N":
                    nx, ny = x, y - 1
                elif ch == "S":
                    nx, ny = x, y + 1
                elif ch == "W":
                    nx, ny = x - 1, y
                else:  # 'E'
                    nx, ny = x + 1, y
                new_pos = (nx, ny)
                add_edge((x, y), new_pos)
                new_positions.add(new_pos)
            current_positions = new_positions

        elif ch == "(":
            # начало группы: запоминаем стартовые позиции и пустое множество концов
            stack.append((set(current_positions), set()))

        elif ch == "|":
            # альтернатива: текущие позиции — один из концов группы,
            # откатываемся на старт группы
            group_start, group_ends = stack[-1]
            group_ends.update(current_positions)
            stack[-1] = (group_start, group_ends)
            current_positions = set(group_start)

        elif ch == ")":
            # конец группы: объединяем текущие позиции с концами группы
            group_start, group_ends = stack.pop()
            group_ends.update(current_positions)
            current_positions = group_ends

        else:
            # другие символы (если вдруг встретятся) игнорируем
            pass

    return graph


def bfs_distances(graph: Dict[Pos, Set[Pos]], start: Pos = (0, 0)) -> Dict[Pos, int]:
    """
    Обычный BFS по комнатам, считаем расстояния (в дверях) от start до всех достижимых.
    """
    dist: Dict[Pos, int] = {start: 0}
    dq = deque([start])

    while dq:
        v = dq.popleft()
        for u in graph.get(v, ()):
            if u not in dist:
                dist[u] = dist[v] + 1
                dq.append(u)

    return dist


def solve_part1(data: str) -> str:
    """
    Part 1: максимальное расстояние (в дверях) от стартовой комнаты.
    """
    regex = parse_input(data)
    if not regex:
        return "0"

    graph = build_graph(regex)
    dist = bfs_distances(graph, (0, 0))
    if not dist:
        return "0"

    farthest = max(dist.values())
    return str(farthest)


def solve_part2(data: str) -> str:
    """
    Part 2: число комнат, расстояние до которых >= 1000 дверей.
    """
    regex = parse_input(data)
    if not regex:
        return "0"

    graph = build_graph(regex)
    dist = bfs_distances(graph, (0, 0))

    count_1000 = sum(1 for d in dist.values() if d >= 1000)
    return str(count_1000)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
