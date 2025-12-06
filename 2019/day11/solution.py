from typing import List, Dict, Tuple


# ================== Intcode-компьютер с относительной базой ==================


def parse_program(data: str) -> List[int]:
    """
    Разбор Intcode-программы: числа через запятую (возможны переводы строк).
    """
    cleaned = data.replace("\n", ",")
    return [int(x) for x in cleaned.split(",") if x.strip()]


class IntcodeComputer:
    def __init__(self, program: List[int]) -> None:
        self.mem = list(program)      # память
        self.ip = 0                   # instruction pointer
        self.relative_base = 0        # относительная база
        self.halted = False
        self.inputs: List[int] = []
        self.outputs: List[int] = []

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

    def run_until_output(self):
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
            mode3 = (modes // 100) % 10  # для записи

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


# ================== Логика робота-художника ==================


def run_robot(program: List[int], start_color: int) -> Dict[Tuple[int, int], int]:
    """
    Запускаем робота с заданным цветом стартовой панели.
    Возвращаем словарь: (x, y) -> color (0 или 1).
    """
    computer = IntcodeComputer(program)
    panels: Dict[Tuple[int, int], int] = {}

    # стартовая панель
    x, y = 0, 0
    panels[(x, y)] = start_color

    # направление: 0=вверх, 1=вправо, 2=вниз, 3=влево
    direction = 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    while True:
        # цвет текущей панели
        current_color = panels.get((x, y), 0)
        computer.add_input(current_color)

        # первый вывод — цвет для покраски
        halted, color_out = computer.run_until_output()
        if halted or color_out is None:
            break

        # второй вывод — поворот
        halted, turn_out = computer.run_until_output()
        if halted or turn_out is None:
            break

        # красим панель
        panels[(x, y)] = int(color_out)

        # поворот
        if turn_out == 0:
            direction = (direction - 1) % 4  # влево
        elif turn_out == 1:
            direction = (direction + 1) % 4  # вправо
        else:
            raise ValueError(f"Неизвестное направление поворота: {turn_out}")

        # шаг вперёд
        dx, dy = dirs[direction]
        x += dx
        y += dy

    return panels


# ================== Решения частей ==================


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    program = parse_program(data)
    panels = run_robot(program, start_color=0)  # стартовая панель чёрная
    # количество уникальных панелей, которые были хоть раз покрашены
    return str(len(panels))


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    program = parse_program(data)
    panels = run_robot(program, start_color=1)  # стартовая панель белая

    # Оставляем только белые панели
    white_points = [pos for pos, color in panels.items() if color == 1]
    if not white_points:
        return ""

    xs = [p[0] for p in white_points]
    ys = [p[1] for p in white_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    lines = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if panels.get((x, y), 0) == 1:
                row.append("█")
            else:
                row.append(" ")
        lines.append("".join(row))
    # Можно глазами прочитать буквы
    return "\n".join(lines)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:")
    print(solve_part2(raw))
