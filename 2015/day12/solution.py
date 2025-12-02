import json


def sum_all(item):
    """
    Суммирует все числа в структуре JSON (часть 1).
    """
    if isinstance(item, int):
        return item
    if isinstance(item, list):
        return sum(sum_all(x) for x in item)
    if isinstance(item, dict):
        return sum(sum_all(v) for v in item.values())
    return 0


def sum_without_red(item):
    """
    Суммирует все числа, игнорируя объекты, содержащие "red" (часть 2).
    """
    if isinstance(item, int):
        return item
    if isinstance(item, list):
        return sum(sum_without_red(x) for x in item)

    if isinstance(item, dict):
        # Если среди значений есть "red", весь объект исключаем
        if "red" in item.values():
            return 0
        return sum(sum_without_red(v) for v in item.values())

    return 0


def solve_part1(data: str) -> str:
    obj = json.loads(data)
    return str(sum_all(obj))


def solve_part2(data: str) -> str:
    obj = json.loads(data)
    return str(sum_without_red(obj))


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

