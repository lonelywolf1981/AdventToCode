# Advent of Code 2016 - Day 22
# Grid Computing
#
# Ожидание от внешнего раннера:
#   solve_part1(raw_input: str) -> int
#   solve_part2(raw_input: str) -> int
#
# Файл input.txt содержит вывод df -h с строками вида:
# /dev/grid/node-x0-y0     88T   65T    23T   73%
# /dev/grid/node-x0-y1     93T   73T    20T   78%
# ...

from pathlib import Path
import re
from collections import deque


NODE_RE = re.compile(r"/dev/grid/node-x(\d+)-y(\d+)")


def _parse_nodes(data: str):
    """
    Парсим вход в структуру:
      nodes[(x, y)] = {"size": int, "used": int, "avail": int}
    Возвращаем (nodes, max_x, max_y).
    """
    nodes: dict[tuple[int, int], dict[str, int]] = {}

    for line in data.splitlines():
        line = line.strip()
        if not line.startswith("/dev/grid/node-"):
            continue

        parts = line.split()
        # parts:
        # 0: /dev/grid/node-xY-yZ
        # 1: Size (например '88T')
        # 2: Used (например '65T')
        # 3: Avail (например '23T')
        name = parts[0]
        size_str = parts[1]
        used_str = parts[2]
        avail_str = parts[3]

        m = NODE_RE.match(name)
        if not m:
            continue
        x, y = map(int, m.groups())

        size = int(size_str[:-1])   # убираем 'T'
        used = int(used_str[:-1])
        avail = int(avail_str[:-1])

        nodes[(x, y)] = {"size": size, "used": used, "avail": avail}

    if not nodes:
        raise ValueError("Не найдено ни одного узла /dev/grid/node-xY-yZ")

    max_x = max(x for x, _ in nodes.keys())
    max_y = max(y for _, y in nodes.keys())
    return nodes, max_x, max_y


# ---------------- Part 1 ---------------- #

def solve_part1(data: str) -> int:
    """
    Part 1:
    Считаем количество viable pairs (A, B):
      - A != B
      - used(A) > 0
      - used(A) <= avail(B)
    """
    nodes, _, _ = _parse_nodes(data)
    coords = list(nodes.keys())

    count = 0
    for a in coords:
        used_a = nodes[a]["used"]
        if used_a == 0:
            continue
        for b in coords:
            if b == a:
                continue
            if used_a <= nodes[b]["avail"]:
                count += 1
    return count


# ---------------- Part 2 ---------------- #

def solve_part2(data: str) -> int:
    """
    Part 2:
    Минимальное количество шагов, чтобы данные из узла (max_x, 0)
    оказались в узле (0, 0).
    Моделируем как "пятнашки":
      - пустой узел (used == 0) — дырка, которую двигаем по сетке;
      - очень большие узлы, whose used > empty.size, считаем стенами;
      - при каждом шаге данные из соседнего узла перетекают в пустой,
        дырка переходит в положение этого соседа;
      - если сосед содержал "целевые" данные, их позиция меняется на
        старую позицию дырки.
    BFS по состояниям (pos_empty, pos_goal).
    """
    nodes, max_x, max_y = _parse_nodes(data)

    # Находим пустой узел и его размер
    empty_pos = None
    empty_size = None
    for (x, y), info in nodes.items():
        if info["used"] == 0:
            empty_pos = (x, y)
            empty_size = info["size"]
            break

    if empty_pos is None:
        raise ValueError("Не найден пустой узел (used == 0)")

    # Целевой узел с данными изначально: самый правый узел в верхней строке
    # goal_pos = max((x for (x, y) in nodes.keys() if y == 0)), 0
    # goal_pos = (goal_pos[0], 0) if isinstance(goal_pos, tuple) else (max(x for (x, y) in nodes.keys() if y == 0), 0)

    # Исправление: выше немного перемудрил, сделаем явно:
    goal_x = max(x for (x, y) in nodes.keys() if y == 0)
    goal_pos = (goal_x, 0)

    # Узлы со слишком большим used никогда не влезут в пустой узел => стены
    walls = {
        (x, y)
        for (x, y), info in nodes.items()
        if info["used"] > empty_size
    }

    # BFS по состояниям (empty_pos, goal_pos)
    start_state = (empty_pos, goal_pos)

    queue = deque()
    queue.append((empty_pos, goal_pos, 0))

    visited = set()
    visited.add(start_state)

    def neighbors(pos):
        x, y = pos
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in nodes and 0 <= nx <= max_x and 0 <= ny <= max_y:
                yield (nx, ny)

    while queue:
        empty, goal, steps = queue.popleft()

        if goal == (0, 0):
            return steps

        ex, ey = empty

        for n in neighbors(empty):
            if n in walls:
                continue

            # Двигаем дырку в соседний узел n:
            # - данные из n перетекают в empty;
            # - узел n становится новой "дыркой".
            new_empty = n

            # Если в n лежали целевые данные — они переезжают в empty
            if n == goal:
                new_goal = empty
            else:
                new_goal = goal

            new_state = (new_empty, new_goal)

            if new_state in visited:
                continue

            visited.add(new_state)
            queue.append((new_empty, new_goal, steps + 1))

    # Теоретически при корректном инпуте сюда не дойдём.
    raise RuntimeError("Не удалось доставить данные в (0,0)")


def main():
    # Локальный запуск: читаем input.txt из текущей папки
    data_path = Path(__file__).with_name("input.txt")
    data = data_path.read_text(encoding="utf-8")

    part1 = solve_part1(data)
    part2 = solve_part2(data)

    print("Part 1:", part1)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
