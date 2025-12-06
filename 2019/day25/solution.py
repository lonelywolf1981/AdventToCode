from __future__ import annotations

from collections import deque
from pathlib import Path
import itertools
import re


# ------------------------------
#  Intcode — твой симулятор
# ------------------------------

class Intcode:
    def __init__(self, code):
        self.mem = {i: v for i, v in enumerate(code)}
        self.ip = 0
        self.rb = 0
        self.inp = deque()
        self.out = []
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
        - не понадобится ввод (opcode 3 с пустым self.inp), или
        - программа не завершится (opcode 99, self.halted = True).
        Всё, что выводится, попадает в self.out.
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
                if not self.inp:
                    # ждём ввод
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


# ------------------------------
#  Вспомогательные функции
# ------------------------------

def parse_program(text: str) -> list[int]:
    return [int(x) for x in text.replace("\n", ",").split(",") if x.strip()]


def run_script(program: list[int], commands: list[str]) -> str:
    """
    Запускает Day25-инткод и проигрывает список текстовых команд.
    Каждая команда — одна строка (без \n).
    Возвращает весь ASCII-вывод как одну большую строку.
    """

    comp = Intcode(program[:])
    output_chars: list[str] = []

    def flush():
        while comp.out:
            output_chars.append(chr(comp.out.pop(0)))

    # Стартовый вывод, до первого запроса ввода
    comp.run_until_input()
    flush()

    # Подаём команды последовательно
    for cmd in commands:
        for ch in (cmd + "\n"):
            comp.inp.append(ord(ch))
            comp.run_until_input()
            flush()
            if comp.halted:
                return "".join(output_chars)

    # Дочитываем хвост вывода (если он есть)
    while not comp.halted:
        comp.run_until_input()
        flush()
        # Если программа ждёт ввод, а мы ничего не даём — выходим
        if not comp.inp:
            break

    return "".join(output_chars)


# Маршрут, которым ты уже проходил вручную:
# - собирает все 8 безопасных предметов
# - в конце оказывается на Security Checkpoint
PATH_TO_CHECKPOINT_AND_PICKUP = [
    'south',
    'take festive hat',
    'north',
    'west',
    'south',
    'take pointer',
    'south',
    'take prime number',
    'west',
    'take coin',
    'east',
    'north',
    'north',
    'east',
    'east',
    'south',
    'south',
    'take space heater',
    'south',
    'take astrolabe',
    'north',
    'north',
    'north',
    'north',
    'take wreath',
    'north',
    'west',
    'take dehydrated water',
    'north',
    'east', # отсюда ты уже у Security Checkpoint
]


def find_password(program: list[int]) -> int:
    print("▶ Выполняем маршрут и читаем инвентарь...")

    out = run_script(program, PATH_TO_CHECKPOINT_AND_PICKUP + ["inv"])
    inventory: list[str] = []

    # Парсим блок "Items in your inventory:"
    lines = out.splitlines()
    inv_mode = False
    for line in lines:
        line = line.strip()
        if line == "Items in your inventory:":
            inv_mode = True
            continue
        if inv_mode:
            if line.startswith("- "):
                inventory.append(line[2:])
            else:
                inv_mode = False

    print(f"📦 Найдено предметов: {len(inventory)} → {inventory}")

    if len(inventory) != 8:
        raise RuntimeError(f"Ожидал 8 предметов, а нашёл {len(inventory)}")

    print("\n▶ Начинаю перебор комбинаций...\n")

    # Перебор всех подмножеств предметов
    total = 0
    for r in range(0, len(inventory) + 1):
        for drop_set in itertools.combinations(inventory, r):
            total += 1

            keep_set = [x for x in inventory if x not in drop_set]
            print(f"\n===== Попытка #{total} =====")
            print(f"🔹 Оставляем: {keep_set}")
            print(f"🔸 Выбрасываем: {list(drop_set)}")

            cmds = list(PATH_TO_CHECKPOINT_AND_PICKUP)

            # drop предметов
            for item in drop_set:
                cmds.append(f"drop {item}")

            cmds.append("inv")
            cmds.append("south")  # шаг на плиту

            out = run_script(program, cmds)

            # Выводим фразу, сказанную плитой
            last_lines = out.strip().splitlines()[-5:]
            print("Ответ плиты:")
            for L in last_lines:
                print("   ", L)

            # Проверяем, появилось ли число
            nums = re.findall(r"\d+", out)
            if nums:
                password = int(nums[0])
                print("\n🎉 НАЙДЕНО! ПРАВИЛЬНАЯ КОМБИНАЦИЯ:")
                print("📦", keep_set)
                print("🔑 Пароль:", password)
                return password

    raise RuntimeError("Не удалось подобрать комбинацию предметов")


# ------------------------------
#  Обёртки под AdventToCode
# ------------------------------

def solve_part1(data: str) -> str:
    data = data.strip()
    if not data:
        return "0"

    program = parse_program(data)
    password = find_password(program)
    return str(password)


def solve_part2(data: str) -> str:
    # У Day 25 по сути одна задача — найти этот пароль.
    # Для совместимости вернём тот же результат.
    data = data.strip()
    if not data:
        return "0"

    program = parse_program(data)
    password = find_password(program)
    return str(password)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
