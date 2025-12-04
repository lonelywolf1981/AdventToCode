from pathlib import Path
from typing import Dict, Tuple
import re


# Тип для правила: (write, move, next_state)
# move: -1 = left, +1 = right
Rule = Tuple[int, int, str]
StateRules = Dict[str, Dict[int, Rule]]


def _parse_input(data: str) -> Tuple[str, int, StateRules]:
    """
    Парсим описание машины Тьюринга из input.txt.

    Возвращает:
      (initial_state, steps, rules)

    rules: dict[state][current_value] = (write, move, next_state)
    """
    text = data.strip()
    if not text:
        raise ValueError("Пустой input для Day 25")

    # Начальное состояние
    m_state = re.search(r"Begin in state ([A-Z])\.", text)
    if not m_state:
        raise ValueError("Не удалось найти начальное состояние")
    initial_state = m_state.group(1)

    # Количество шагов
    m_steps = re.search(
        r"Perform a diagnostic checksum after (\d+) steps\.", text
    )
    if not m_steps:
        raise ValueError("Не удалось найти количество шагов для checksum")
    steps = int(m_steps.group(1))

    # Парсим блоки состояний
    # Разобьём по "In state X:"
    # Первый блок (с заголовком) найдём через regex с DOTALL
    state_blocks = re.split(r"\n\s*\n", text)  # грубое разбиение по пустым строкам

    rules: StateRules = {}

    # Ищем блоки, начинающиеся с "In state X:"
    state_block_re = re.compile(
        r"In state ([A-Z]):\s*"
        r"If the current value is 0:\s*"
        r"- Write the value (\d)\.\s*"
        r"- Move one slot to the (right|left)\.\s*"
        r"- Continue with state ([A-Z])\.\s*"
        r"If the current value is 1:\s*"
        r"- Write the value (\d)\.\s*"
        r"- Move one slot to the (right|left)\.\s*"
        r"- Continue with state ([A-Z])\.",
        re.MULTILINE,
    )

    for match in state_block_re.finditer(text):
        (
            state,
            w0,
            move0,
            next0,
            w1,
            move1,
            next1,
        ) = match.groups()

        write0 = int(w0)
        write1 = int(w1)
        move0_dir = 1 if move0 == "right" else -1
        move1_dir = 1 if move1 == "right" else -1

        rules[state] = {
            0: (write0, move0_dir, next0),
            1: (write1, move1_dir, next1),
        }

    if not rules:
        raise ValueError("Не удалось разобрать ни одного блока 'In state X:'")

    return initial_state, steps, rules


def _run_machine(initial_state: str, steps: int, rules: StateRules) -> int:
    """
    Запускаем машину Тьюринга:
      - лента бесконечна, изначально всё 0
      - позиция = 0
      - после 'steps' шагов возвращаем количество 1 на ленте.
    """
    # Ленту удобно хранить как множество позиций со значением 1.
    tape_ones = set()  # set[int]
    pos = 0
    state = initial_state

    for _ in range(steps):
        current_val = 1 if pos in tape_ones else 0

        if state not in rules:
            raise RuntimeError(f"Нет правил для состояния {state!r}")
        if current_val not in rules[state]:
            raise RuntimeError(f"Нет правила для состояния {state!r} и значения {current_val}")

        write, move, next_state = rules[state][current_val]

        # Записываем
        if write == 1:
            tape_ones.add(pos)
        else:
            tape_ones.discard(pos)

        # Двигаемся
        pos += move

        # Переходим в следующее состояние
        state = next_state

    # checksum = количество 1 на ленте
    return len(tape_ones)


def solve_part1(data: str) -> int:
    """
    Day 25, Part 1:
    Диагностический checksum после заданного числа шагов.
    """
    initial_state, steps, rules = _parse_input(data)
    return _run_machine(initial_state, steps, rules)


def solve_part2(data: str) -> int:
    """
    Day 25:
    В оригинальном AoC 2017 у дня 25 только одна часть.
    Для совместимости с твоим start.py вернём тот же checksum.
    """
    return solve_part1(data)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
