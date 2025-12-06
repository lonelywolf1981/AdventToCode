from typing import List


def parse_program(data: str) -> List[int]:
    """
    Разбор Intcode-программы: числа через запятую (возможны переводы строк).
    """
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


class IntcodeComputer:
    def __init__(self, program: List[int]) -> None:
        # Копируем программу и используем "растягиваемый" список как память
        self.mem = list(program)
        self.ip = 0               # instruction pointer
        self.relative_base = 0    # относительный базис
        self.halted = False
        self.inputs: List[int] = []
        self.outputs: List[int] = []

    # ---------- работа с памятью ----------

    def _ensure_mem(self, addr: int) -> None:
        if addr < 0:
            raise IndexError("Отрицательный адрес памяти")
        if addr >= len(self.mem):
            self.mem.extend([0] * (addr + 1 - len(self.mem)))

    def _get(self, addr: int) -> int:
        self._ensure_mem(addr)
        return self.mem[addr]

    def _set(self, addr: int, value: int) -> None:
        self._ensure_mem(addr)
        self.mem[addr] = value

    # ---------- параметры и выполнение ----------

    def add_input(self, value: int) -> None:
        self.inputs.append(value)

    def _get_param(self, mode: int, offset: int) -> int:
        """
        mode:
          0 - позиционный
          1 - непосредственный
          2 - относительный (relative_base + значение)
        """
        raw = self._get(self.ip + offset)
        if mode == 0:   # позиционный
            return self._get(raw)
        elif mode == 1:  # непосредственный
            return raw
        elif mode == 2:  # относительный
            return self._get(self.relative_base + raw)
        else:
            raise ValueError(f"Неизвестный режим параметра: {mode}")

    def _get_write_addr(self, mode: int, offset: int) -> int:
        """
        Адрес для записи: учитываем режимы 0 и 2.
        (режим 1 для записи не используется).
        """
        raw = self._get(self.ip + offset)
        if mode == 0:
            return raw
        elif mode == 2:
            return self.relative_base + raw
        else:
            raise ValueError(f"Недопустимый режим для записи: {mode}")

    def run(self) -> None:
        """
        Выполнить программу до остановки (opcode 99).
        Все выводы сохраняются в self.outputs.
        """
        while not self.halted:
            instr = self._get(self.ip)
            opcode = instr % 100
            modes = instr // 100

            if opcode == 99:
                self.halted = True
                break

            mode1 = modes % 10
            mode2 = (modes // 10) % 10
            mode3 = (modes // 100) % 10  # пригодится только для записи

            if opcode in (1, 2, 7, 8):
                # три параметра: два чтения, одна запись
                p1 = self._get_param(mode1, 1)
                p2 = self._get_param(mode2, 2)
                out_addr = self._get_write_addr(mode3, 3)

                if opcode == 1:      # add
                    self._set(out_addr, p1 + p2)
                elif opcode == 2:    # mul
                    self._set(out_addr, p1 * p2)
                elif opcode == 7:    # less than
                    self._set(out_addr, 1 if p1 < p2 else 0)
                elif opcode == 8:    # equals
                    self._set(out_addr, 1 if p1 == p2 else 0)

                self.ip += 4

            elif opcode == 3:
                # input
                if not self.inputs:
                    raise RuntimeError("Нет входных данных для opcode 3")
                out_addr = self._get_write_addr(mode1, 1)
                value = self.inputs.pop(0)
                self._set(out_addr, value)
                self.ip += 2

            elif opcode == 4:
                # output
                p1 = self._get_param(mode1, 1)
                self.outputs.append(p1)
                self.ip += 2

            elif opcode in (5, 6):
                # jumps
                p1 = self._get_param(mode1, 1)
                p2 = self._get_param(mode2, 2)

                if opcode == 5:  # jump-if-true
                    if p1 != 0:
                        self.ip = p2
                    else:
                        self.ip += 3
                elif opcode == 6:  # jump-if-false
                    if p1 == 0:
                        self.ip = p2
                    else:
                        self.ip += 3

            elif opcode == 9:
                # adjust relative base
                p1 = self._get_param(mode1, 1)
                self.relative_base += p1
                self.ip += 2

            else:
                raise ValueError(f"Неизвестный opcode {opcode} на позиции {self.ip}")


# ================== Решения частей ==================


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    program = parse_program(data)
    comp = IntcodeComputer(program)
    comp.add_input(1)  # BOOST keycode (часть 1)
    comp.run()

    if not comp.outputs:
        return "no output"

    return str(comp.outputs[-1])


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    program = parse_program(data)
    comp = IntcodeComputer(program)
    comp.add_input(2)  # режим для второй части
    comp.run()

    if not comp.outputs:
        return "no output"

    return str(comp.outputs[-1])


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
