def solve_part1(data: str) -> str:
    target = int(data.strip())

    # Эмпирически верхняя граница ~ target // 10,
    # но можно взять немного больше.
    limit = target // 10

    # массив подарков для домов
    houses = [0] * (limit + 1)

    # Для каждого эльфа добавляем подарки всем кратным
    for elf in range(1, limit + 1):
        gift = elf * 10
        for house in range(elf, limit + 1, elf):
            houses[house] += gift

    # Ищем первый дом >= target
    for i in range(1, limit + 1):
        if houses[i] >= target:
            return str(i)

    return "not found"


def solve_part2(data: str) -> str:
    target = int(data.strip())

    # Аналогично, но правило отличается (только первые 50 домов)
    limit = target // 10

    houses = [0] * (limit + 1)

    for elf in range(1, limit + 1):
        gift = elf * 11
        count = 0
        house = elf
        while house <= limit and count < 50:
            houses[house] += gift
            house += elf
            count += 1

    for i in range(1, limit + 1):
        if houses[i] >= target:
            return str(i)

    return "not found"


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
