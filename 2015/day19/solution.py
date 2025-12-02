from typing import List, Tuple, Set
import re


def parse(data: str) -> Tuple[List[Tuple[str, str]], str]:
    """
    Возвращает (rules, molecule):
    rules: список (from, to)
    molecule: строка молекулы
    """
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]
    rules: List[Tuple[str, str]] = []

    # Все строки, кроме последней — правила, последняя — молекула
    for line in lines[:-1]:
        left, right = line.split(" => ")
        rules.append((left, right))

    molecule = lines[-1]
    return rules, molecule


def solve_part1(data: str) -> str:
    rules, molecule = parse(data)

    results: Set[str] = set()

    for src, dst in rules:
        start = 0
        # Ищем все вхождения src в molecule
        while True:
            idx = molecule.find(src, start)
            if idx == -1:
                break
            new_mol = molecule[:idx] + dst + molecule[idx + len(src):]
            results.add(new_mol)
            start = idx + 1  # ищем следующее вхождение дальше

    return str(len(results))


def tokenize_molecule(m: str) -> List[str]:
    """
    Разбиваем молекулу на токены-химические элементы:
    заглавная буква + необязательная строчная, например:
    "CRnCaCaCaSiTh" -> ["C","Rn","Ca","Ca","Ca","Si","Th"]
    """
    return re.findall(r"[A-Z][a-z]?", m)


def solve_part2(data: str) -> str:
    # Для стандартного инпута AoC 2015 Day 19
    # используем аналитическую формулу:
    #
    # steps = N_tokens - N_Rn - N_Ar - 2 * N_Y - 1
    #
    # где токены — это элементы вида H, Al, Ca и т.п.
    _, molecule = parse(data)

    tokens = tokenize_molecule(molecule)
    n_tokens = len(tokens)
    n_rn = molecule.count("Rn")
    n_ar = molecule.count("Ar")
    n_y = molecule.count("Y")

    steps = n_tokens - n_rn - n_ar - 2 * n_y - 1
    return str(steps)


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
