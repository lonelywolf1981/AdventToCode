from __future__ import annotations
from typing import List, Tuple, Dict, Optional


# ================== Intcode ==================

def parse_program(data: str) -> List[int]:
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


class Intcode:
    def __init__(self, program: List[int]):
        # Делаем большую "бесконечную" память
        self.mem = program[:] + [0] * 20000
        self.ip = 0
        self.rb = 0
        self.halted = False
        self.inputs: List[int] = []

    def add_input(self, v: int) -> None:
        self.inputs.append(v)

    def run(self) -> List[int]:
        """
        Запуск до полного завершения.
        Возвращает список всех выводов (целые числа, в том числе ASCII-коды).
        """
        outputs: List[int] = []

        while not self.halted:
            op = self.mem[self.ip] % 100
            m1 = (self.mem[self.ip] // 100) % 10
            m2 = (self.mem[self.ip] // 1000) % 10
            m3 = (self.mem[self.ip] // 10000) % 10

            def get(i: int, m: int) -> int:
                v = self.mem[self.ip + i]
                if m == 0:
                    return self.mem[v]
                elif m == 1:
                    return v
                elif m == 2:
                    return self.mem[self.rb + v]
                else:
                    raise ValueError("bad mode")

            def addr(i: int, m: int) -> int:
                v = self.mem[self.ip + i]
                if m == 0:
                    return v
                elif m == 2:
                    return self.rb + v
                else:
                    raise ValueError("bad mode for address")

            if op == 99:
                self.halted = True
                break

            elif op in (1, 2):  # add / mul
                a = get(1, m1)
                b = get(2, m2)
                out = addr(3, m3)
                self.mem[out] = a + b if op == 1 else a * b
                self.ip += 4

            elif op == 3:  # input
                if not self.inputs:
                    raise RuntimeError("input expected")
                out = addr(1, m1)
                self.mem[out] = self.inputs.pop(0)
                self.ip += 2

            elif op == 4:  # output
                a = get(1, m1)
                outputs.append(a)
                self.ip += 2

            elif op in (5, 6):  # jumps
                a = get(1, m1)
                b = get(2, m2)
                if (op == 5 and a != 0) or (op == 6 and a == 0):
                    self.ip = b
                else:
                    self.ip += 3

            elif op == 7:  # less than
                a = get(1, m1)
                b = get(2, m2)
                out = addr(3, m3)
                self.mem[out] = 1 if a < b else 0
                self.ip += 4

            elif op == 8:  # equals
                a = get(1, m1)
                b = get(2, m2)
                out = addr(3, m3)
                self.mem[out] = 1 if a == b else 0
                self.ip += 4

            elif op == 9:  # adjust relative base
                a = get(1, m1)
                self.rb += a
                self.ip += 2

            else:
                raise RuntimeError(f"Unknown opcode {op}")

        return outputs


# ================== Общие вспомогательные функции ==================

def build_grid(outputs: List[int]) -> List[str]:
    """
    Преобразуем ASCII-вывод в список строк (карту).
    """
    text = "".join(chr(c) for c in outputs)
    lines = [line for line in text.split("\n") if line]
    return lines


def find_intersections(grid: List[str]) -> int:
    h = len(grid)
    if h == 0:
        return 0
    w = len(grid[0])
    total = 0

    def is_scaffold(x: int, y: int) -> bool:
        if 0 <= y < h and 0 <= x < w:
            return grid[y][x] == "#"
        return False

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if grid[y][x] == "#" and is_scaffold(x, y - 1) and is_scaffold(x, y + 1) and is_scaffold(x - 1, y) and is_scaffold(x + 1, y):
                total += x * y

    return total


# ================== Построение маршрута по карте (Part 2) ==================

# Направления: 0=вверх, 1=вправо, 2=вниз, 3=влево
DIRS = [
    (0, -1),  # up
    (1, 0),   # right
    (0, 1),   # down
    (-1, 0),  # left
]
ROBOT_CHARS = "^>v<"


def build_route(grid: List[str]) -> List[str]:
    """
    Строим полный маршрут как список токенов: ['R','8','L','10',...].
    Алгоритм:
      - стоим на старте;
      - пока можем:
        - поворачиваем L или R (если возможно),
        - идём вперёд максимально, считаем шаги.
    """
    h = len(grid)
    w = len(grid[0])

    def is_scaffold(x: int, y: int) -> bool:
        if 0 <= y < h and 0 <= x < w:
            return grid[y][x] in ("#", "^", "v", "<", ">")
        return False

    # Находим старт и направление
    sx = sy = None
    dir_idx = None
    for y in range(h):
        for x in range(w):
            ch = grid[y][x]
            if ch in ROBOT_CHARS:
                sx, sy = x, y
                dir_idx = ROBOT_CHARS.index(ch)
                break
        if sx is not None:
            break

    if sx is None or dir_idx is None:
        raise RuntimeError("Не найден робот на карте")

    x, y = sx, sy
    moves: List[str] = []

    while True:
        # Пытаемся повернуть влево или вправо, если есть путь
        turned = False
        for turn_label, delta in (("L", -1), ("R", 1)):
            ndir = (dir_idx + delta) % 4
            dx, dy = DIRS[ndir]
            nx, ny = x + dx, y + dy
            if is_scaffold(nx, ny):
                # Есть куда идти после поворота
                dir_idx = ndir
                moves.append(turn_label)
                # шагаем вперёд максимально
                steps = 0
                while True:
                    nx, ny = x + DIRS[dir_idx][0], y + DIRS[dir_idx][1]
                    if is_scaffold(nx, ny):
                        x, y = nx, ny
                        steps += 1
                    else:
                        break
                moves.append(str(steps))
                turned = True
                break

        if not turned:
            # Никуда повернуть и идти уже нельзя — маршрут закончен
            break

    return moves


# ================== Сжатие маршрута в A/B/C ==================

def encode(tokens: List[str]) -> str:
    return ",".join(tokens)


def fits_limit(tokens: List[str]) -> bool:
    return len(encode(tokens)) <= 20


def compress_route(route: List[str]) -> Tuple[str, str, str, str]:
    """
    Ищем функции A/B/C и main routine, удовлетворяющие ограничениям AoC:
      - каждая функция <= 20 символов (включая запятые),
      - main routine <= 20 символов.
    Возвращаем (main_str, A_str, B_str, C_str).
    """

    # patterns: 'A'/'B'/'C' -> список токенов или None
    from copy import deepcopy

    best: Optional[Tuple[List[str], Dict[str, List[str]]]] = None

    def dfs(idx: int, patterns: Dict[str, Optional[List[str]]], main_seq: List[str]) -> bool:
        nonlocal best
        if idx == len(route):
            # Вся строка покрыта; проверяем длину main и что все A/B/C определены
            if len(encode(main_seq)) <= 20 and all(patterns[k] is not None for k in ("A", "B", "C")):
                # Сохраняем решение
                best = (main_seq[:], {k: patterns[k] for k in ("A", "B", "C")})  # type: ignore[index]
                return True
            return False

        # Сначала пытаемся применить уже существующие шаблоны
        for name in ("A", "B", "C"):
            pat = patterns[name]
            if pat is None:
                continue
            L = len(pat)
            if route[idx:idx + L] == pat:
                new_main = main_seq + [name]
                if len(encode(new_main)) <= 20:
                    if dfs(idx + L, patterns, new_main):
                        return True

        # Если ни один шаблон не подошёл — пробуем создать новый (первый неинициализированный)
        # Это гарантирует, что сначала полностью определим A, потом B, потом C.
        for name in ("A", "B", "C"):
            if patterns[name] is None:
                # создаём новый шаблон, начиная с route[idx:]
                # выбираем длину от 2 токенов (turn+steps) до тех пор, пока строка <= 20 символов
                for end in range(idx + 2, len(route) + 1):
                    cand = route[idx:end]
                    if not fits_limit(cand):
                        break
                    new_patterns = deepcopy(patterns)
                    new_patterns[name] = cand
                    new_main = main_seq + [name]
                    if not fits_limit(new_main):
                        continue
                    if dfs(end, new_patterns, new_main):
                        return True
                # Не получилось с этим именем — дальше имена не трогаем
                return False

        # Если сюда дошли — вариантов нет
        return False

    initial_patterns: Dict[str, Optional[List[str]]] = {"A": None, "B": None, "C": None}
    dfs(0, initial_patterns, [])
    if best is None:
        raise RuntimeError("Не удалось сжать маршрут в A/B/C")

    main_seq, patterns = best
    main_str = encode(main_seq) + "\n"
    a_str = encode(patterns["A"]) + "\n"  # type: ignore[index]
    b_str = encode(patterns["B"]) + "\n"  # type: ignore[index]
    c_str = encode(patterns["C"]) + "\n"  # type: ignore[index]

    # На всякий случай проверим ограничения
    assert len(main_str.strip()) <= 20
    assert len(a_str.strip()) <= 20
    assert len(b_str.strip()) <= 20
    assert len(c_str.strip()) <= 20

    return main_str, a_str, b_str, c_str


# ================== Решения частей ==================

def solve_part1(data: str) -> str:
    program = parse_program(data)
    comp = Intcode(program)
    outputs = comp.run()
    grid = build_grid(outputs)
    answer = find_intersections(grid)
    return str(answer)


def solve_part2(data: str) -> str:
    program = parse_program(data)

    # 1) Сначала строим карту (как в part1), чтобы получить маршрут
    comp_map = Intcode(program)
    outputs = comp_map.run()
    grid = build_grid(outputs)

    # 2) Строим полный маршрут L/R + шаги
    route = build_route(grid)

    # 3) Сжимаем маршрут в A/B/C + main
    main_str, a_str, b_str, c_str = compress_route(route)

    # 4) Запускаем программу в "боевом" режиме
    prog2 = program[:]
    prog2[0] = 2
    comp = Intcode(prog2)

    # Кидаем строки по очереди + 'n' (видеопоток не нужен)
    full_input = main_str + a_str + b_str + c_str + "n\n"
    for ch in full_input:
        comp.add_input(ord(ch))

    outputs2 = comp.run()
    # Последнее значение — ответ
    return str(outputs2[-1])


# ================== Шаблон запуска ==================

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
