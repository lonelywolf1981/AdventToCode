from typing import List, Dict, Tuple, Optional, Callable


# ================== Intcode-компьютер с относительной базой ==================


def parse_program(data: str) -> List[int]:
    """
    Разбор Intcode-программы: числа через запятую (возможны переводы строк).
    """
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


class IntcodeComputer:
    def __init__(
        self,
        program: List[int],
        input_callback: Optional[Callable[[], int]] = None,
    ) -> None:
        self.mem = list(program)      # память
        self.ip = 0                   # instruction pointer
        self.relative_base = 0        # относительная база
        self.halted = False
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.input_callback = input_callback

    # --- работа с памятью ---

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

    # --- параметры ---

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

    # --- выполнение ---

    def run_until_output(self) -> Tuple[bool, Optional[int]]:
        """
        Выполняем программу, пока:
          - не получим НОВЫЙ вывод (opcode 4), или
          - не встретим opcode 99 (halt).

        Возвращаем:
          (halted: bool, output_value или None)
        """
        while True:
            if self.halted:
                return True, None

            instr = self._get(self.ip)
            opcode = instr % 100
            modes = instr // 100

            if opcode == 99:
                self.halted = True
                return True, None

            mode1 = modes % 10
            mode2 = (modes // 10) % 10
            mode3 = (modes // 100) % 10  # только для записи

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
                    if self.input_callback is not None:
                        # Берём новое значение джойстика/ввода из callback
                        self.inputs.append(self.input_callback())
                    else:
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
                return False, p1

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


# ================== Part 1 — подсчёт блоков ==================


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    program = parse_program(data)
    comp = IntcodeComputer(program)

    tiles: Dict[Tuple[int, int], int] = {}
    buffer: List[int] = []

    while True:
        halted, out = comp.run_until_output()
        if halted:
            break
        if out is None:
            continue

        buffer.append(out)
        if len(buffer) == 3:
            x, y, tile_id = buffer
            tiles[(x, y)] = tile_id
            buffer.clear()

    # считаем блоки (tile_id == 2)
    blocks = sum(1 for t in tiles.values() if t == 2)
    return str(blocks)


# ================== Part 2 — автоигра и финальный score ==================


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    program = parse_program(data)
    # играем "бесплатно"
    program[0] = 2

    # Эти переменные будут замыканием для callback'а ввода:
    ball_x: Optional[int] = None
    paddle_x: Optional[int] = None

    def joystick_ai() -> int:
        """
        Простейший автопилот: двигаем платформу за шариком.
        Вызывается в момент, когда программе реально нужен ввод.
        """
        nonlocal ball_x, paddle_x
        if ball_x is None or paddle_x is None:
            return 0
        if ball_x > paddle_x:
            return 1
        if ball_x < paddle_x:
            return -1
        return 0

    comp = IntcodeComputer(program, input_callback=joystick_ai)

    score = 0
    buffer: List[int] = []

    while True:
        halted, out = comp.run_until_output()
        if halted:
            break
        if out is None:
            continue

        buffer.append(out)
        if len(buffer) == 3:
            x, y, v = buffer
            buffer.clear()

            if x == -1 and y == 0:
                # обновление счёта
                score = v
            else:
                tile_id = v
                if tile_id == 3:
                    paddle_x = x
                elif tile_id == 4:
                    ball_x = x

    return str(score)


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
