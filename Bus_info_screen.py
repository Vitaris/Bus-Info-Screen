import tkinter as tk

HEADER_TEXTS = [
    ("Smer", "Mešká"),
    ("Pezinok", "0 min"),
    ("Bratislava", "0 min"),
]

# Per‑cell background colors (None = uses global BG_COLOR)
CELL_BG_COLORS = [
    (None, None),
    ("#004400", "#220000"),   # Row 1 (index 1)
    ("#003366", "#331100"),   # Row 2 (index 2)
]

# Cells that should flash: (row_index, col_index): {alt: alt_color, interval: ms}
# This example flashes the Pezinok delay cell (row 1, col 1).
FLASH_CELLS = {
    (1, 1): {"alt": "#ff0000", "interval": 700},
}

LINE_COLOR = "white"
TEXT_COLOR = "white"
BG_COLOR = "black"

FONT_HEADER = ("Segoe UI", 32, "bold")
ROW_RATIOS = [0.18, 0.41, 0.41]

# Will hold rectangle item IDs for each cell: (r, c) -> canvas id
CELL_RECTS = {}

def draw_grid(canvas):
    canvas.delete("all")
    CELL_RECTS.clear()

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    rows = len(HEADER_TEXTS)
    cols = len(HEADER_TEXTS[0])
    col_w = w / cols

    cumulative = [0]
    for ratio in ROW_RATIOS:
        cumulative.append(cumulative[-1] + ratio)

    # Cell backgrounds
    for r in range(rows):
        row_top = cumulative[r] * h
        row_bottom = cumulative[r + 1] * h
        for c in range(cols):
            x0 = c * col_w
            x1 = (c + 1) * col_w
            base_color = CELL_BG_COLORS[r][c] if CELL_BG_COLORS[r][c] else BG_COLOR
            rect_id = canvas.create_rectangle(
                x0, row_top, x1, row_bottom,
                fill=base_color, outline=""
            )
            CELL_RECTS[(r, c)] = rect_id

    # Grid lines
    for i in range(1, len(cumulative) - 1):
        y = int(cumulative[i] * h)
        canvas.create_line(0, y, w, y, fill=LINE_COLOR, width=4)

    for c in range(1, cols):
        x = int(c * col_w)
        canvas.create_line(x, 0, x, h, fill=LINE_COLOR, width=4)

    canvas.create_rectangle(2, 2, w - 2, h - 2, outline=LINE_COLOR, width=4)

    # Text
    for r in range(rows):
        row_top = cumulative[r] * h
        row_bottom = cumulative[r + 1] * h
        row_height = row_bottom - row_top
        cy = (row_top + row_bottom) / 2
        for c in range(cols):
            cx = (c + 0.5) * col_w
            font = FONT_HEADER if r == 0 else ("Segoe UI", int(row_height * 0.20), "bold")
            canvas.create_text(
                cx, cy,
                text=HEADER_TEXTS[r][c],
                fill=TEXT_COLOR,
                font=font
            )

def main():
    root = tk.Tk()
    root.title("Bus Info Screen")
    root.configure(bg=BG_COLOR)
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("q", lambda e: root.destroy())

    canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.bind("<Configure>", lambda e: draw_grid(canvas))

    flash_state = {"on": False}

    def flash_step():
        # Toggle state
        flash_state["on"] = not flash_state["on"]
        for (r, c), cfg in FLASH_CELLS.items():
            rect_id = CELL_RECTS.get((r, c))
            if not rect_id:
                continue
            base = CELL_BG_COLORS[r][c] if CELL_BG_COLORS[r][c] else BG_COLOR
            alt = cfg["alt"]
            fill = alt if flash_state["on"] else base
            canvas.itemconfig(rect_id, fill=fill)
            # Schedule next based on this cell's interval (all share same schedule if multiple)
            interval = cfg.get("interval", 700)
        # Use the shortest interval among flashing cells
        next_interval = min(cfg.get("interval", 700) for cfg in FLASH_CELLS.values())
        root.after(next_interval, flash_step)

    # Initial draw then start flashing shortly after
    root.after(50, lambda: (draw_grid(canvas), flash_step()))

    root.mainloop()

if __name__ == "__main__":
    main()