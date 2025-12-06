from __future__ import annotations


def parse_instructions(data: str):
    lines = []
    for line in data.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return lines


# Объединяем все операции в общее линейное преобразование вида:
#   x -> (a * x + b) mod M
def combine_shuffle(instructions, M):
    a = 1
    b = 0

    for line in instructions:
        if line == "deal into new stack":
            # x -> -x - 1
            a = (-a) % M
            b = (-b - 1) % M
        elif line.startswith("cut"):
            n = int(line.split()[1])
            # x -> x - n
            b = (b - n) % M
        elif line.startswith("deal with increment"):
            n = int(line.split()[-1])
            # x -> x * n
            a = (a * n) % M
            b = (b * n) % M
        else:
            raise ValueError("Unknown instruction: " + line)

    return a, b


# Возведение линейного отображения f(x) = a*x + b к степени k:
# f^k(x) = A*x + B
def repeat_shuffle(a, b, M, k):
    # Используем бинарную экспоненту
    A = 1
    B = 0

    while k > 0:
        if (k & 1) != 0:
            # A,B = compose(A,B with a,b)
            A = (A * a) % M
            B = (B * a + b) % M

        # Составляем (a,b) с самим собой
        b_new = (b * (a + 1)) % M if a == 1 else (b * (a + 1)) % M

        # Правильно: f(f(x)) = a*(a*x+b) + b = a^2 x + (a*b + b)
        b_new = (a * b + b) % M
        a_new = (a * a) % M

        a, b = a_new, b_new
        k >>= 1

    return A, B


def modinv(x, mod):
    # обратный элемент по Ферма/Евклиду
    return pow(x, mod - 2, mod)


def solve_part1(data: str) -> str:
    instructions = parse_instructions(data)
    M = 10007
    a, b = combine_shuffle(instructions, M)
    # ищем позицию карты 2019
    # pos = (a*2019 + b) mod M
    pos = (a * 2019 + b) % M
    return str(pos)


def solve_part2(data: str) -> str:
    instructions = parse_instructions(data)

    M = 119315717514047
    K = 101741582076661  # repeat count
    target_pos = 2020

    # Применим операции "в обратную сторону".
    # Переворачиваем инверсно: x -> (x - b)*a^{-1}.
    a, b = combine_shuffle(instructions, M)
    inv_a = modinv(a, M)

    # Одно «обратное» преобразование:
    # old = (x - b) * inv_a
    # => old = (inv_a * x - inv_a*b)
    a_r = inv_a % M
    b_r = (-inv_a * b) % M

    # Повторяем K раз
    A, B = repeat_shuffle(a_r, b_r, M, K)

    # Теперь карта, оказавшаяся на позиции target_pos:
    val = (A * target_pos + B) % M
    return str(val)


# ================== TEMPLATE ==================

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
