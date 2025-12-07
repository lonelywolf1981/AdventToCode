from pathlib import Path
from collections import deque, defaultdict
from math import gcd


# --------------------------------------------------
# Парсинг схемы модулей
# --------------------------------------------------


def parse_modules(data: str):
    modules = {}        # name -> {"type": "broadcaster"/"flip"/"conj", "dests": [..]}
    inputs = defaultdict(list)  # name -> [sources]

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        left, right = line.split("->")
        left = left.strip()
        dests = [d.strip() for d in right.split(",")]

        if left == "broadcaster":
            mtype = "broadcaster"
            name = "broadcaster"
        elif left.startswith("%"):
            mtype = "flip"
            name = left[1:]
        elif left.startswith("&"):
            mtype = "conj"
            name = left[1:]
        else:
            # на всякий случай, если формат другой
            mtype = "broadcaster"
            name = left

        modules[name] = {
            "type": mtype,
            "dests": dests,
        }

        for d in dests:
            inputs[d].append(name)

    return modules, inputs


# --------------------------------------------------
# Симуляция одного нажатия кнопки
# --------------------------------------------------


def run_press(modules, inputs, ff_state, conj_mem, on_pulse=None):
    """
    Выполняет одну симуляцию нажатия кнопки.
    Состояния ff_state и conj_mem изменяются по месту (переносятся между нажатиями).
    Возвращает (low_count, high_count).
    """
    q = deque()
    # кнопка посылает низкий импульс в broadcaster
    q.append(("button", "broadcaster", False))

    low_count = 0
    high_count = 0

    while q:
        src, dest, pulse = q.popleft()

        # считаем импульсы
        if pulse:
            high_count += 1
        else:
            low_count += 1

        # хук-для-чего-угодно (для part2)
        if on_pulse is not None:
            on_pulse(src, dest, pulse)

        # если приёмник не модуль — просто глотаем импульс
        if dest not in modules:
            continue

        mod = modules[dest]
        mtype = mod["type"]
        dests = mod["dests"]

        if mtype == "broadcaster":
            # пересылает тот же импульс всем
            for d2 in dests:
                q.append((dest, d2, pulse))

        elif mtype == "flip":
            # flip-flop: реагирует только на low
            if pulse:  # high → игнор
                continue
            # low → переключить состояние и выдать импульс
            state = ff_state.get(dest, False)
            state = not state
            ff_state[dest] = state
            out_pulse = state  # True = high, False = low
            for d2 in dests:
                q.append((dest, d2, out_pulse))

        elif mtype == "conj":
            # conjunction: хранит последнее состояние для каждого входа
            mem = conj_mem[dest]
            mem[src] = pulse  # обновляем источник

            # если все входы high → выдаём low, иначе high
            all_high = True
            for inp in inputs[dest]:
                if not mem.get(inp, False):
                    all_high = False
                    break

            out_pulse = not all_high  # all_high → low (False), иначе high (True)
            for d2 in dests:
                q.append((dest, d2, out_pulse))

    return low_count, high_count


# --------------------------------------------------
# Part 1
# --------------------------------------------------


def solve_part1(data: str) -> str:
    modules, inputs = parse_modules(data)

    # начальные состояния
    ff_state = {name: False for name, m in modules.items() if m["type"] == "flip"}
    conj_mem = {name: {src: False for src in inputs[name]} for name, m in modules.items() if m["type"] == "conj"}

    total_low = 0
    total_high = 0

    # 1000 нажатий кнопки
    for _ in range(1000):
        low, high = run_press(modules, inputs, ff_state, conj_mem)
        total_low += low
        total_high += high

    return str(total_low * total_high)


# --------------------------------------------------
# Part 2
# --------------------------------------------------


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def solve_part2(data: str) -> str:
    modules, inputs = parse_modules(data)

    # найдём модуль, который подаёт в rx
    target_parent = None
    for name, m in modules.items():
        if "rx" in m["dests"]:
            target_parent = name
            break

    if target_parent is None:
        # на всякий случай
        return "0"

    # входы в этот модуль
    parents = inputs[target_parent]
    parents_set = set(parents)

    # состояния
    ff_state = {name: False for name, m in modules.items() if m["type"] == "flip"}
    conj_mem = {name: {src: False for src in inputs[name]} for name, m in modules.items() if m["type"] == "conj"}

    # для каждого входящего модуля фиксируем номер нажатия, на котором он шлёт high в target_parent
    first_high_press = {p: None for p in parents}

    press = 0

    # пока не увидим по одному high-импульсу от каждого родителя к target_parent
    while any(v is None for v in first_high_press.values()):
        press += 1

        def on_pulse(src, dest, pulse):
            if dest == target_parent and src in parents_set and pulse:
                if first_high_press[src] is None:
                    first_high_press[src] = press

        run_press(modules, inputs, ff_state, conj_mem, on_pulse=on_pulse)

    # теперь у каждого родителя есть "период" (для данного ввода AoC
    # первый момент, когда он шлёт high в target_parent).
    # искомое нажатие = НОК всех этих чисел.
    periods = [v for v in first_high_press.values()]
    cur = periods[0]
    for p in periods[1:]:
        cur = lcm(cur, p)

    return str(cur)


# --------------------------------------------------
# Точка входа
# --------------------------------------------------
if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
