import re
import heapq
from pathlib import Path
from typing import Dict, Set, List, Tuple


def parse_input(data: str) -> Tuple[Set[str], Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Разбирает строки вида:
    Step C must be finished before step A can begin.

    Возвращает:
    - множество всех шагов
    - словарь prerequisites[step] = set(предшествующих шагов)
    - словарь graph[step] = set(шагов, зависящих от данного)
    """
    all_steps: Set[str] = set()
    prerequisites: Dict[str, Set[str]] = {}
    graph: Dict[str, Set[str]] = {}

    pattern = re.compile(
        r"Step\s+([A-Z])\s+must\s+be\s+finished\s+before\s+step\s+([A-Z])\s+can\s+begin\."
    )

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if not m:
            continue

        before = m.group(1)
        after = m.group(2)

        all_steps.add(before)
        all_steps.add(after)

        # after зависит от before
        prerequisites.setdefault(after, set()).add(before)
        prerequisites.setdefault(before, prerequisites.get(before, set()))

        graph.setdefault(before, set()).add(after)
        graph.setdefault(after, graph.get(after, set()))

    # на случай, если какие-то шаги не попали в словари
    for step in all_steps:
        prerequisites.setdefault(step, set())
        graph.setdefault(step, set())

    return all_steps, prerequisites, graph


def solve_part1(data: str) -> str:
    # Решение части 1. data — содержимое input.txt.
    all_steps, prerequisites, graph = parse_input(data)

    # шаги с нулевыми зависимостями
    available: List[str] = [
        s for s in all_steps if not prerequisites.get(s)
    ]
    heapq.heapify(available)  # min-heap по буквам

    result_order: List[str] = []
    # Копируем зависимости, чтобы не портить исходные структуры (на всякий случай)
    prereq = {s: set(reqs) for s, reqs in prerequisites.items()}

    while available:
        step = heapq.heappop(available)
        result_order.append(step)

        # "выполнить" шаг: убрать его из зависимостей других
        for nxt in graph.get(step, ()):
            deps = prereq[nxt]
            if step in deps:
                deps.remove(step)
                if not deps:
                    heapq.heappush(available, nxt)

    return "".join(result_order)


def step_duration(step: str, base_time: int = 60) -> int:
    """
    Время выполнения шага:
    base_time + позиция буквы (A=1, B=2, ...).
    """
    return base_time + (ord(step) - ord("A") + 1)


def solve_part2(data: str) -> str:
    # Решение части 2. data — содержимое input.txt.
    all_steps, prerequisites, graph = parse_input(data)

    NUM_WORKERS = 5
    BASE_TIME = 60

    # Копия зависимостей
    prereq = {s: set(reqs) for s, reqs in prerequisites.items()}

    # начально доступные шаги (без зависимостей)
    available: List[str] = [
        s for s in all_steps if not prereq.get(s)
    ]
    heapq.heapify(available)

    # состояние рабочих: список кортежей (current_step, remaining_time) или (None, 0) если свободен
    workers: List[Tuple[str | None, int]] = [(None, 0) for _ in range(NUM_WORKERS)]

    time = 0
    completed: Set[str] = set()

    # пока не завершены все шаги
    while len(completed) < len(all_steps):
        # 1) назначаем задачи свободным рабочим
        for i in range(NUM_WORKERS):
            step, remaining = workers[i]
            if step is None and available:
                # даём новую задачу
                new_step = heapq.heappop(available)
                workers[i] = (new_step, step_duration(new_step, BASE_TIME))

        # если никто не работает (очень маловероятно, но на всякий случай)
        if all(step is None for step, _ in workers):
            break

        # 2) найдём ближайшее завершение задачи
        # минимальное оставшееся время среди занятых рабочих
        active_times = [rem for step, rem in workers if step is not None]
        if not active_times:
            break
        dt = min(active_times)

        # сдвигаем время
        time += dt

        # уменьшаем оставшееся время по всем рабочим
        finished_steps: List[str] = []
        new_workers: List[Tuple[str | None, int]] = []

        for step, remaining in workers:
            if step is None:
                new_workers.append((None, 0))
            else:
                remaining -= dt
                if remaining == 0:
                    # шаг завершён
                    completed.add(step)
                    finished_steps.append(step)
                    new_workers.append((None, 0))
                else:
                    new_workers.append((step, remaining))

        workers = new_workers

        # 3) обновляем зависимости после завершения шагов
        for done_step in finished_steps:
            for nxt in graph.get(done_step, ()):
                deps = prereq[nxt]
                if done_step in deps:
                    deps.remove(done_step)
                    if not deps:
                        # шаг стал доступен (если ещё не выполнен и не в available)
                        if nxt not in completed:
                            heapq.heappush(available, nxt)

    return str(time)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8")
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
