from pathlib import Path
from typing import List, Tuple, Dict, Deque, Optional
from collections import deque


Instruction = Tuple[str, List[str]]


def _parse_program(data: str) -> List[Instruction]:
    """
    Разбираем input.txt в список инструкций:
    (opcode, [arg1, arg2, ...])
    """
    program: List[Instruction] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        op = parts[0]
        args = parts[1:]
        program.append((op, args))
    if not program:
        raise ValueError("Пустой input для Day 18")
    return program


def _get_value(x: str, regs: Dict[str, int]) -> int:
    """
    Значение операнда: число или значение регистра.
    """
    try:
        return int(x)
    except ValueError:
        return regs.get(x, 0)


# ---------- Part 1 ----------

def solve_part1(data: str) -> int:
    """
    Day 18, Part 1:
    Одна программа, 'snd' запоминает последнюю частоту,
    'rcv X' при X != 0 восстанавливает её и возвращает.
    """
    program = _parse_program(data)

    regs: Dict[str, int] = {}
    ip = 0  # instruction pointer
    last_sound: Optional[int] = None

    while 0 <= ip < len(program):
        op, args = program[ip]

        if op == "snd":
            x = args[0]
            last_sound = _get_value(x, regs)
            ip += 1

        elif op == "set":
            x, y = args
            regs[x] = _get_value(y, regs)
            ip += 1

        elif op == "add":
            x, y = args
            regs[x] = regs.get(x, 0) + _get_value(y, regs)
            ip += 1

        elif op == "mul":
            x, y = args
            regs[x] = regs.get(x, 0) * _get_value(y, regs)
            ip += 1

        elif op == "mod":
            x, y = args
            regs[x] = regs.get(x, 0) % _get_value(y, regs)
            ip += 1

        elif op == "rcv":
            x = args[0]
            if _get_value(x, regs) != 0:
                # Восстанавливаем последнюю частоту
                if last_sound is None:
                    raise RuntimeError("rcv с ненулевым X, но ни одного snd ещё не было")
                return last_sound
            ip += 1

        elif op == "jgz":
            x, y = args
            if _get_value(x, regs) > 0:
                ip += _get_value(y, regs)
            else:
                ip += 1

        else:
            raise ValueError(f"Неизвестная инструкция: {op!r}")

    # Теоретически AoC гарантирует, что раньше вернёмся из rcv.
    raise RuntimeError("Программа завершилась, не восстановив ни одной частоты")


# ---------- Part 2 ----------

class DuetProgram:
    def __init__(self, pid: int, program: List[Instruction]) -> None:
        self.pid = pid
        self.program = program
        self.regs: Dict[str, int] = {"p": pid}
        self.ip: int = 0
        self.queue: Deque[int] = deque()
        self.send_count: int = 0
        self.waiting: bool = False
        self.terminated: bool = False

    def step(self, other_queue: Deque[int]) -> None:
        """
        Выполнить одну инструкцию (если возможно).
        - Если ждём на rcv и данных нет, остаёмся waiting=True, ip не меняется.
        - Если выходим за пределы программы, terminated=True.
        """
        if self.terminated:
            return

        if not (0 <= self.ip < len(self.program)):
            self.terminated = True
            return

        op, args = self.program[self.ip]

        def val(s: str) -> int:
            return _get_value(s, self.regs)

        if op == "snd":
            x = args[0]
            v = val(x)
            other_queue.append(v)
            self.send_count += 1
            self.ip += 1
            self.waiting = False

        elif op == "set":
            x, y = args
            self.regs[x] = val(y)
            self.ip += 1
            self.waiting = False

        elif op == "add":
            x, y = args
            self.regs[x] = self.regs.get(x, 0) + val(y)
            self.ip += 1
            self.waiting = False

        elif op == "mul":
            x, y = args
            self.regs[x] = self.regs.get(x, 0) * val(y)
            self.ip += 1
            self.waiting = False

        elif op == "mod":
            x, y = args
            self.regs[x] = self.regs.get(x, 0) % val(y)
            self.ip += 1
            self.waiting = False

        elif op == "rcv":
            x = args[0]
            if self.queue:
                self.regs[x] = self.queue.popleft()
                self.ip += 1
                self.waiting = False
            else:
                # Нет значения — блокируемся, ip не двигаем
                self.waiting = True

        elif op == "jgz":
            x, y = args
            if val(x) > 0:
                self.ip += val(y)
            else:
                self.ip += 1
            self.waiting = False

        else:
            raise ValueError(f"Неизвестная инструкция: {op!r}")

        # Проверка выхода за пределы после шага
        if not (0 <= self.ip < len(self.program)):
            self.terminated = True


def solve_part2(data: str) -> int:
    """
    Day 18, Part 2:
    Две программы (p=0 и p=1), обмениваются через snd/rcv.
    Нужно вернуть, сколько раз программа 1 отправила значение.
    """
    prog = _parse_program(data)

    p0 = DuetProgram(0, prog)
    p1 = DuetProgram(1, prog)

    # Очереди сообщений: p0.queue — вход p0; p1.queue — вход p1.
    # snd p0 -> p1.queue; snd p1 -> p0.queue.
    while True:
        # Делаем шаги обеих программ
        p0.step(p1.queue)
        p1.step(p0.queue)

        # Условие тупика:
        # обе программы или завершились, или ждут, и очереди пусты
        if (
            (p0.terminated or p0.waiting)
            and (p1.terminated or p1.waiting)
            and not p0.queue
            and not p1.queue
        ):
            break

    return p1.send_count


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
