from pathlib import Path
import re


def parse_input(data: str):
    wf_part, parts_part = data.strip().split("\n\n")

    workflows = {}
    for line in wf_part.splitlines():
        name, rest = line.split("{")
        rest = rest[:-1]  # remove trailing '}'
        rules = rest.split(",")
        parsed = []
        for r in rules:
            if ":" in r:
                cond, target = r.split(":")
                parsed.append((cond, target))
            else:
                parsed.append(("TRUE", r))
        workflows[name] = parsed

    parts = []
    for line in parts_part.splitlines():
        xs = list(map(int, re.findall(r"\d+", line)))
        parts.append({"x": xs[0], "m": xs[1], "a": xs[2], "s": xs[3]})

    return workflows, parts


def run_workflow(workflows, part):
    """
    Part 1 simulation.
    """
    cur = "in"
    while True:
        rules = workflows[cur]
        for cond, target in rules:
            if cond == "TRUE":
                cur = target
                break
            # condition like x>1000 or a<123
            var = cond[0]
            op = cond[1]
            val = int(cond[2:])
            if op == ">":
                ok = part[var] > val
            else:
                ok = part[var] < val
            if ok:
                cur = target
                break

        if cur in ("A", "R"):
            return cur


def solve_part1(data: str) -> str:
    workflows, parts = parse_input(data)
    total = 0
    for p in parts:
        res = run_workflow(workflows, p)
        if res == "A":
            total += p["x"] + p["m"] + p["a"] + p["s"]
    return str(total)


# ---------------------------------------------------------------
# Part 2 — диапазонный просчёт
# ---------------------------------------------------------------

def count_accepted(workflows):
    """
    Возвращает количество подходящих комбинаций (x,m,a,s) ∈ [1..4000], попадающих в A.
    """

    def dfs(wf_name, ranges):
        """
        ranges: {"x":(lo,hi), "m":..., "a":..., "s":...} — включительно
        """
        if wf_name == "R":
            return 0
        if wf_name == "A":
            # Количество точек в многомерном прямоугольнике
            res = 1
            for v in ("x", "m", "a", "s"):
                lo, hi = ranges[v]
                if lo > hi:
                    return 0
                res *= (hi - lo + 1)
            return res

        total = 0

        for cond, target in workflows[wf_name]:
            if cond == "TRUE":
                # Nothing to split, pass whole range
                total += dfs(target, ranges)
                return total

            # condition: x<1000 or a>12 etc
            var = cond[0]
            op = cond[1]
            val = int(cond[2:])

            lo, hi = ranges[var]

            if op == "<":
                true_range = (lo, min(hi, val - 1))
                false_range = (max(lo, val), hi)
            else:  # >
                true_range = (max(lo, val + 1), hi)
                false_range = (lo, min(hi, val))

            # Ветка "истинная"
            if true_range[0] <= true_range[1]:
                new_ranges = dict(ranges)
                new_ranges[var] = true_range
                total += dfs(target, new_ranges)

            # Остаток идёт на следующие правила
            if false_range[0] <= false_range[1]:
                ranges = dict(ranges)
                ranges[var] = false_range
                continue
            else:
                # часть диапазона исключена, дальше идти нечем
                return total

        return total

    start_ranges = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }

    return dfs("in", start_ranges)


def solve_part2(data: str) -> str:
    workflows, _ = parse_input(data)
    return str(count_accepted(workflows))


# ---------------------------------------------------------------
# Entry
# ---------------------------------------------------------------
if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"
    if input_path.exists():
        raw = input_path.read_text(encoding="utf-8").strip()
    else:
        raw = ""
    print("Part 1:", solve_part1(raw))
    print("Part 2:", solve_part2(raw))
