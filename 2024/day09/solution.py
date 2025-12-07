def build_disk_for_part1(line: str) -> list[int]:
    """
    Преобразует строку карты диска в список блоков:
    -1 = свободное место, >=0 = ID файла.
    Используется в части 1.
    """
    line = line.strip()
    disk: list[int] = []
    is_file = True
    file_id = 0

    for ch in line:
        length = int(ch)
        if is_file:
            # Блок файла с данным ID
            for _ in range(length):
                disk.append(file_id)
            file_id += 1
        else:
            # Свободные блоки
            for _ in range(length):
                disk.append(-1)
        is_file = not is_file

    return disk


def build_disk_and_files_for_part2(line: str) -> tuple[list[int], list[int], list[int]]:
    """
    Для части 2:
    - строим такой же массив блоков,
    - плюс для каждого файла запоминаем начало и длину.
      starts[file_id], lengths[file_id]
    """
    line = line.strip()
    disk: list[int] = []
    starts: list[int] = []
    lengths: list[int] = []

    is_file = True
    file_id = 0
    pos = 0  # текущая позиция в диске

    for ch in line:
        length = int(ch)
        if is_file:
            # файл с ID = file_id, длина length
            starts.append(pos)
            lengths.append(length)
            for _ in range(length):
                disk.append(file_id)
                pos += 1
            file_id += 1
        else:
            # свободное место
            for _ in range(length):
                disk.append(-1)
                pos += 1
        is_file = not is_file

    return disk, starts, lengths


def checksum(disk: list[int]) -> int:
    """
    Считает файловую чек-сумму:
    сумма (позиция * ID файла), свободные блоки (-1) пропускаем.
    """
    total = 0
    for i, v in enumerate(disk):
        if v != -1:
            total += i * v
    return total


def solve_part1(data: str) -> str:
    # Ожидается один длинный ряд цифр
    line = data.strip()
    if not line:
        return "0"

    disk = build_disk_for_part1(line)

    left = 0
    right = len(disk) - 1

    # Два указателя:
    # left — ищет первый свободный блок слева,
    # right — ищет первый файловый блок справа.
    while left < right:
        while left < right and disk[left] != -1:
            left += 1
        while left < right and disk[right] == -1:
            right -= 1
        if left < right:
            disk[left] = disk[right]
            disk[right] = -1
            left += 1
            right -= 1

    return str(checksum(disk))


def solve_part2(data: str) -> str:
    line = data.strip()
    if not line:
        return "0"

    # Диск + таблица файлов (начало и длина каждого ID)
    disk, starts, lengths = build_disk_and_files_for_part2(line)
    total_len = len(disk)
    num_files = len(starts)

    # Обрабатываем файлы с максимального ID к нулю
    for file_id in range(num_files - 1, -1, -1):
        length = lengths[file_id]
        if length == 0:
            # Файл нулевой длины — блоков нет, двигать нечего
            continue

        current_start = starts[file_id]

        # Ищем самую левую подходящую "дыру":
        # свободный непрерывный участок длиной >= length
        # с началом строго левее current_start.
        best_start = None
        i = 0

        while i < current_start:
            if disk[i] != -1:
                i += 1
                continue

            run_start = i
            # Собираем длину текущего свободного отрезка
            while i < total_len and disk[i] == -1:
                i += 1
            run_len = i - run_start

            if run_start < current_start and run_len >= length:
                best_start = run_start
                break

        if best_start is None:
            # Нет подходящего места — файл остаётся где был
            continue

        # Перемещаем целый файл:
        # 1) очищаем старое место
        for pos in range(current_start, current_start + length):
            disk[pos] = -1

        # 2) записываем файл в новое место (best_start .. best_start+length-1)
        for pos in range(best_start, best_start + length):
            disk[pos] = file_id

        # Обновляем начало файла
        starts[file_id] = best_start

    return str(checksum(disk))


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
