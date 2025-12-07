def parse_game_line(line: str):
    """
    Разбирает строку формата:
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'
    Возвращает: game_id: int и список показов,
    где каждый показ — dict {'red': int, 'green': int, 'blue': int}
    """
    if not line.strip():
        return None, []

    left, right = line.split(":", 1)
    # "Game 1" -> 1
    game_id_part = left.strip()
    # предполагаем формат "Game N"
    try:
        game_id = int(game_id_part.split()[1])
    except (IndexError, ValueError):
        # на всякий случай, чтобы не падать
        game_id = -1

    shows_raw = right.strip().split(";")
    shows = []

    for show in shows_raw:
        show_counts = {"red": 0, "green": 0, "blue": 0}
        parts = show.strip().split(",")
        for part in parts:
            part = part.strip()
            if not part:
                continue
            num_str, color = part.split()
            count = int(num_str)
            color = color.lower()
            if color in show_counts:
                show_counts[color] += count
        shows.append(show_counts)

    return game_id, shows


def solve_part1(data: str) -> str:
    # ограничения мешка
    limits = {"red": 12, "green": 13, "blue": 14}

    total = 0
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        game_id, shows = parse_game_line(line)
        if game_id is None:
            continue

        possible = True
        for show in shows:
            for color, limit in limits.items():
                if show[color] > limit:
                    possible = False
                    break
            if not possible:
                break

        if possible:
            total += game_id

    return str(total)


def solve_part2(data: str) -> str:
    total_power = 0

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        game_id, shows = parse_game_line(line)
        if game_id is None:
            continue

        max_red = 0
        max_green = 0
        max_blue = 0

        for show in shows:
            if show["red"] > max_red:
                max_red = show["red"]
            if show["green"] > max_green:
                max_green = show["green"]
            if show["blue"] > max_blue:
                max_blue = show["blue"]

        power = max_red * max_green * max_blue
        total_power += power

    return str(total_power)
