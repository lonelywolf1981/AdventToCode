from collections import deque
from pathlib import Path
from typing import Tuple


def parse_input(data: str) -> Tuple[int, int]:
    """
    Ожидаемый формат AoC 2018 Day 9:
    '10 players; last marble is worth 1618 points'
    Берём первые два числа: количество игроков и номер последнего мрамора.
    """
    nums = []
    for part in data.replace("\n", " ").split():
        if part.isdigit():
            nums.append(int(part))
    if len(nums) < 2:
        return 0, 0
    players, last_marble = nums[0], nums[1]
    return players, last_marble


def play_game(players: int, last_marble: int) -> int:
    """
    Эмуляция игры.
    Используем deque для эффективных операций вставки/удаления по кругу.
    """
    if players <= 0 or last_marble <= 0:
        return 0

    scores = [0] * players
    circle = deque([0])  # текущий мрамор считается "на конце" deque

    for marble in range(1, last_marble + 1):
        player = (marble - 1) % players

        if marble % 23 == 0:
            # Особый ход: отматываем на 7 CCW, забираем мрамор
            circle.rotate(7)
            removed = circle.pop()
            scores[player] += marble + removed
            # Новый текущий — мрамор справа от удалённого
            circle.rotate(-1)
        else:
            # Обычный ход: сдвиг на 1 CW и вставка мрамора
            circle.rotate(-1)
            circle.append(marble)

    return max(scores)


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    players, last_marble = parse_input(data)
    result = play_game(players, last_marble)
    return str(result)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    players, last_marble = parse_input(data)
    last_marble *= 100
    result = play_game(players, last_marble)
    return str(result)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
