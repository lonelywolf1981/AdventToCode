from pathlib import Path
from typing import Dict


def _parse_input(data: str) -> Dict[int, int]:
    """
    Парсим строки вида:
      0: 3
      1: 2
      4: 4
      6: 4
    Возвращаем словарь {depth: range}.
    """
    layers: Dict[int, int] = {}

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        # Разделяем по ":"
        left, right = line.split(":")
        depth = int(left.strip())
        rng = int(right.strip())
        layers[depth] = rng

    if not layers:
        raise ValueError("Пустой input для Day 13")

    return layers


def _is_caught_at_layer(depth: int, rng: int, delay: int) -> bool:
    """
    Проверка: будет ли пакет пойман на слое depth при данном delay.
    Пакет приходит в слой depth в момент t = depth + delay.
    Сканер с диапазоном rng цикличен с period = 2 * (rng - 1).
    При t % period == 0 он в позиции 0, значит, ловит.
    Особый случай rng == 1: сканер всегда в позиции 0.
    """
    t = depth + delay
    if rng <= 1:
        # Диапазон 1: сканер никуда не двигается, всегда на 0.
        return True
    period = 2 * (rng - 1)
    return (t % period) == 0


def solve_part1(data: str) -> int:
    """
    Day 13, Part 1:
    Суммарная серьёзность (severity) при delay = 0.
    severity += depth * range для каждого слоя, где поймали.
    """
    layers = _parse_input(data)
    severity = 0

    for depth, rng in layers.items():
        if _is_caught_at_layer(depth, rng, delay=0):
            severity += depth * rng

    return severity


def solve_part2(data: str) -> int:
    """
    Day 13, Part 2:
    Найти минимальную задержку delay >= 0, при которой ни на одном слое
    пакет не будет пойман.
    """
    layers = _parse_input(data)

    delay = 0
    # Простой перебор delay; входы AoC 2017 проходят достаточно быстро.
    while True:
        caught = False
        for depth, rng in layers.items():
            if _is_caught_at_layer(depth, rng, delay):
                caught = True
                break
        if not caught:
            return delay
        delay += 1


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
