BASE_PATTERN = [0, 1, 0, -1]


def parse_signal(data: str) -> list[int]:
    """
    Парсим входной сигнал: все цифры подряд.
    В input.txt обычно сигнал в одной строке.
    """
    line = "".join(data.split())  # на всякий случай убираем переводы строк и пробелы
    return [int(ch) for ch in line if ch.isdigit()]


def apply_phase(signal: list[int]) -> list[int]:
    """
    Применяем одну фазу преобразования по полному правилу (Part 1).
    Наивная O(n^2), но для длины ~650 и 100 фаз этого достаточно.
    """
    n = len(signal)
    out = [0] * n
    for i in range(n):
        repeat = i + 1
        s = 0
        # j — индекс входного сигнала (0..n-1)
        for j in range(n):
            # позиция в шаблоне (с пропуском самого первого элемента)
            k = (j + 1) // repeat
            pattern_val = BASE_PATTERN[k % 4]
            s += signal[j] * pattern_val
        out[i] = abs(s) % 10
    return out


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    signal = parse_signal(data)
    for _ in range(100):
        signal = apply_phase(signal)
    first8 = "".join(str(d) for d in signal[:8])
    return first8


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    base = parse_signal(data)
    if not base:
        return ""

    # Первые 7 цифр — смещение
    offset = int("".join(str(d) for d in base[:7]))

    # Строим повторённый 10000 раз сигнал
    full_len = len(base) * 10_000

    # По условиям AoC 2019 Day 16, offset во второй половине сигнала,
    # поэтому можно использовать "хвостовой" алгоритм.
    if offset < full_len // 2:
        # На всякий случай, если вдруг окажется не так для кастомного ввода.
        # Для стандартного инпута AoC сюда не попадём.
        # Можно было бы реализовать общий медленный алгоритм,
        # но он слишком тяжёлый для 10k повторов.
        raise ValueError("Offset находится в первой половине сигнала — быстрый алгоритм не работает.")

    # Нас интересует только хвост от offset до конца.
    tail_len = full_len - offset
    tail = [0] * tail_len
    # Заполняем хвост: он — это срез повторённого base
    # Индекс в полном сигнале: offset + i
    n_base = len(base)
    for i in range(tail_len):
        idx = (offset + i) % n_base
        tail[i] = base[idx]

    # 100 фаз, каждая — суффиксные суммы справа налево
    for _ in range(100):
        acc = 0
        for i in range(tail_len - 1, -1, -1):
            acc = (acc + tail[i]) % 10
            tail[i] = acc

    first8 = "".join(str(d) for d in tail[:8])
    return first8


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
