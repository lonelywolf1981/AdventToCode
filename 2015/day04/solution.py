import hashlib


def solve_part1(data: str) -> str:
    secret = data.strip()
    n = 1
    prefix = "00000"
    while True:
        s = f"{secret}{n}".encode("utf-8")
        h = hashlib.md5(s).hexdigest()
        if h.startswith(prefix):
            return str(n)
        n += 1


def solve_part2(data: str) -> str:
    secret = data.strip()
    n = 1
    prefix = "000000"
    while True:
        s = f"{secret}{n}".encode("utf-8")
        h = hashlib.md5(s).hexdigest()
        if h.startswith(prefix):
            return str(n)
        n += 1


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
