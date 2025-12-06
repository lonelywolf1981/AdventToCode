WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT


def parse_layers(data: str):
    """
    Разбиваем строку на слои фиксированного размера.
    """
    digits = data.strip()
    layers = []
    for i in range(0, len(digits), LAYER_SIZE):
        layer = digits[i:i + LAYER_SIZE]
        if len(layer) == LAYER_SIZE:
            layers.append(layer)
    return layers


def solve_part1(data: str) -> str:
    layers = parse_layers(data)
    if not layers:
        return "0"

    # Ищем слой с минимальным количеством '0'
    best_layer = min(layers, key=lambda layer: layer.count("0"))

    ones = best_layer.count("1")
    twos = best_layer.count("2")

    return str(ones * twos)


def solve_part2(data: str) -> str:
    layers = parse_layers(data)
    if not layers:
        return ""

    final = ["2"] * LAYER_SIZE  # пока всё прозрачное

    # Накладываем слои сверху вниз
    for layer in layers:
        for i, px in enumerate(layer):
            if final[i] == "2":  # если прозрачный — заменяем
                final[i] = px

    # Преобразуем в картинку
    rows = []
    for y in range(HEIGHT):
        row = final[y * WIDTH:(y + 1) * WIDTH]
        # 1 — белый пиксель, 0 — чёрный
        row_str = "".join("█" if c == "1" else " " for c in row)
        rows.append(row_str)

    return "\n".join(rows)


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:")
    print(solve_part2(raw))
