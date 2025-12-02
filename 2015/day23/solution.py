from typing import List, Tuple


Instruction = Tuple[str, Tuple]


def parse_program(data: str) -> List[Instruction]:
    program: List[Instruction] = []
    for line in data.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.replace(",", "").split()
        op = parts[0]

        if op in ("hlf", "tpl", "inc"):
            # hlf a | tpl a | inc a
            r = parts[1]
            program.append((op, (r,)))
        elif op == "jmp":
            # jmp +2 / jmp -1
            offset = int(parts[1])
            program.append((op, (offset,)))
        elif op in ("jie", "jio"):
            # jie a, +2 | jio b, -1
            r = parts[1]
            offset = int(parts[2])
            program.append((op, (r, offset)))
        else:
            raise ValueError(f"Unknown instruction: {line}")

    return program


def run_program(program: List[Instruction], a_start: int, b_start: int) -> int:
    regs = {"a": a_start, "b": b_start}
    pc = 0  # program counter

    while 0 <= pc < len(program):
        op, args = program[pc]

        if op == "hlf":
            (r,) = args
            regs[r] //= 2
            pc += 1
        elif op == "tpl":
            (r,) = args
            regs[r] *= 3
            pc += 1
        elif op == "inc":
            (r,) = args
            regs[r] += 1
            pc += 1
        elif op == "jmp":
            (offset,) = args
            pc += offset
        elif op == "jie":
            r, offset = args
            if regs[r] % 2 == 0:
                pc += offset
            else:
                pc += 1
        elif op == "jio":
            r, offset = args
            if regs[r] == 1:
                pc += offset
            else:
                pc += 1
        else:
            raise ValueError(f"Unknown op at runtime: {op}")

    return regs["b"]


def solve_part1(data: str) -> str:
    program = parse_program(data)
    result_b = run_program(program, a_start=0, b_start=0)
    return str(result_b)


def solve_part2(data: str) -> str:
    program = parse_program(data)
    result_b = run_program(program, a_start=1, b_start=0)
    return str(result_b)


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
