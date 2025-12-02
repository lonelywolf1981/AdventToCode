# init.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SOLUTION_TEMPLATE = """\
def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    # TODO: реализовать
    return "not implemented"


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    # TODO: реализовать
    return "not implemented"


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
"""

START_TEMPLATE = '''\
import os
import sys
import re
import html
from pathlib import Path
from typing import Optional

import requests  # pip install requests


BASE_DIR = Path(__file__).resolve().parent  # папка года, например 2025
ROOT_DIR = BASE_DIR.parent                  # корень проекта (там .env)


def detect_year() -> int:
    try:
        return int(BASE_DIR.name)
    except ValueError:
        print(f"Не удалось определить год из имени папки: {BASE_DIR.name}")
        sys.exit(1)


def get_session_token() -> Optional[str]:
    """
    Токен сессии Advent of Code:
    1) переменная окружения AOC_SESSION
    2) файл .env в корне проекта (ROOT_DIR) с строкой AOC_SESSION=...
    """
    token = os.environ.get("AOC_SESSION")
    if token:
        return token.strip()

    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        content = env_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            if key.strip() == "AOC_SESSION":
                return value.strip().strip('"').strip("'")
    return None


def fetch_page(url: str, session_token: str) -> str:
    cookies = {"session": session_token}
    headers = {
        "User-Agent": "AdventToCode-Helper (personal use)"
    }
    resp = requests.get(url, cookies=cookies, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.text


def html_to_text(fragment: str) -> str:
    """Грубый перевод HTML AoC в обычный текст."""
    fragment = re.sub(
        r"<(script|style).*?>.*?</\\1>", "", fragment, flags=re.S | re.I
    )
    fragment = re.sub(r"<\\s*br\\s*/?>", "\\n", fragment, flags=re.I)
    fragment = re.sub(r"</p>", "\\n\\n", fragment, flags=re.I)
    fragment = re.sub(r"<.*?>", "", fragment)
    text = html.unescape(fragment)
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\\n".join(lines)


def parse_articles(html_page: str):
    """
    Возвращает (part1_text, part2_text_or_None) на основе <article class="day-desc">.
    Сначала на AoC появляется только Part 1, после решения — добавляется Part 2.
    """
    articles = re.findall(
        r'<article\\s+class="day-desc">(.+?)</article>',
        html_page,
        flags=re.S | re.I,
    )
    if not articles:
        full_text = html_to_text(html_page)
        return full_text.strip(), None

    part1 = html_to_text(articles[0]).strip()
    part2 = html_to_text(articles[1]).strip() if len(articles) >= 2 else None
    return part1, part2


def write_quest_and_state(day_dir: Path, part1: str, part2: Optional[str]) -> None:
    quest_path = day_dir / "quest.txt"
    init_path = day_dir / "init.txt"

    if part2:
        content = (
            "=== Part 1 ===\\n\\n"
            + part1
            + "\\n\\n=== Part 2 ===\\n\\n"
            + part2
            + "\\n"
        )
        init_value = "PARTS=2\\n"
    else:
        content = "=== Part 1 ===\\n\\n" + part1 + "\\n"
        init_value = "PARTS=1\\n"

    quest_path.write_text(content, encoding="utf-8")
    init_path.write_text(init_value, encoding="utf-8")


def read_parts_from_quest(day_dir: Path):
    quest_path = day_dir / "quest.txt"
    if not quest_path.exists():
        return None, None

    text = quest_path.read_text(encoding="utf-8")
    part1 = part2 = None

    if "=== Part 2 ===" in text:
        before, _, after = text.partition("=== Part 2 ===")
        _, _, p1_body = before.partition("=== Part 1 ===")
        part1 = p1_body.strip()
        part2 = after.strip()
    else:
        _, sep, p1_body = text.partition("=== Part 1 ===")
        part1 = (p1_body if sep else text).strip()

    return part1, part2


def download_input_if_needed(year: int, day: int, session_token: str, day_dir: Path):
    """
    Скачиваем input.txt только если его ещё нет
    или он пустой/заглушка (строка начинается с '#').
    """
    input_path = day_dir / "input.txt"

    if input_path.exists():
        existing = input_path.read_text(encoding="utf-8").strip()
        if existing and not existing.startswith("#"):
            print(f"input.txt уже существует, не перекачиваем: {input_path}")
            return

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    try:
        text = fetch_page(url, session_token)
    except Exception as e:
        print(f"[WARN] Не удалось скачать input: {e}")
        if not input_path.exists():
            input_path.write_text(
                "# Не удалось автоматически скачать input.\\n"
                "# Скопируйте его с сайта AoC вручную.\\n",
                encoding="utf-8",
            )
        return

    input_path.write_text(text.lstrip("\\n"), encoding="utf-8")
    print(f"input.txt скачан/обновлён: {input_path}")


def load_solution_module(day_dir: Path):
    solution_path = day_dir / "solution.py"
    if not solution_path.exists():
        raise FileNotFoundError(f"Не найден {solution_path}")

    import importlib.util

    spec = importlib.util.spec_from_file_location("solution", solution_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def main():
    print("=== AdventToCode: запуск года ===")
    year = detect_year()
    print(f"Год: {year}")

    day_str = input("Введите номер дня (1-25): ").strip()
    if not day_str.isdigit():
        print("Ожидался числовой номер дня.")
        sys.exit(1)
    day = int(day_str)
    if not (1 <= day <= 25):
        print("Номер дня должен быть от 1 до 25.")
        sys.exit(1)

    day_dir = BASE_DIR / f"day{day:02d}"
    if not day_dir.exists():
        print(f"Папка дня не найдена: {day_dir}")
        sys.exit(1)

    session_token = get_session_token()
    if not session_token:
        print("Не найден токен сессии Advent of Code.")
        print("Создайте в корне .env с строкой AOC_SESSION=<ваш_cookie_значение>")
        print("или задайте переменную окружения AOC_SESSION.")
        sys.exit(1)

    # 1) Качаем страницу, вытаскиваем Part 1 и (если есть) Part 2
    base_url = f"https://adventofcode.com/{year}/day/{day}"
    try:
        html_page = fetch_page(base_url, session_token)
    except Exception as e:
        print(f"Не удалось скачать страницу задачи: {e}")
        sys.exit(1)

    part1_text, part2_text = parse_articles(html_page)

    # 2) Записываем quest.txt и init.txt
    write_quest_and_state(day_dir, part1_text, part2_text)
    print("Условия задачи обновлены в quest.txt и init.txt.")

    # 3) При первом запуске (и если input ещё не нормальный) — качаем input.txt
    download_input_if_needed(year, day, session_token, day_dir)

    # 4) Читаем части из quest.txt и показываем
    p1, p2 = read_parts_from_quest(day_dir)

    print("\\n" + "=" * 40)
    print(f"Day {day:02d} — Part 1")
    print("-" * 40)
    if p1:
        print(p1)
    else:
        print("Текст Part 1 не найден.")

    if p2:
        print("\\n" + "=" * 40)
        print(f"Day {day:02d} — Part 2")
        print("-" * 40)
        print(p2)
    else:
        print("\\n[INFO] Part 2 пока недоступна (на странице только первая часть).")
        print("[INFO] Когда AoC откроет Part 2, запусти start.py снова для этого дня.")

    # 5) Пытаемся выполнить решение
    try:
        module = load_solution_module(day_dir)
    except Exception as e:
        print(f"Не удалось загрузить solution.py: {e}")
        return

    input_path = day_dir / "input.txt"
    if input_path.exists():
        data = input_path.read_text(encoding="utf-8")
    else:
        data = ""
        print("[WARN] input.txt не найден, в функции будет передана пустая строка.")

    print("\\n" + "=" * 40)
    print("Результаты решения:")
    print("-" * 40)

    # Part 1
    if hasattr(module, "solve_part1"):
        try:
            res1 = module.solve_part1(data)
        except Exception as e:
            res1 = f"Ошибка выполнения: {e}"
        print("Part 1:", res1)
    else:
        print("Part 1: функция solve_part1 не найдена.")

    # Part 2
    if hasattr(module, "solve_part2"):
        try:
            res2 = module.solve_part2(data)
        except Exception as e:
            res2 = f"Ошибка выполнения: {e}"
        print("Part 2:", res2)
    else:
        print("Part 2: функция solve_part2 не найдена.")


if __name__ == "__main__":
    main()
'''


def main():
    year_str = input("Введите год (например, 2025): ").strip()
    if not year_str.isdigit():
        print("Ожидался числовой год.")
        return
    year = int(year_str)

    # .env в корне (если нет)
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        env_path.write_text(
            "AOC_SESSION=your_session_cookie_here\\n"
            "# Замените your_session_cookie_here на значение cookie 'session' с сайта Advent of Code\\n",
            encoding="utf-8",
        )
        print(f"Создан шаблон {env_path}")

    # Папка года
    year_dir = BASE_DIR / str(year)
    year_dir.mkdir(exist_ok=True)

    # start.py в папке года (если нет)
    start_path = year_dir / "start.py"
    if not start_path.exists():
        start_path.write_text(START_TEMPLATE, encoding="utf-8")
        print(f"Создан файл {start_path}")

    # Папки дней
    for day in range(1, 25 + 1):
        day_dir = year_dir / f"day{day:02d}"
        day_dir.mkdir(exist_ok=True)

        sol_path = day_dir / "solution.py"
        if not sol_path.exists():
            sol_path.write_text(SOLUTION_TEMPLATE, encoding="utf-8")
            print(f"Создан {sol_path}")

        quest_path = day_dir / "quest.txt"
        if not quest_path.exists():
            quest_path.write_text(
                "Задача ещё не загружена. Запустите start.py для этого года и выберите день.\\n",
                encoding="utf-8",
            )

        init_path = day_dir / "init.txt"
        if not init_path.exists():
            init_path.write_text("PARTS=0\\n", encoding="utf-8")

    print(f"Структура для {year} готова: {year_dir}")


if __name__ == "__main__":
    main()
