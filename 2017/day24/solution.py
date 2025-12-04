from pathlib import Path
from typing import List, Tuple


def _parse_input(data: str) -> List[Tuple[int, int]]:
    """
    Парсим строки формата "A/B" в список компонентов (A, B).
    """
    components: List[Tuple[int, int]] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        left, right = line.split("/")
        a = int(left)
        b = int(right)
        components.append((a, b))
    if not components:
        raise ValueError("Пустой input для Day 24")
    return components


def _search_best(components: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Перебираем все возможные мосты DFS-ом.

    Возвращаем:
      (max_strength_any, max_strength_among_longest)

    max_strength_any            — максимальная сила моста (Part 1).
    max_strength_among_longest  — сила среди самых длинных мостов (Part 2).
    """
    n = len(components)
    used = [False] * n

    def dfs(port: int) -> Tuple[int, int, int]:
        """
        DFS от текущего открытого порта `port`.

        Возвращает:
          (best_any, best_len, best_len_str)

        best_any     — максимальная сила моста, который можно построить отсюда
                       (без учёта уже добавленных сверху компонентов).
        best_len     — максимальная длина (число деталей) среди мостов отсюда.
        best_len_str — сила среди *самых длинных* мостов отсюда.
        """
        best_any = 0          # для Part 1
        best_len = 0          # длина лучшего по длине моста
        best_len_str = 0      # сила лучшего по длине моста

        for i, (a, b) in enumerate(components):
            if used[i]:
                continue
            if a != port and b != port:
                continue

            used[i] = True
            next_port = b if a == port else a

            child_any, child_len, child_len_str = dfs(next_port)

            used[i] = False

            strength_here_any = child_any + a + b  # для Part 1
            length_here = child_len + 1
            strength_here_len = child_len_str + a + b  # сила для длинного варианта

            # Обновляем общий максимум силы (Part 1)
            if strength_here_any > best_any:
                best_any = strength_here_any

            # Обновляем максимум для пары (длина, сила) (Part 2)
            if length_here > best_len:
                best_len = length_here
                best_len_str = strength_here_len
            elif length_here == best_len and strength_here_len > best_len_str:
                best_len_str = strength_here_len

        # Если дальше нет компонентов — остаёмся с нулями (0 длина, 0 сила)
        return best_any, best_len, best_len_str

    max_any, _, max_longest = dfs(0)
    return max_any, max_longest


def solve_part1(data: str) -> int:
    """
    Day 24, Part 1:
    Максимальная сила моста, начинающегося с порта 0.
    """
    components = _parse_input(data)
    max_any, _ = _search_best(components)
    return max_any


def solve_part2(data: str) -> int:
    """
    Day 24, Part 2:
    Среди самых длинных мостов (по числу деталей) берём самый сильный.
    """
    components = _parse_input(data)
    _, max_longest = _search_best(components)
    return max_longest


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
