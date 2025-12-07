from pathlib import Path


def parse(data: str):
    return [list(line) for line in data.splitlines() if line.strip()]


def tilt_north(grid):
    R = len(grid)
    C = len(grid[0])
    for col in range(C):
        write_row = 0
        for row in range(R):
            if grid[row][col] == "#":
                write_row = row + 1
            elif grid[row][col] == "O":
                if write_row != row:
                    grid[write_row][col] = "O"
                    grid[row][col] = "."
                write_row += 1


def tilt_south(grid):
    R = len(grid)
    C = len(grid[0])
    for col in range(C):
        write_row = R - 1
        for row in range(R - 1, -1, -1):
            if grid[row][col] == "#":
                write_row = row - 1
            elif grid[row][col] == "O":
                if write_row != row:
                    grid[write_row][col] = "O"
                    grid[row][col] = "."
                write_row -= 1


def tilt_west(grid):
    R = len(grid)
    C = len(grid[0])
    for row in range(R):
        write_col = 0
        for col in range(C):
            if grid[row][col] == "#":
                write_col = col + 1
            elif grid[row][col] == "O":
                if write_col != col:
                    grid[row][write_col] = "O"
                    grid[row][col] = "."
                write_col += 1


def tilt_east(grid):
    R = len(grid)
    C = len(grid[0])
    for row in range(R):
        write_col = C - 1
        for col in range(C - 1, -1, -1):
            if grid[row][col] == "#":
                write_col = col - 1
            elif grid[row][col] == "O":
                if write_col != col:
                    grid[row][write_col] = "O"
                    grid[row][col] = "."
                write_col -= 1


def calc_load(grid):
    R = len(grid)
    total = 0
    for r in range(R):
        for c in range(len(grid[0])):
            if grid[r][c] == "O":
                total += (R - r)
    return total


def grid_to_tuple(grid):
    return tuple("".join(row) for row in grid)


def cycle(grid):
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


def solve_part1(data: str) -> str:
    grid = parse(data)
    tilt_north(grid)
    return str(calc_load(grid))


def solve_part2(data: str) -> str:
    grid = parse(data)

    seen = {}  # state → cycle_index
    states = []  # список состояний по порядку

    i = 0
    target = 1_000_000_000

    while True:
        k = grid_to_tuple(grid)
        if k in seen:
            # нашли цикл
            cycle_start = seen[k]
            cycle_length = i - cycle_start
            break

        seen[k] = i
        states.append(k)

        # выполняем один цикл
        cycle(grid)
        i += 1

    # сколько осталось пройти после перехода в цикл
    remaining = (target - cycle_start) % cycle_length
    final_state = states[cycle_start + remaining]

    # Превращаем обратно в grid и считаем нагрузку
    grid = [list(row) for row in final_state]
    return str(calc_load(grid))


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""

    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
