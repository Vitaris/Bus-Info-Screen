import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Bus Info Screen")
    root.configure(bg="black")

    # Fullscreen (Esc or q to exit)
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("q", lambda e: root.destroy())

    label = tk.Label(
        root,
        text="Bus",
        font=("Segoe UI", 180, "bold"),
        fg="white",
        bg="black"
    )
    label.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()