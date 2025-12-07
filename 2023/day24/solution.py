import re
from itertools import combinations
from fractions import Fraction


def _parse_stones(data: str):
    stones = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        nums = list(map(int, re.findall(r"-?\d+", line)))
        x, y, z, vx, vy, vz = nums
        stones.append((x, y, z, vx, vy, vz))
    return stones


def solve_part1(data: str) -> str:
    # Разбор входа
    stones = _parse_stones(data)

    # Диапазон из основной задачи AoC 2023 Day 24
    # Для примерного входа из условия диапазон другой.
    LO = 200000000000000
    HI = 400000000000000

    ans = 0

    # Перебираем все пары частиц
    for (x1, y1, _z1, vx1, vy1, _vz1), (x2, y2, _z2, vx2, vy2, _vz2) in combinations(stones, 2):
        # Решаем пересечение двух траекторий в плоскости XY:
        # x1 + vx1 * t1 = x2 + vx2 * t2
        # y1 + vy1 * t1 = y2 + vy2 * t2

        det = vx1 * vy2 - vy1 * vx2
        if det == 0:
            # Параллельны или совпадают в XY — не считаем
            continue

        t1 = ((x2 - x1) * vy2 - (y2 - y1) * vx2) / det
        t2 = ((x2 - x1) * vy1 - (y2 - y1) * vx1) / det

        # Нас интересует будущее
        if t1 <= 0 or t2 <= 0:
            continue

        ix = x1 + vx1 * t1
        iy = y1 + vy1 * t1

        if LO <= ix <= HI and LO <= iy <= HI:
            ans += 1

    return str(ans)


# ---------- Вспомогательные функции для Part 2 ----------

def _cross(s, v):
    """Векторное произведение s × v."""
    sx, sy, sz = s
    vx, vy, vz = v
    return (
        sy * vz - sz * vy,
        sz * vx - sx * vz,
        sx * vy - sy * vx,
    )


def _gauss_solve_6x6(M, B):
    """
    Решает систему 6x6 с помощью Гаусса.
    M — список из 6 строк по 6 Fraction,
    B — список из 6 Fraction.
    Возвращает список из 6 Fraction или None, если матрица вырождена.
    """
    n = 6

    for col in range(n):
        # Находим опорный элемент
        pivot = None
        for row in range(col, n):
            if M[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return None  # сингулярная матрица

        # Перестановка строк
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            B[col], B[pivot] = B[pivot], B[col]

        # Нормируем ведущую строку
        div = M[col][col]
        for j in range(col, n):
            M[col][j] /= div
        B[col] /= div

        # Обнуляем столбец в остальных строках
        for row in range(n):
            if row == col:
                continue
            factor = M[row][col]
            if factor == 0:
                continue
            for j in range(col, n):
                M[row][j] -= factor * M[col][j]
            B[row] -= factor * B[col]

    # Теперь M ~ I, решение в B
    return B


def _solve_rock(stones):
    """
    Находит координаты скалы (rx, ry, rz) и скорость (rvx, rvy, rvz)
    по списку камней (x, y, z, vx, vy, vz), используя
    линейную систему из условий коллинеарности.
    """

    n = len(stones)
    if n < 3:
        raise ValueError("Для Part 2 нужно минимум 3 камня")

    # Перебираем тройки камней, чтобы избежать вырожденных случаев
    for i1 in range(n):
        for i2 in range(i1 + 1, n):
            for i3 in range(i2 + 1, n):
                pairs = [(i1, i2), (i1, i3)]  # две пары => 6 уравнений

                rows = []
                rhs = []

                for a, b in pairs:
                    sx1, sy1, sz1, vx1, vy1, vz1 = stones[a]
                    sx2, sy2, sz2, vx2, vy2, vz2 = stones[b]

                    # Вектора
                    A = (sx1 - sx2, sy1 - sy2, sz1 - sz2)          # s1 - s2
                    Bv = (vx1 - vx2, vy1 - vy2, vz1 - vz2)         # v1 - v2
                    C1 = _cross((sx1, sy1, sz1), (vx1, vy1, vz1))  # s1 × v1
                    C2 = _cross((sx2, sy2, sz2), (vx2, vy2, vz2))  # s2 × v2
                    C = (C1[0] - C2[0], C1[1] - C2[1], C1[2] - C2[2])

                    Ax, Ay, Az = A
                    Bx, By, Bz = Bv
                    Cx, Cy, Cz = C

                    # Для X:
                    # (A × rv)_x + (r0 × B)_x = Cx
                    # Ay*rvz - Az*rvy + ry*Bz - rz*By = Cx
                    row_x = [0, Bz, -By, 0, -Az, Ay]  # [rx, ry, rz, rvx, rvy, rvz]
                    rows.append(row_x)
                    rhs.append(Cx)

                    # Для Y:
                    # (A × rv)_y + (r0 × B)_y = Cy
                    # Az*rvx - Ax*rvz + rz*Bx - rx*Bz = Cy
                    row_y = [-Bz, 0, Bx, Az, 0, -Ax]
                    rows.append(row_y)
                    rhs.append(Cy)

                    # Для Z:
                    # (A × rv)_z + (r0 × B)_z = Cz
                    # Ax*rvy - Ay*rvx + rx*By - ry*Bx = Cz
                    row_z = [By, -Bx, 0, -Ay, Ax, 0]
                    rows.append(row_z)
                    rhs.append(Cz)

                # В Fraction и решаем
                M = [[Fraction(v) for v in row] for row in rows]
                Bvec = [Fraction(v) for v in rhs]

                sol = _gauss_solve_6x6(M, Bvec)
                if sol is None:
                    continue

                rx, ry, rz, rvx, rvy, rvz = sol
                return rx, ry, rz, rvx, rvy, rvz

    raise RuntimeError("Не удалось найти невырожденную систему для скалы")


def solve_part2(data: str) -> str:
    stones = _parse_stones(data)

    rx, ry, rz, _rvx, _rvy, _rvz = _solve_rock(stones)

    s = rx + ry + rz  # по условию ответ = сумма координат скалы

    if isinstance(s, Fraction):
        if s.denominator != 1:
            value = s.numerator // s.denominator
        else:
            value = s.numerator
    else:
        value = int(round(s))

    return str(value)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip("\n")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
