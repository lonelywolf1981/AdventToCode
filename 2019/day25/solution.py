from __future__ import annotations

from collections import deque
from pathlib import Path
import itertools
import re
from typing import Dict, List, Tuple, Set, Optional


# =========================
#   Intcode-машина (твоя)
# =========================

class Intcode:
    def __init__(self, code):
        self.mem = {i: v for i, v in enumerate(code)}
        self.ip = 0
        self.rb = 0
        self.inp = deque()
        self.out: List[int] = []
        self.halted = False

    def _get(self, i):
        return self.mem.get(i, 0)

    def _set(self, i, v):
        self.mem[i] = v

    def _addr(self, off, mode):
        val = self._get(self.ip + off)
        if mode == 0:
            return val
        elif mode == 2:
            return self.rb + val
        else:
            raise ValueError("invalid address mode")

    def _param(self, off, mode):
        val = self._get(self.ip + off)
        if mode == 0:
            return self._get(val)
        elif mode == 1:
            return val
        elif mode == 2:
            return self._get(self.rb + val)
        else:
            raise ValueError("bad param mode")

    def run_until_input(self):
        """
        Крутит программу до тех пор, пока:
        - не закончится (opcode 99), или
        - не понадобится ввод (opcode 3 при пустом inp).
        """
        while True:
            op = self._get(self.ip)
            opcode = op % 100
            m1 = (op // 100) % 10
            m2 = (op // 1000) % 10
            m3 = (op // 10000) % 10

            if opcode == 99:
                self.halted = True
                return

            if opcode in (1, 2, 7, 8):
                a = self._param(1, m1)
                b = self._param(2, m2)
                dst = self._addr(3, m3)
                if opcode == 1:
                    self._set(dst, a + b)
                elif opcode == 2:
                    self._set(dst, a * b)
                elif opcode == 7:
                    self._set(dst, 1 if a < b else 0)
                elif opcode == 8:
                    self._set(dst, 1 if a == b else 0)
                self.ip += 4

            elif opcode in (5, 6):
                a = self._param(1, m1)
                b = self._param(2, m2)
                if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                    self.ip = b
                else:
                    self.ip += 3

            elif opcode == 3:
                # Нужен ввод
                if not self.inp:
                    return
                dst = self._addr(1, m1)
                self._set(dst, self.inp.popleft())
                self.ip += 2

            elif opcode == 4:
                a = self._param(1, m1)
                self.out.append(a)
                self.ip += 2

            elif opcode == 9:
                a = self._param(1, m1)
                self.rb += a
                self.ip += 2

            else:
                raise RuntimeError("bad opcode " + str(opcode))


# =========================
#   Константы и утилиты
# =========================

FORBIDDEN_ITEMS: Set[str] = {
    "escape pod",
    "infinite loop",
    "giant electromagnet",
    "molten lava",
    "photons",
}

OPPOSITE = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
}


def flush_output(comp: Intcode) -> str:
    """Считать и очистить всё, что накопилось в comp.out, вернуть как строку."""
    chars: List[str] = []
    while comp.out:
        chars.append(chr(comp.out.pop(0)))
    return "".join(chars)


def read_room(comp: Intcode) -> str:
    """Крутит программу до ожидания ввода и возвращает весь текст."""
    comp.run_until_input()
    return flush_output(comp)


def send_command(comp: Intcode, cmd: str) -> str:
    """Отправить одну команду и вернуть текст, появившийся после неё."""
    for ch in cmd + "\n":
        comp.inp.append(ord(ch))
        comp.run_until_input()
    return flush_output(comp)


def parse_room(text: str):
    """
    Разбирает вывод комнаты.
    Возвращает (room_name: str|None, doors: list[str], items: list[str]).
    """
    lines = text.splitlines()
    room_name: Optional[str] = None
    for line in lines:
        line = line.strip()
        if line.startswith("== ") and line.endswith("=="):
            room_name = line
            break

    if room_name is None:
        return None, [], []

    doors: List[str] = []
    items: List[str] = []

    i = 0    # аккуратно пробегаемся по строкам
    while i < len(lines):
        line = lines[i].strip()

        if line == "Doors here lead:":
            i += 1
            while i < len(lines) and lines[i].strip().startswith("- "):
                doors.append(lines[i].strip()[2:])
                i += 1
            continue

        if line == "Items here:":
            i += 1
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            continue

        i += 1

    return room_name, doors, items


# =========================
#   Обход карты (DFS)
# =========================

def explore_map(program: List[int]):
    """
    Запускает дроида, полностью обходит карту, строит граф комнат и
    собирает список предметов (не забирая их).

    Возвращает:
      graph: room -> list[(direction, neighbor_room)]
      items_by_room: room -> list[safe_item]
      start_room: str
      checkpoint_room: str
      pressure_room: str
    """
    comp = Intcode(program[:])

    # стартовая комната
    text = read_room(comp)
    room_name, doors, items = parse_room(text)
    if room_name is None:
        raise RuntimeError("Не удалось распарсить стартовую комнату")

    graph: Dict[str, List[Tuple[str, str]]] = {}
    items_by_room: Dict[str, List[str]] = {}
    visited: Set[str] = set()
    checkpoint_room: Optional[str] = None
    pressure_room: Optional[str] = None

    def dfs(curr_name: str, curr_doors: List[str], curr_items: List[str]):
        nonlocal checkpoint_room, pressure_room

        if curr_name in visited:
            return
        visited.add(curr_name)

        safe_items = [it for it in curr_items if it not in FORBIDDEN_ITEMS]
        items_by_room[curr_name] = safe_items

        if curr_name == "== Security Checkpoint ==" and checkpoint_room is None:
            checkpoint_room = curr_name
        if curr_name == "== Pressure-Sensitive Floor ==" and pressure_room is None:
            pressure_room = curr_name

        for d in curr_doors:
            # шаг в соседнюю комнату
            text2 = send_command(comp, d)
            next_name, next_doors, next_items = parse_room(text2)
            if next_name is None:
                # что-то странное, откатываемся
                send_command(comp, OPPOSITE[d])
                continue

            graph.setdefault(curr_name, []).append((d, next_name))
            graph.setdefault(next_name, []).append((OPPOSITE[d], curr_name))

            dfs(next_name, next_doors, next_items)

            # возвращаемся назад
            send_command(comp, OPPOSITE[d])

    dfs(room_name, doors, items)

    if checkpoint_room is None:
        raise RuntimeError("Не найден Security Checkpoint")
    if pressure_room is None:
        raise RuntimeError("Не найден Pressure-Sensitive Floor")

    return graph, items_by_room, room_name, checkpoint_room, pressure_room


# =========================
#   BFS по графу комнат
# =========================

def bfs_path(graph: Dict[str, List[Tuple[str, str]]], start: str, goal: str) -> List[str]:
    """
    По графу комнат находим путь как последовательность направлений.
    Используем обычный BFS.
    """
    from collections import deque as dq

    q = dq()
    q.append(start)
    prev: Dict[str, Tuple[str, str] | None] = {start: None}

    while q:
        v = q.popleft()
        if v == goal:
            break
        for d, u in graph.get(v, []):
            if u not in prev:
                prev[u] = (v, d)  # пришли в u из v направлением d
                q.append(u)

    if goal not in prev:
        raise RuntimeError(f"Нет пути от {start} до {goal}")

    # восстанавливаем путь
    dirs: List[str] = []
    cur = goal
    while prev[cur] is not None:
        v, d = prev[cur]
        dirs.append(d)
        cur = v
    dirs.reverse()
    return dirs


# =========================
#   Строим маршрут сбора
# =========================

def build_collection_route(
    graph: Dict[str, List[Tuple[str, str]]],
    items_by_room: Dict[str, List[str]],
    start_room: str,
    checkpoint_room: str,
) -> Tuple[List[str], List[str]]:
    """
    Строим маршрут:
      - от старта до всех комнат с предметами (с командами take ...),
      - в конце до Security Checkpoint.

    Возвращает (route, full_inventory_list).
    """
    # копия предметов
    items_left: Dict[str, List[str]] = {
        room: items[:] for room, items in items_by_room.items() if items
    }
    current_room = start_room
    route: List[str] = []
    full_inv: List[str] = []

    while items_left:
        targets = list(items_left.keys())
        best_room: Optional[str] = None
        best_path: Optional[List[str]] = None

        # находим ближайшую комнату с предметами
        for room in targets:
            path = bfs_path(graph, current_room, room)
            if best_path is None or len(path) < len(best_path):
                best_path = path
                best_room = room

        assert best_room is not None and best_path is not None

        # идём по пути
        for d in best_path:
            route.append(d)
        current_room = best_room

        # берём все предметы в комнате
        for item in items_left[best_room]:
            route.append(f"take {item}")
            full_inv.append(item)

        # предметы в комнате закончились
        del items_left[best_room]

    # когда все предметы собраны, идём к чекпоинту
    if current_room != checkpoint_room:
        path_to_checkpoint = bfs_path(graph, current_room, checkpoint_room)
        for d in path_to_checkpoint:
            route.append(d)
        current_room = checkpoint_room

    return route, full_inv


# =========================
#   Запуск сценария (отдельный)
# =========================

def run_script(program: List[int], commands: List[str]) -> str:
    """
    Запускает инткод с нуля и проигрывает список команд,
    возвращает весь ASCII-вывод.
    """
    comp = Intcode(program[:])
    out_chars: List[str] = []

    def flush():
        while comp.out:
            out_chars.append(chr(comp.out.pop(0)))

    # стартовый вывод
    comp.run_until_input()
    flush()

    # команды
    for cmd in commands:
        for ch in cmd + "\n":
            comp.inp.append(ord(ch))
            comp.run_until_input()
            flush()
            if comp.halted:
                return "".join(out_chars)

    # дочитываем хвост
    while not comp.halted:
        comp.run_until_input()
        flush()
        if not comp.inp:
            break

    return "".join(out_chars)


# =========================
#   Поиск пароля (брутфорс)
# =========================

def find_password(program: List[int]) -> int:
    print("▶ Обход карты...")
    graph, items_by_room, start_room, checkpoint_room, pressure_room = explore_map(program)
    print("Стартовая комната:", start_room)
    print("Security Checkpoint:", checkpoint_room)
    print("Pressure-Sensitive Floor:", pressure_room)

    print("\nПредметы по комнатам:")
    for room, items in items_by_room.items():
        print(" ", room, ":", items)

    print("\n▶ Строим маршрут сбора предметов...")
    route, inventory = build_collection_route(graph, items_by_room, start_room, checkpoint_room)
    print("Построенный маршрут длиной", len(route), "команд")
    print("Инвентарь для перебора:", inventory)

    # направление от чекпоинта к плите
    plate_dir: Optional[str] = None
    for d, neigh in graph.get(checkpoint_room, []):
        if neigh == pressure_room:
            plate_dir = d
            break
    if plate_dir is None:
        raise RuntimeError("Не удалось найти направление от чекпоинта к плите")

    print("Направление к плите из чекпоинта:", plate_dir)

    print("\n▶ Начинаем перебор комбинаций...\n")
    total = 0
    for r in range(0, len(inventory) + 1):
        for drop_set in itertools.combinations(inventory, r):
            total += 1
            keep = [x for x in inventory if x not in drop_set]
            print(f"\n===== Попытка #{total} =====")
            print("🔹 Оставляем:", keep)
            print("🔸 Выбрасываем:", list(drop_set))

            cmds = list(route)
            for item in drop_set:
                cmds.append(f"drop {item}")
            cmds.append("inv")
            cmds.append(plate_dir)

            out = run_script(program, cmds)
            last_lines = out.strip().splitlines()[-6:]
            print("Ответ плиты / финальный вывод:")
            for L in last_lines:
                print("   ", L)

            nums = re.findall(r"\d+", out)
            if nums:
                password = int(nums[0])
                print("\n🎉 Найдена комбинация:", keep)
                print("Пароль:", password)
                return password

    raise RuntimeError("Не удалось подобрать комбинацию")


# =========================
#   Обёртки под AdventToCode
# =========================

def parse_program(text: str) -> List[int]:
    return [int(x) for x in text.replace("\n", ",").split(",") if x.strip()]


def solve_part1(data: str) -> str:
    data = data.strip()
    if not data:
        return "0"
    program = parse_program(data)
    # Запуск брутфорса ТОЛЬКО здесь
    password = find_password(program)
    return str(password)


def solve_part2(data: str) -> str:
    # У Day 25 фактически нет второй части.
    # Делаем заглушку, чтобы start.py не запускал перебор снова.
    return "not implemented"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
