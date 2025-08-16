import tkinter as tk

HEADER_TEXTS = [
    ("Bus direction", "Delay"),
    ("Bus1", "0 min"),
    ("Bus2", "0 min"),
]

LINE_COLOR = "white"
TEXT_COLOR = "white"
BG_COLOR = "black"

FONT_HEADER = ("Segoe UI", 32, "bold")
# Removed fixed large font; will compute dynamically
# FONT_CELL = ("Segoe UI", 72, "bold")

ROW_RATIOS = [0.18, 0.41, 0.41]

def draw_grid(canvas):
    canvas.delete("all")
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    cols = 2
    col_w = w / cols

    cumulative = [0]
    for ratio in ROW_RATIOS:
        cumulative.append(cumulative[-1] + ratio)

    for i in range(1, len(cumulative) - 1):
        y = int(cumulative[i] * h)
        canvas.create_line(0, y, w, y, fill=LINE_COLOR, width=4)

    x_mid = int(col_w)
    canvas.create_line(x_mid, 0, x_mid, h, fill=LINE_COLOR, width=4)

    canvas.create_rectangle(2, 2, w - 2, h - 2, outline=LINE_COLOR, width=4)

    for r in range(3):
        row_top = cumulative[r] * h
        row_bottom = cumulative[r + 1] * h
        row_height = row_bottom - row_top
        cy = (row_top + row_bottom) / 2
        for c in range(cols):
            cx = (c + 0.5) * col_w
            if r == 0:
                font = FONT_HEADER
            else:
                # Dynamic font size (~40% of row height)
                size = int(row_height * 0.40)
                font = ("Segoe UI", size, "bold")
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

    root.mainloop()

if __name__ == "__main__":
    main()