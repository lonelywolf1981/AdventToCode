from collections import deque
from typing import List, Optional, Tuple


def _parse_program(data: str) -> List[int]:
    """Парсим инткод-программу из input.txt."""
    return [int(x) for x in data.replace("\n", ",").split(",") if x.strip()]


class IntcodeComputer:
    """
    Инткод-компьютер с динамической памятью.
    Входная очередь хранится в self.in_queue, выводим пакеты тройками.
    """

    def __init__(self, program: List[int], address: int):
        # копия программы в виде списка (расширяем по мере надобности)
        self.mem = program[:]
        self.ip = 0
        self.rb = 0
        self.halted = False

        # входная очередь: первым элементом кладём адрес компьютера
        self.in_queue: deque[int] = deque([address])
        # буфер вывода (накапливаем до 3 значений)
        self.out_buf: List[int] = []

    # --- вспомогательные методы для работы с памятью ---

    def _ensure(self, idx: int) -> None:
        if idx < 0:
            raise IndexError("negative memory index")
        if idx >= len(self.mem):
            self.mem.extend([0] * (idx + 1 - len(self.mem)))

    def _load(self, idx: int) -> int:
        self._ensure(idx)
        return self.mem[idx]

    def _write(self, idx: int, value: int) -> None:
        self._ensure(idx)
        self.mem[idx] = value

    # --- один шаг инткода ---

    def step(self) -> Optional[Tuple[int, int, int]]:
        """
        Выполняет одну инструкцию.
        Возвращает пакет (dest, x, y), когда накоплено 3 вывода,
        иначе None.
        """
        if self.halted:
            return None

        ip = self.ip
        rb = self.rb

        def get_param(offset: int, mode: int) -> int:
            v = self._load(ip + offset)
            if mode == 0:      # позиционный
                return self._load(v)
            elif mode == 1:    # непосредственный
                return v
            elif mode == 2:    # относительный
                return self._load(rb + v)
            else:
                raise ValueError(f"unknown mode {mode}")

        def get_addr(offset: int, mode: int) -> int:
            v = self._load(ip + offset)
            if mode == 0:
                return v
            elif mode == 2:
                return rb + v
            else:
                # для записи режим 1 не используется
                raise ValueError(f"bad addr mode {mode}")

        instr = self._load(ip)
        opcode = instr % 100
        mode1 = (instr // 100) % 10
        mode2 = (instr // 1000) % 10
        mode3 = (instr // 10000) % 10

        if opcode == 99:
            self.halted = True
            return None

        if opcode in (1, 2, 7, 8):
            a = get_param(1, mode1)
            b = get_param(2, mode2)
            addr = get_addr(3, mode3)
            if opcode == 1:
                self._write(addr, a + b)
            elif opcode == 2:
                self._write(addr, a * b)
            elif opcode == 7:
                self._write(addr, 1 if a < b else 0)
            else:  # opcode == 8
                self._write(addr, 1 if a == b else 0)
            self.ip += 4

        elif opcode == 3:
            # ввод: либо из очереди, либо -1 если входов нет
            addr = get_addr(1, mode1)
            if self.in_queue:
                v = self.in_queue.popleft()
            else:
                v = -1
            self._write(addr, v)
            self.ip += 2

        elif opcode == 4:
            # вывод: собираем в буфер до тройки
            a = get_param(1, mode1)
            self.out_buf.append(a)
            self.ip += 2
            if len(self.out_buf) == 3:
                dest, x, y = self.out_buf
                self.out_buf = []
                return dest, x, y

        elif opcode in (5, 6):
            a = get_param(1, mode1)
            b = get_param(2, mode2)
            if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                self.ip = b
            else:
                self.ip += 3

        elif opcode == 9:
            a = get_param(1, mode1)
            rb += a
            self.rb = rb
            self.ip += 2

        else:
            raise RuntimeError(f"Unknown opcode {opcode} at ip={ip}")

        return None


# ===========================
#  ЧАСТЬ 1
# ===========================


def solve_part1(data: str) -> str:
    """
    Part 1: первое значение Y, попавшее в пакет с адресом 255.
    """
    program = _parse_program(data)
    comps = [IntcodeComputer(program, addr) for addr in range(50)]

    while True:
        for comp in comps:
            packet = comp.step()
            if packet is None:
                continue
            dest, x, y = packet
            if dest == 255:
                # первый пакет на 255 — ответ part 1
                return str(y)
            if 0 <= dest < 50:
                comps[dest].in_queue.append(x)
                comps[dest].in_queue.append(y)


# ===========================
#  ЧАСТЬ 2
# ===========================


def solve_part2(data: str) -> str:
    """
    Part 2: NAT:
      - перехватывает все пакеты на адрес 255 и запоминает последний (X, Y);
      - когда сеть простаивает, шлёт последний пакет на адрес 0;
      - нужно найти первый Y, который NAT отправляет на адрес 0 два раза подряд.
    """
    program = _parse_program(data)
    comps = [IntcodeComputer(program, addr) for addr in range(50)]

    nat_packet: Optional[Tuple[int, int]] = None
    last_nat_y: Optional[int] = None

    # Чем больше порог, тем «надёжнее» детект простоя.
    # 100 проверок без пакетов и входящих очередей оказалось достаточно стабильным.
    IDLE_THRESHOLD = 100
    idle_streak = 0

    while True:
        produced_any = False
        has_any_input = False

        for comp in comps:
            if comp.in_queue:
                has_any_input = True

            packet = comp.step()
            if packet is not None:
                produced_any = True
                dest, x, y = packet
                if dest == 255:
                    # NAT перехватывает, но не шлёт дальше сразу
                    nat_packet = (x, y)
                elif 0 <= dest < 50:
                    comps[dest].in_queue.append(x)
                    comps[dest].in_queue.append(y)

        # проверяем, не простаивает ли сеть
        if (not produced_any) and (not has_any_input):
            idle_streak += 1
        else:
            idle_streak = 0

        # сеть достаточно долго «молчит» — NAT будит её
        if idle_streak >= IDLE_THRESHOLD and nat_packet is not None:
            x, y = nat_packet
            comps[0].in_queue.append(x)
            comps[0].in_queue.append(y)

            if last_nat_y == y:
                # первый Y, который нат посылает на адрес 0 дважды подряд
                return str(y)
            last_nat_y = y


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
