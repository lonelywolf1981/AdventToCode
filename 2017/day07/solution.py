from pathlib import Path
from typing import Dict, List, Tuple
import re
from collections import Counter


# Тип: имя -> (собственный вес, список детей)
NodeMap = Dict[str, Tuple[int, List[str]]]


def _parse_input(data: str) -> NodeMap:
    """
    Разбираем строки вида:
      fwft (72) -> ktlj, cntj, xhth
      pbga (66)
    В словарь: name -> (weight, [children...])
    """
    nodes: NodeMap = {}

    line_re = re.compile(r"^([a-z]+)\s+\((\d+)\)(?:\s*->\s*(.*))?$")

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        m = line_re.match(line)
        if not m:
            raise ValueError(f"Непонятная строка: {line!r}")

        name = m.group(1)
        weight = int(m.group(2))
        children_str = m.group(3)

        if children_str:
            children = [c.strip() for c in children_str.split(",")]
        else:
            children = []

        nodes[name] = (weight, children)

    if not nodes:
        raise ValueError("Пустой input для Day 7")

    return nodes


def _find_root(nodes: NodeMap) -> str:
    """
    Корень — тот, кто ни разу не встречается в списках детей.
    """
    all_names = set(nodes.keys())
    child_names = set()

    for _, (_, children) in nodes.items():
        child_names.update(children)

    roots = list(all_names - child_names)
    if len(roots) != 1:
        # На AoC гарантированно один, но на всякий — проверка
        raise ValueError(f"Ожидался один корень, найдено: {roots}")

    return roots[0]


def _total_weight_and_correction(
    name: str, nodes: NodeMap
) -> Tuple[int, int | None]:
    """
    Рекурсивно возвращает:
      (total_weight, correction)
    total_weight — суммарный вес поддерева.
    correction  — если найдено несбалансированное место,
                  здесь будет КАКИМ должен быть СОБСТВЕННЫЙ вес
                  проблемного узла; дальше по стеку просто пробрасываем.
    """
    weight, children = nodes[name]

    # Лист
    if not children:
        return weight, None

    child_totals: List[Tuple[str, int]] = []

    for child in children:
        t_weight, corr = _total_weight_and_correction(child, nodes)
        # Если ниже по дереву уже нашли корректировку — пробрасываем наверх
        if corr is not None:
            return 0, corr
        child_totals.append((child, t_weight))

    totals = [tw for _, tw in child_totals]

    # Все дети уже сбалансированы между собой
    if len(set(totals)) == 1:
        return weight + sum(totals), None

    # Здесь впервые нашли несбалансированное место — надо вычислить корректный вес.
    counter = Counter(totals)

    # Ожидаем, что одна величина встречается 1 раз (неправильная),
    # а другая — несколько раз (правильная).
    correct_total = None
    wrong_total = None

    for val, cnt in counter.items():
        if cnt == 1:
            wrong_total = val
        else:
            correct_total = val

    if correct_total is None or wrong_total is None:
        raise RuntimeError("Не удалось определить неверный/правильный вес детей")

    # Находим имя проблемного ребёнка
    wrong_child = None
    for child_name, t in child_totals:
        if t == wrong_total:
            wrong_child = child_name
            break

    if wrong_child is None:
        raise RuntimeError("Не найден проблемный ребёнок при несбалансированном узле")

    child_weight, _ = nodes[wrong_child]

    # wrong_total - это (child_weight + weight_его_поддерева_без_него),
    # correct_total - это правильная сумма.
    # Хотим изменить child_weight так, чтобы новый total стал correct_total.
    # diff = wrong_total - correct_total
    # новый_вес = child_weight - diff
    diff = wrong_total - correct_total
    corrected_weight = child_weight - diff

    # Возвращаем correction, total можно не использовать (ставим 0)
    return 0, corrected_weight


def solve_part1(data: str) -> str:
    """
    Day 7, Part 1:
    Имя самого нижнего диска (корень дерева).
    """
    nodes = _parse_input(data)
    root = _find_root(nodes)
    return root


def solve_part2(data: str) -> int:
    """
    Day 7, Part 2:
    Собственный вес проблемного диска, при котором вся башня станет сбалансированной.
    """
    nodes = _parse_input(data)
    root = _find_root(nodes)
    _, correction = _total_weight_and_correction(root, nodes)

    if correction is None:
        raise RuntimeError("Не удалось найти несбалансированный узел")

    return correction


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
