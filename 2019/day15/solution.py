from __future__ import annotations
from typing import List, Tuple, Dict, Optional
import collections


# ================== Intcode-computer ==================

def parse_program(data: str) -> List[int]:
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


class Intcode:
    def __init__(self, mem: List[int]):
        self.mem = mem[:] + [0] * 10_000  # фиксируем длинную память
        self.ip = 0
        self.rb = 0
        self.halted = False

    def clone(self) -> "Intcode":
        c = Intcode(self.mem[:])
        c.ip = self.ip
        c.rb = self.rb
        c.halted = self.halted
        return c

    def run(self, inp: Optional[int] = None) -> Optional[int]:
        """
        Запустить до вывода или остановки.
        inp — команда движения (или None, если не требуется).
        Возвращает:
           output (0,1,2) или None, если halted.
        """
        while True:
            op = self.mem[self.ip] % 100
            mode1 = (self.mem[self.ip] // 100) % 10
            mode2 = (self.mem[self.ip] // 1000) % 10
            mode3 = (self.mem[self.ip] // 10_000) % 10

            def get(idx, mode):
                v = self.mem[self.ip + idx]
                if mode == 0:
                    return self.mem[v]
                if mode == 1:
                    return v
                if mode == 2:
                    return self.mem[self.rb + v]
                raise ValueError("bad mode")

            def addr(idx, mode):
                v = self.mem[self.ip + idx]
                if mode == 0:
                    return v
                if mode == 2:
                    return self.rb + v
                raise ValueError("bad addr mode")

            if op == 99:
                self.halted = True
                return None

            elif op in (1, 2):
                a = get(1, mode1)
                b = get(2, mode2)
                out = addr(3, mode3)
                self.mem[out] = a + b if op == 1 else a * b
                self.ip += 4

            elif op == 3:
                if inp is None:
                    raise RuntimeError("input expected but not provided")
                out = addr(1, mode1)
                self.mem[out] = inp
                self.ip += 2
                inp = None  # input consumed

            elif op == 4:
                a = get(1, mode1)
                self.ip += 2
                return a

            elif op in (5, 6):
                a = get(1, mode1)
                b = get(2, mode2)
                if (op == 5 and a != 0) or (op == 6 and a == 0):
                    self.ip = b
                else:
                    self.ip += 3

            elif op == 7:
                a = get(1, mode1)
                b = get(2, mode2)
                out = addr(3, mode3)
                self.mem[out] = 1 if a < b else 0
                self.ip += 4

            elif op == 8:
                a = get(1, mode1)
                b = get(2, mode2)
                out = addr(3, mode3)
                self.mem[out] = 1 if a == b else 0
                self.ip += 4

            elif op == 9:
                a = get(1, mode1)
                self.rb += a
                self.ip += 2

            else:
                raise RuntimeError(f"Unknown opcode {op}")


# ================== Movement helpers ==================

DIRS = {
    1: (0, -1),  # up
    2: (0, 1),   # down
    3: (-1, 0),  # left
    4: (1, 0),   # right
}

REVERSE = {1: 2, 2: 1, 3: 4, 4: 3}


def explore_map(program: List[int]) -> Tuple[Dict[Tuple[int,int], int], Tuple[int,int]]:
    """
    Возвращает:
      - map: {(x,y): tile}
         tile = 0 — стена
         tile = 1 — пол
         tile = 2 — кислородная система
      - координата кислородной системы
    Полное исследование DFS с хранением состояний Intcode.
    """
    start = (0, 0)
    world = {start: 1}
    oxygen = None

    # стек для DFS: (x,y, interpreter_state)
    stack = [(0, 0, Intcode(program))]

    visited = set([(0, 0)])

    while stack:
        x, y, state = stack.pop()

        for cmd in (1, 2, 3, 4):
            dx, dy = DIRS[cmd]
            nx, ny = x + dx, y + dy

            if (nx, ny) in world:  # уже исследована
                continue

            new_state = state.clone()
            out = new_state.run(cmd)

            if out == 0:  # стена
                world[(nx, ny)] = 0
            elif out in (1, 2):  # пол или кислород
                world[(nx, ny)] = out
                if out == 2:
                    oxygen = (nx, ny)

                # продолжаем DFS
                stack.append((nx, ny, new_state))

    return world, oxygen


def bfs_distance(world: Dict[Tuple[int,int], int], start: Tuple[int,int], target: Tuple[int,int]) -> int:
    """ BFS для поиска кратчайшего пути. """
    q = collections.deque([(start, 0)])
    seen = {start}

    while q:
        (x, y), d = q.popleft()
        if (x, y) == target:
            return d
        for dx, dy in DIRS.values():
            nx, ny = x + dx, y + dy
            if world.get((nx, ny), 0) != 0 and (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append(((nx, ny), d + 1))

    return -1


def bfs_oxygen_fill(world: Dict[Tuple[int,int], int], start: Tuple[int,int]) -> int:
    """
    BFS-разливание кислорода.
    Возвращает количество минут для полного заполнения.
    """
    q = collections.deque()
    q.append((start, 0))
    seen = {start}
    max_d = 0

    while q:
        (x, y), d = q.popleft()
        max_d = max(max_d, d)
        for dx, dy in DIRS.values():
            nx, ny = x + dx, y + dy
            if world.get((nx, ny), 0) != 0 and (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append(((nx, ny), d + 1))

    return max_d


# ================== Solutions ==================

def solve_part1(data: str) -> str:
    program = parse_program(data)
    world, oxygen = explore_map(program)
    if oxygen is None:
        return "no oxygen found"
    dist = bfs_distance(world, (0, 0), oxygen)
    return str(dist)


def solve_part2(data: str) -> str:
    program = parse_program(data)
    world, oxygen = explore_map(program)
    if oxygen is None:
        return "no oxygen found"
    minutes = bfs_oxygen_fill(world, oxygen)
    return str(minutes)


# ================== template ==================

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
