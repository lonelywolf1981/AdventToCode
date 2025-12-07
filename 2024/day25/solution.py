def parse_blocks(data: str):
    """
    Разделяем вход на блоки чертежей.
    Каждый блок — 7 строк: либо lock, либо key.
    Разделены пустыми строками.
    """
    blocks = []
    current = []
    for line in data.splitlines():
        line = line.rstrip("\n")
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


def classify(block):
    """
    Определяем, это key или lock.
    key — верхняя строка "#####"
    lock — нижняя строка "#####"
    """
    if block[0] == "#####":
        return "key"
    else:
        return "lock"


def extract_heights(block):
    """
    Превращаем чертёж key/lock в массив высот для 5 столбцов.

    Фигура: 7 строк, ширина = 5.
      - Для key сверху полка "#####", дальше вниз "наращивание".
      - Для lock снизу полка "#####", дальше вверх "наращивание".

    Чтобы унифицировать, считаем количество заполняющих клеток
    НЕ включая полку "#####".
    """
    # блок всегда имеет 7 строк
    # ищем строки с "#...." и считаем по колонкам

    # Для key: полка сверху, работать начинаем со строки 1.
    # Для lock: полка снизу, работать заканчиваем строкой -2.

    h = [0] * 5
    # Пропускаем верхнюю или нижнюю полку, просто считаем '#'
    # по всем строкам, кроме полки, и суммируем по столбцам.
    # Но важно условие задачи: суммарная высота (key + lock) <= 5.

    # Для key: верхняя строка index=0 — полка, пропускаем
    # Для lock: нижняя строка index=-1 — полка, пропускаем

    if block[0] == "#####":  # key
        rows = block[1:]     # исключаем верхнюю полку
    else:                    # lock
        rows = block[:-1]    # исключаем нижнюю полку

    # Считаем количество '#' в каждом столбце
    for r in rows:
        for c, ch in enumerate(r):
            if ch == "#":
                h[c] += 1

    return h


def solve_part1(data: str) -> str:
    blocks = parse_blocks(data)

    keys = []
    locks = []

    for block in blocks:
        t = classify(block)
        h = extract_heights(block)
        if t == "key":
            keys.append(h)
        else:
            locks.append(h)

    # Подсчёт подходящих пар
    ans = 0
    for k in keys:
        for l in locks:
            ok = True
            for i in range(5):
                if k[i] + l[i] > 5:
                    ok = False
                    break
            if ok:
                ans += 1

    return str(ans)


def solve_part2(data: str) -> str:
    # В Day 25 нет второй части — возвращаем заглушку
    return "0"


if __name__ == "__main__":
    from pathlib import Path

    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    raw = input_path.read_text(encoding="utf-8") if input_path.exists() else ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
