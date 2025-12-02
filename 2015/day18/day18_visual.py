import tkinter as tk
from pathlib import Path
from typing import List


CELL_SIZE = 6  # размер клетки в пикселях (для 100x100 получится 600x600)


def parse_grid(text: str) -> List[List[bool]]:
    grid = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        row = [c == "#" for c in line]
        grid.append(row)
    return grid


def count_on_neighbors(grid: List[List[bool]], x: int, y: int) -> int:
    h = len(grid)
    w = len(grid[0])
    cnt = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if 0 <= nx < h and 0 <= ny < w:
                if grid[nx][ny]:
                    cnt += 1
    return cnt


def step_grid(grid: List[List[bool]], stuck_corners: bool = False) -> List[List[bool]]:
    h = len(grid)
    w = len(grid[0])
    new_grid = [[False] * w for _ in range(h)]

    for i in range(h):
        for j in range(w):
            neighbors = count_on_neighbors(grid, i, j)
            if grid[i][j]:
                new_grid[i][j] = neighbors in (2, 3)
            else:
                new_grid[i][j] = neighbors == 3

    if stuck_corners:
        new_grid[0][0] = True
        new_grid[0][w - 1] = True
        new_grid[h - 1][0] = True
        new_grid[h - 1][w - 1] = True

    return new_grid


class LightsApp(tk.Tk):
    def __init__(self, grid: List[List[bool]]):
        super().__init__()
        self.title("AoC 2015 Day 18 — Lights Visualizer")

        self.original_grid = [row[:] for row in grid]
        self.grid_data = [row[:] for row in grid]

        self.h = len(self.grid_data)
        self.w = len(self.grid_data[0])

        # состояние
        self.step_count = 0
        self.stuck_corners_var = tk.BooleanVar(value=False)  # Part 2 режим

        # для автоплея
        self.is_playing = False
        self.after_id = None

        # UI
        self._build_widgets()
        self._apply_stuck_corners_if_needed(reset=True)
        self._draw_grid()
        self._update_status()

    def _build_widgets(self):
        # Canvas для отображения сетки
        canvas_width = self.w * CELL_SIZE
        canvas_height = self.h * CELL_SIZE
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg="black")
        self.canvas.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        # --- Панель управления ---

        # 1-я строка: шаг, N шагов, Play/Pause
        self.btn_step = tk.Button(self, text="Next step", command=self.on_step)
        self.btn_step.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        tk.Label(self, text="Steps:").grid(row=1, column=1, sticky="e")
        self.steps_entry = tk.Entry(self, width=6)
        self.steps_entry.insert(0, "10")
        self.steps_entry.grid(row=1, column=2, sticky="w")

        self.btn_run = tk.Button(self, text="Run N steps", command=self.on_run_n_steps)
        self.btn_run.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        self.btn_play = tk.Button(self, text="Play", command=self.on_toggle_play)
        self.btn_play.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

        # 2-я строка: режим, Reset, Quit, скорость
        self.chk_stuck = tk.Checkbutton(
            self,
            text="Stuck corners (Part 2)",
            variable=self.stuck_corners_var,
            command=self.on_toggle_stuck
        )
        self.chk_stuck.grid(row=2, column=0, columnspan=2, sticky="w", padx=5)

        self.btn_reset = tk.Button(self, text="Reset", command=self.on_reset)
        self.btn_reset.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        self.btn_quit = tk.Button(self, text="Quit", command=self.on_quit)
        self.btn_quit.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        tk.Label(self, text="Speed (ms):").grid(row=2, column=4, sticky="w")
        # Scale: от 10 до 1000 мс, по умолчанию 100
        self.speed_scale = tk.Scale(self, from_=10, to=1000, orient="horizontal", showvalue=True, length=150)
        self.speed_scale.set(100)
        self.speed_scale.grid(row=3, column=0, columnspan=5, sticky="ew", padx=5)

        # Статус
        self.status_label = tk.Label(self, text="", anchor="w")
        self.status_label.grid(row=4, column=0, columnspan=5, sticky="ew", padx=5, pady=5)

    def _apply_stuck_corners_if_needed(self, reset: bool = False):
        if not self.stuck_corners_var.get():
            return
        h = self.h
        w = self.w
        self.grid_data[0][0] = True
        self.grid_data[0][w - 1] = True
        self.grid_data[h - 1][0] = True
        self.grid_data[h - 1][w - 1] = True

    def _draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.h):
            for j in range(self.w):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                color = "lime" if self.grid_data[i][j] else "gray10"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def _count_on(self) -> int:
        return sum(cell for row in self.grid_data for cell in row)

    def _update_status(self):
        on_count = self._count_on()
        mode = "Part 2 (stuck corners)" if self.stuck_corners_var.get() else "Part 1"
        self.status_label.config(
            text=f"Step: {self.step_count} | Lights ON: {on_count} | Mode: {mode}"
        )

    def _get_delay_ms(self) -> int:
        try:
            v = int(self.speed_scale.get())
            if v < 1:
                v = 1
        except Exception:
            v = 100
        return v

    # --- Кнопки/действия ---

    def on_step(self):
        # один шаг
        self.grid_data = step_grid(self.grid_data, stuck_corners=self.stuck_corners_var.get())
        self.step_count += 1
        self._draw_grid()
        self._update_status()

    def on_run_n_steps(self):
        try:
            n = int(self.steps_entry.get())
        except ValueError:
            n = 0
        if n <= 0:
            return
        for _ in range(n):
            self.grid_data = step_grid(self.grid_data, stuck_corners=self.stuck_corners_var.get())
            self.step_count += 1
        self._draw_grid()
        self._update_status()

    def on_reset(self):
        self._stop_play()
        self.grid_data = [row[:] for row in self.original_grid]
        self.step_count = 0
        self._apply_stuck_corners_if_needed(reset=True)
        self._draw_grid()
        self._update_status()

    def on_toggle_stuck(self):
        # при переключении режима — просто применяем углы (если надо) и перерисовываем
        self._apply_stuck_corners_if_needed()
        self._draw_grid()
        self._update_status()

    def on_quit(self):
        self._stop_play()
        self.destroy()

    # --- Автоплей ---

    def on_toggle_play(self):
        if not self.is_playing:
            self._start_play()
        else:
            self._stop_play()

    def _start_play(self):
        self.is_playing = True
        self.btn_play.config(text="Pause")
        self._schedule_next_frame()

    def _stop_play(self):
        self.is_playing = False
        self.btn_play.config(text="Play")
        if self.after_id is not None:
            try:
                self.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

    def _schedule_next_frame(self):
        if not self.is_playing:
            return
        delay = self._get_delay_ms()
        self.after_id = self.after(delay, self._play_step)

    def _play_step(self):
        if not self.is_playing:
            return
        self.grid_data = step_grid(self.grid_data, stuck_corners=self.stuck_corners_var.get())
        self.step_count += 1
        self._draw_grid()
        self._update_status()
        self._schedule_next_frame()


def main():
    here = Path(__file__).resolve().parent
    input_path = here / "input.txt"

    if not input_path.exists():
        raise SystemExit(f"input.txt не найден рядом со скриптом: {input_path}")

    raw = input_path.read_text(encoding="utf-8")
    grid = parse_grid(raw)

    app = LightsApp(grid)
    app.mainloop()


if __name__ == "__main__":
    main()
