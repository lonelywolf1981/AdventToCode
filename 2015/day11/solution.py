def increment_password(s: str) -> str:
    """
    Увеличиваем пароль как число в 26-ричной системе (a..z).
    """
    arr = list(s)
    i = len(arr) - 1
    while i >= 0:
        if arr[i] == 'z':
            arr[i] = 'a'
            i -= 1
        else:
            arr[i] = chr(ord(arr[i]) + 1)
            break
    return "".join(arr)


def valid(s: str) -> bool:
    # Условие 2: запрещённые буквы
    if any(ch in s for ch in "iol"):
        return False

    # Условие 1: возрастающая последовательность из трёх
    has_straight = any(
        ord(s[i]) + 1 == ord(s[i+1]) and
        ord(s[i]) + 2 == ord(s[i+2])
        for i in range(len(s) - 2)
    )
    if not has_straight:
        return False

    # Условие 3: две разные непересекающиеся пары
    pairs = set()
    i = 0
    while i < len(s) - 1:
        if s[i] == s[i+1]:
            pairs.add(s[i])
            i += 2  # пропускаем, чтобы пары не перекрывались
        else:
            i += 1

    return len(pairs) >= 2


def next_valid_password(s: str) -> str:
    while True:
        s = increment_password(s)
        if valid(s):
            return s


def solve_part1(data: str) -> str:
    start = data.strip()
    return next_valid_password(start)


def solve_part2(data: str) -> str:
    first = next_valid_password(data.strip())
    second = next_valid_password(first)
    return second


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
