import tkinter as tk
from tkinter import colorchooser, simpledialog

# ===================== START SIZE =====================
root = tk.Tk()
root.withdraw()

WIDTH = simpledialog.askinteger("Width", "Enter width:")
HEIGHT = simpledialog.askinteger("Height", "Enter height:")

if not WIDTH or not HEIGHT:
    WIDTH, HEIGHT = 1000, 700

root.destroy()

# ===================== MAIN WINDOW =====================
window = tk.Tk()
window.title("TUX PAINT")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.configure(bg="#1e1e1e")

# ===================== STATE =====================
current_color = "#000000"
brush_size = 4
eraser = False
darkmode = True

drawing = False
last_x = 0
last_y = 0

grid_on = False
grid_lines = []

pixel_mode = False

# ===================== THEMES =====================
themes = {
    "Dark": {
        "bg": "#1e1e1e",
        "top": "#2a2a2a",
        "side": "#252525",
        "canvas": "#ffffff"
    },

    "Light": {
        "bg": "#f0f0f0",
        "top": "#dddddd",
        "side": "#e6e6e6",
        "canvas": "#ffffff"
    },

    "Synthwave": {
        "bg": "#241734",
        "top": "#ff00ff",
        "side": "#2d1b4e",
        "canvas": "#fff7ff"
    },

    "Hacker": {
        "bg": "#000000",
        "top": "#101010",
        "side": "#050505",
        "canvas": "#0f0f0f"
    }
}

# ===================== LAYOUT =====================
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

# ===================== TOP BAR =====================
topbar = tk.Frame(window, bg="#2a2a2a", height=50)
topbar.grid(row=0, column=0, columnspan=2, sticky="nsew")

# ===================== TOOLBAR =====================
toolbar = tk.Frame(window, bg="#252525", width=120)
toolbar.grid(row=1, column=0, sticky="nsew")

# ===================== CANVAS =====================
canvas = tk.Canvas(window, bg="#ffffff", highlightthickness=0)
canvas.grid(row=1, column=1, sticky="nsew")

# ===================== DRAW SYSTEM =====================
def start_draw(e):
    global drawing, last_x, last_y
    drawing = True
    last_x, last_y = e.x, e.y

def draw(e):
    global last_x, last_y

    if not drawing:
        return

    color = "white" if eraser else current_color

    # PIXEL MODE
    if pixel_mode:
        size = brush_size * 4

        canvas.create_rectangle(
            e.x,
            e.y,
            e.x + size,
            e.y + size,
            fill=color,
            outline=color
        )

    # NORMAL MODE
    else:
        canvas.create_line(
            last_x, last_y,
            e.x, e.y,
            fill=color,
            width=brush_size,
            capstyle=tk.ROUND,
            smooth=True
        )

    last_x, last_y = e.x, e.y

def stop_draw(e):
    global drawing
    drawing = False

canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

# ===================== TOOLS =====================
def set_color(c):
    global current_color, eraser
    current_color = c
    eraser = False

def toggle_eraser():
    global eraser
    eraser = not eraser

def set_brush(val):
    global brush_size
    brush_size = int(val)

def clear_canvas():
    canvas.delete("all")

    # redraw grid if active
    if grid_on:
        draw_grid()

def pick_color():
    global current_color, eraser

    c = colorchooser.askcolor()[1]

    if c:
        current_color = c
        eraser = False

# ===================== GRID MODE =====================
def draw_grid():
    global grid_lines

    spacing = 20

    for x in range(0, WIDTH, spacing):
        line = canvas.create_line(
            x, 0, x, HEIGHT,
            fill="#d0d0d0"
        )
        grid_lines.append(line)

    for y in range(0, HEIGHT, spacing):
        line = canvas.create_line(
            0, y, WIDTH, y,
            fill="#d0d0d0"
        )
        grid_lines.append(line)

def toggle_grid():
    global grid_on, grid_lines

    grid_on = not grid_on

    # remove old grid
    for line in grid_lines:
        canvas.delete(line)

    grid_lines.clear()

    if grid_on:
        draw_grid()

# ===================== PIXEL MODE =====================
def toggle_pixel_mode():
    global pixel_mode
    pixel_mode = not pixel_mode

# ===================== THEMES =====================
def apply_theme(name):
    t = themes[name]

    window.configure(bg=t["bg"])
    topbar.config(bg=t["top"])
    toolbar.config(bg=t["side"])
    canvas.config(bg=t["canvas"])

# ===================== SETTINGS =====================
def open_settings():

    current_bg = window["bg"]
    current_top = topbar["bg"]

    win = tk.Toplevel(window)
    win.title("Settings")
    win.geometry("340x700")
    win.config(bg=current_bg)
    win.resizable(False, False)

    # ================= TITLE =================
    tk.Label(
        win,
        text="Settings Panel",
        fg="white",
        bg=current_bg,
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    # ================= COLOR PICKER =================
    tk.Button(
        win,
        text="Color Picker",
        command=pick_color,
        bg=current_top,
        fg="white",
        relief="flat",
        font=("Arial", 10, "bold"),
        activebackground=current_top,
        activeforeground="white",
        cursor="hand2"
    ).pack(pady=6, ipadx=10, ipady=5)

    # ================= CLEAR =================
    tk.Button(
        win,
        text="Clear Canvas",
        command=clear_canvas,
        bg=current_top,
        fg="white",
        relief="flat",
        font=("Arial", 10, "bold"),
        activebackground=current_top,
        activeforeground="white",
        cursor="hand2"
    ).pack(pady=6, ipadx=10, ipady=5)

    # ================= BRUSH SIZE =================
    tk.Label(
        win,
        text="Brush Size",
        fg="white",
        bg=current_bg,
        font=("Arial", 10)
    ).pack(pady=(20, 5))

    tk.Scale(
        win,
        from_=1,
        to=20,
        orient="horizontal",
        command=set_brush,
        bg=current_bg,
        fg="white",
        troughcolor=current_top,
        highlightthickness=0
    ).pack()

    # ================= THEMES =================
    tk.Label(
        win,
        text="Themes",
        fg="white",
        bg=current_bg,
        font=("Arial", 12, "bold")
    ).pack(pady=(25, 10))

    # THEME BUTTON CREATOR
    def theme_btn(name, color):
        tk.Button(
            win,
            text=name,
            command=lambda: apply_theme(name),

            bg=color,
            fg="white",

            activebackground=color,
            activeforeground="white",

            relief="flat",
            bd=0,

            font=("Arial", 9, "bold"),
            cursor="hand2"

        ).pack(fill="x", padx=40, pady=3, ipady=5)

    # THEME BUTTONS
    theme_btn("Dark", "#2b2b2b")
    theme_btn("Light", "#aaaaaa")
    theme_btn("Synthwave", "#ff00ff")
    theme_btn("Hacker", "#00aa44")
    theme_btn("Ocean", "#0284c7")
    theme_btn("Sunset", "#ff7b00")
    theme_btn("Matrix", "#00ff00")
    theme_btn("Ice", "#47b5ff")

    # ================= CLOSE BUTTON =================
    tk.Button(
        win,
        text="Close",
        command=win.destroy,
        bg="#444444",
        fg="white",
        relief="flat",
        font=("Arial", 10, "bold"),
        cursor="hand2"
    ).pack(pady=25, ipadx=10, ipady=5)

# ===================== ABOUT =====================
def open_about():
    win = tk.Toplevel(window)
    win.title("About App")
    win.geometry("350x250")
    win.config(bg="#2a2a2a")
    win.resizable(False, False)

    tk.Label(
        win,
        text="TUX PAINT",
        fg="white",
        bg="#2a2a2a",
        font=("Arial", 18, "bold")
    ).pack(pady=(20, 10))

    tk.Label(
        win,
        text="A Almost 98 themed paint app made with Tkinter.",
        fg="#d0d0d0",
        bg="#2a2a2a",
        font=("Arial", 11),
        wraplength=280,
        justify="center"
    ).pack(pady=5)

    tk.Label(
        win,
        text="Made by Techx32",
        fg="white",
        bg="#2a2a2a",
        font=("Arial", 10, "bold")
    ).pack(pady=(20, 5))

    tk.Label(
        win,
        text="Powered by Python and Linux",
        fg="#aaaaaa",
        bg="#2a2a2a",
        font=("Arial", 10)
    ).pack()

    tk.Button(
        win,
        text="Close",
        command=win.destroy,
        bg="#444444",
        fg="white",
        relief="flat",
        padx=15
    ).pack(pady=20)

# ===================== TOOLBAR BUTTONS =====================
tk.Button(toolbar, text="Black",
          command=lambda: set_color("black")).pack(pady=5, fill="x")

tk.Button(toolbar, text="Red",
          command=lambda: set_color("red")).pack(pady=5, fill="x")

tk.Button(toolbar, text="Blue",
          command=lambda: set_color("blue")).pack(pady=5, fill="x")

tk.Button(toolbar, text="Green",
          command=lambda: set_color("green")).pack(pady=5, fill="x")

tk.Button(toolbar, text="Orange",
          command=lambda: set_color("orange")).pack(pady=5, fill="x")

tk.Button(toolbar, text="Pick Color",
          command=pick_color).pack(pady=5, fill="x")

tk.Button(toolbar, text="Eraser",
          command=toggle_eraser).pack(pady=10, fill="x")

tk.Button(toolbar, text="Pixel Mode",
          command=toggle_pixel_mode).pack(pady=5, fill="x")

tk.Button(toolbar, text="Grid",
          command=toggle_grid).pack(pady=5, fill="x")

tk.Button(toolbar, text="Clear",
          command=clear_canvas).pack(pady=5, fill="x")


# ===================== TOPBAR BUTTONS =====================
tk.Button(topbar, text="Settings",
          command=open_settings).pack(side="right", padx=10)

tk.Button(topbar, text="About",
          command=open_about).pack(side="right", padx=10)

tk.Button(topbar, text="Exit",
          command=window.destroy).pack(side="right", padx=10)

# ===================== START =====================
window.mainloop()