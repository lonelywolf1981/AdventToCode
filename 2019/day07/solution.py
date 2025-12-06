from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import itertools


# ================== Вспомогательные функции и классы ==================


def parse_program(data: str) -> List[int]:
    """
    Разбор Intcode-программы: числа через запятую (возможны переводы строк).
    """
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


@dataclass
class IntcodeComputer:
    memory: List[int]
    ip: int = 0
    halted: bool = False
    inputs: List[int] = field(default_factory=list)
    outputs: List[int] = field(default_factory=list)

    def add_input(self, value: int) -> None:
        self.inputs.append(value)

    def _get_param(self, mode: int, offset: int) -> int:
        val = self.memory[self.ip + offset]
        if mode == 0:  # позиционный
            return self.memory[val]
        elif mode == 1:  # непосредственный
            return val
        else:
            raise ValueError(f"Неизвестный режим параметра: {mode}")

    def _get_addr(self, offset: int) -> int:
        # В этой задаче адрес для записи всегда позиционный
        return self.memory[self.ip + offset]

    def run_until_output_or_halt(self) -> Tuple[bool, Optional[int]]:
        """
        Выполняем программу, пока:
          - не получим НОВЫЙ вывод (opcode 4), или
          - не встретим opcode 99 (halt).

        Возвращаем:
          (halted, output_value_or_None)
        """
        while True:
            if self.halted:
                return True, None

            instr = self.memory[self.ip]
            opcode = instr % 100
            modes = instr // 100

            if opcode == 99:
                self.halted = True
                return True, None

            mode1 = modes % 10
            mode2 = (modes // 10) % 10
            mode3 = (modes // 100) % 10  # на будущее не нужен

            if opcode in (1, 2, 7, 8):
                p1 = self._get_param(mode1, 1)
                p2 = self._get_param(mode2, 2)
                out_addr = self._get_addr(3)

                if opcode == 1:      # add
                    self.memory[out_addr] = p1 + p2
                elif opcode == 2:    # mul
                    self.memory[out_addr] = p1 * p2
                elif opcode == 7:    # less than
                    self.memory[out_addr] = 1 if p1 < p2 else 0
                elif opcode == 8:    # equals
                    self.memory[out_addr] = 1 if p1 == p2 else 0

                self.ip += 4

            elif opcode == 3:
                # input
                if not self.inputs:
                    raise RuntimeError("Нет входных данных для opcode 3")
                out_addr = self._get_addr(1)
                self.memory[out_addr] = self.inputs.pop(0)
                self.ip += 2

            elif opcode == 4:
                # output
                p1 = self._get_param(mode1, 1)
                self.outputs.append(p1)
                self.ip += 2
                return False, p1  # не halt, но появился вывод

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

            else:
                raise ValueError(f"Неизвестный opcode {opcode} на позиции {self.ip}")


def run_amplifiers_chain(program: List[int], phases: List[int]) -> int:
    """
    Часть 1: линейная цепочка усилителей A -> B -> C -> D -> E.
    Каждый усилитель:
      входы: [phase, input_signal]
    На вход A подаём 0, берём выход E.
    """
    signal = 0
    for phase in phases:
        comp = IntcodeComputer(memory=program.copy())
        comp.add_input(phase)
        comp.add_input(signal)

        last_output = None
        # Полностью прогоняем программу усилителя
        while not comp.halted:
            halted, out = comp.run_until_output_or_halt()
            if out is not None:
                last_output = out
            if halted:
                break

        if last_output is None:
            raise RuntimeError("Усилитель не выдал выходной сигнал")
        signal = last_output
    return signal


def run_amplifiers_feedback(program: List[int], phases: List[int]) -> int:
    """
    Часть 2: усилители подключены кольцом (feedback loop).
    Начальный вход для A: 0.
    Каждый усилитель:
      - один раз получает phase при запуске,
      - далее получает сигналы от предыдущего усилителя.
    Ответ — последний сигнал от E перед его завершением.
    """
    amps = [IntcodeComputer(memory=program.copy()) for _ in range(5)]

    # Первичный ввод фаз
    for comp, phase in zip(amps, phases):
        comp.add_input(phase)

    signal = 0
    last_output_from_E = 0
    idx = 0  # текущий усилитель

    while True:
        comp = amps[idx]
        comp.add_input(signal)

        halted, out = comp.run_until_output_or_halt()
        if out is not None:
            signal = out
            if idx == 4:  # E
                last_output_from_E = signal

        if all(a.halted for a in amps):
            break

        idx = (idx + 1) % 5

    return last_output_from_E


# ================== Решения частей ==================


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    program = parse_program(data)
    best = 0
    for phases in itertools.permutations(range(5), 5):
        out = run_amplifiers_chain(program, list(phases))
        if out > best:
            best = out
    return str(best)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    program = parse_program(data)
    best = 0
    for phases in itertools.permutations(range(5, 10), 5):
        out = run_amplifiers_feedback(program, list(phases))
        if out > best:
            best = out
    return str(best)


# ================== Твой стандартный шаблон запуска ==================


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
