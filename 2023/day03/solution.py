def solve_part1(data: str) -> str:
    grid = data.splitlines()
    H = len(grid)
    W = len(grid[0]) if H else 0

    def is_symbol(ch: str) -> bool:
        return not (ch.isdigit() or ch == ".")

    total = 0

    r = 0
    while r < H:
        c = 0
        while c < W:
            if grid[r][c].isdigit():
                # читаем целое число
                start = c
                while c < W and grid[r][c].isdigit():
                    c += 1
                num_str = grid[r][start:c]
                num_val = int(num_str)

                # проверяем окрестность числа
                touches_symbol = False
                for rr in range(r - 1, r + 2):
                    for cc in range(start - 1, c + 1):
                        if 0 <= rr < H and 0 <= cc < W:
                            ch = grid[rr][cc]
                            if is_symbol(ch):
                                touches_symbol = True
                                break
                    if touches_symbol:
                        break

                if touches_symbol:
                    total += num_val
            else:
                c += 1
        r += 1

    return str(total)


def solve_part2(data: str) -> str:
    grid = data.splitlines()
    H = len(grid)
    W = len(grid[0]) if H else 0

    # сохраняем: для каждой звезды — список присоединённых чисел
    gear_map = {}

    r = 0
    while r < H:
        c = 0
        while c < W:
            if grid[r][c].isdigit():
                # читаем число
                start = c
                while c < W and grid[r][c].isdigit():
                    c += 1
                num_str = grid[r][start:c]
                num_val = int(num_str)

                # ищем соседние звёзды
                adjacent_gears = set()
                for rr in range(r - 1, r + 2):
                    for cc in range(start - 1, c + 1):
                        if 0 <= rr < H and 0 <= cc < W:
                            if grid[rr][cc] == "*":
                                adjacent_gears.add((rr, cc))

                # добавляем число в каждую найденную шестерёнку
                for pos in adjacent_gears:
                    gear_map.setdefault(pos, []).append(num_val)
            else:
                c += 1
        r += 1

    # теперь считаем только те *, у которых ровно 2 числа
    total = 0
    for pos, nums in gear_map.items():
        if len(nums) == 2:
            total += nums[0] * nums[1]

    return str(total)
