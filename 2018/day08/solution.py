from pathlib import Path
from typing import Tuple, List


def parse_input(data: str) -> List[int]:
    """
    Разбираем input.txt в список чисел.
    """
    nums: List[int] = []
    for part in data.replace("\n", " ").split():
        nums.append(int(part))
    return nums


def parse_node(nums: List[int], pos: int) -> Tuple[int, int, int]:
    """
    Рекурсивно разбирает узел.
    Возвращает:
        total_metadata_sum — сумма метаданных в поддереве
        node_value — значение этого узла по правилам части 2
        new_pos — позиция после разбора узла
    """
    child_count = nums[pos]
    metadata_count = nums[pos + 1]
    pos += 2

    children_values = []
    total_metadata_sum = 0

    # Парсим детей
    for _ in range(child_count):
        t_sum, val, pos = parse_node(nums, pos)
        total_metadata_sum += t_sum
        children_values.append(val)

    # Метаданные
    metadata = nums[pos: pos + metadata_count]
    pos += metadata_count

    # Добавляем сумму метаданных в общий счёт (для Part 1)
    total_metadata_sum += sum(metadata)

    # Значение узла для Part 2
    if child_count == 0:
        # значение = сумма метаданных
        node_value = sum(metadata)
    else:
        # метаданные — индексы детей (1-based)
        node_value = 0
        for m in metadata:
            idx = m - 1
            if 0 <= idx < child_count:
                node_value += children_values[idx]

    return total_metadata_sum, node_value, pos


def solve_part1(data: str) -> str:
    nums = parse_input(data)
    if not nums:
        return "0"

    total_metadata, _, _ = parse_node(nums, 0)
    return str(total_metadata)


def solve_part2(data: str) -> str:
    nums = parse_input(data)
    if not nums:
        return "0"

    _, value, _ = parse_node(nums, 0)
    return str(value)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
