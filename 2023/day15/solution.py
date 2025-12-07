from pathlib import Path


def hash_str(s: str) -> int:
    """
    Хэш-функция из условия:
    value = 0
    для каждого символа:
        value = ((value + ord(ch)) * 17) % 256
    """
    value = 0
    for ch in s:
        value += ord(ch)
        value *= 17
        value %= 256
    return value


def parse_steps(data: str) -> list[str]:
    # Ввод — одна строка с шагами, разделёнными запятыми.
    # На всякий случай убираем переводы строк.
    line = data.strip().replace("\n", "")
    if not line:
        return []
    return line.split(",")


def solve_part1(data: str) -> str:
    steps = parse_steps(data)
    total = 0
    for s in steps:
        total += hash_str(s)
    return str(total)


def solve_part2(data: str) -> str:
    steps = parse_steps(data)

    # 256 коробок, в каждой — список линз (label, focal_length)
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]

    for step in steps:
        if not step:
            continue

        if "-" in step and "=" not in step:
            # Операция удаления: label-
            label = step[:-1]
            box_idx = hash_str(label)
            box = boxes[box_idx]
            # удаляем линзу с таким label, если есть
            boxes[box_idx] = [(lab, f) for (lab, f) in box if lab != label]

        else:
            # Операция добавления/замены: label=number
            label, num_str = step.split("=")
            focal = int(num_str)
            box_idx = hash_str(label)
            box = boxes[box_idx]

            # ищем линзу с таким label
            for i, (lab, f) in enumerate(box):
                if lab == label:
                    box[i] = (label, focal)  # заменяем фокусное
                    break
            else:
                # не нашли — добавляем в конец
                box.append((label, focal))

    # Считаем focusing power
    total_power = 0
    for box_idx, box in enumerate(boxes):
        if not box:
            continue
        for slot_idx, (_, focal) in enumerate(box, start=1):
            # (box index + 1) * slot index * focal length
            total_power += (box_idx + 1) * slot_idx * focal

    return str(total_power)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
