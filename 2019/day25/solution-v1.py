def solve_part1(data: str) -> str:
    """
    Day 25 — интерактивный текстовый квест.
    Автоматически решить его внутри solve_part1 невозможно.
    Чтобы получить код, нужно запустить solution.py вручную.
    """
    return "Запусти solution.py вручную для интерактивного прохождения квеста."


def solve_part2(data: str) -> str:
    """
    Во второй части Day 25 нет числового ответа.
    Нужно только собрать все 50 звёзд.
    """
    return "У Day 25 нет отдельного ответа Part 2 — требуется лишь собрать все 50 звёзд."


# ----------- Интерактивная игра (запускать напрямую!) -----------

from collections import deque

def parse_program(text: str):
    return [int(x) for x in text.replace("\n", ",").split(",") if x.strip()]


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
                    return  # ждём инпут пользователя
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


def print_ascii(out):
    s = "".join(chr(c) if 0 <= c < 256 else f"[{c}]" for c in out)
    print(s, end="")


if __name__ == "__main__":
    from pathlib import Path

    path = Path(__file__).resolve().parent / ("input.txt")
    if not path.exists():
        print("input.txt отсутствует")
        exit()

    code = parse_program(path.read_text())
    comp = Intcode(code)

    # первая порция вывода
    comp.run_until_input()
    print_ascii(comp.out)
    comp.out.clear()

    while not comp.halted:
        cmd = input("\nCommand> ")
        if cmd.strip().lower() in ("exit", "quit"):
            break

        for ch in cmd:
            comp.inp.append(ord(ch))
        comp.inp.append(ord("\n"))

        comp.run_until_input()
        print_ascii(comp.out)
        comp.out.clear()
