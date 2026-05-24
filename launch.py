import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

# =========================
# CONFIG
# =========================
TOOLS_FOLDER = "apps"
APP_NAME = "TUX UTIL"

# =========================
# MAIN APP
# =========================
class ToolLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("800x600")
        self.root.configure(bg="#c0c0c0")  # Windows 9X style

        # Top header
        header = tk.Label(
            root,
            text="TUX UTIL",
            font=("Tahoma", 22, "bold"),
            bg="#000080",
            fg="white",
            pady=10
        )
        header.pack(fill="x")

        # Subtitle
        subtitle = tk.Label(
            root,
            text="Select a tool to launch",
            font=("Tahoma", 11),
            bg="#c0c0c0",
            fg="black"
        )
        subtitle.pack(pady=10)

        # Tool area
        self.tool_frame = tk.Frame(root, bg="#c0c0c0")
        self.tool_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # About button
        about_btn = tk.Button(
            root,
            text="About",
            font=("Tahoma", 10, "bold"),
            bg="#d4d0c8",
            fg="black",
            relief="raised",
            bd=2,
            cursor="hand2",
            command=self.show_about
        )
        about_btn.pack(pady=10)

        self.load_tools()

    # =========================
    # LOAD TOOLS
    # =========================
    def load_tools(self):
        if not os.path.exists(TOOLS_FOLDER):
            messagebox.showerror("Error", f"'{TOOLS_FOLDER}' folder not found.")
            return

        tool_files = [f for f in os.listdir(TOOLS_FOLDER) if f.endswith(".py")]

        if not tool_files:
            messagebox.showinfo("No Tools", "No Python tools found in tools/ folder.")
            return

        for tool in tool_files:
            tool_name = tool.replace(".py", "")

            btn = tk.Button(
                self.tool_frame,
                text=tool_name,
                font=("Tahoma", 11, "bold"),
                bg="#d4d0c8",
                fg="black",
                relief="raised",
                bd=2,
                cursor="hand2",
                command=lambda t=tool: self.run_tool(t)
            )
            btn.pack(fill="x", pady=6)

    # =========================
    # RUN TOOL
    # =========================
    def run_tool(self, tool_file):
        path = os.path.join(TOOLS_FOLDER, tool_file)

        try:
            subprocess.Popen([sys.executable, path])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =========================
    # ABOUT WINDOW (500x600)
    # =========================
    def show_about(self):
        about = tk.Toplevel(self.root)
        about.title("About TUX UTIL")
        about.geometry("500x600")
        about.configure(bg="#c0c0c0")

        title = tk.Label(
            about,
            text="TUX UTIL",
            font=("Tahoma", 18, "bold"),
            bg="#000080",
            fg="white",
            pady=10
        )
        title.pack(fill="x")

        info = """
Created By:
Techx32

Created On:
24 May 2026

Theme:
Windows 9X
"""

        label = tk.Label(
            about,
            text=info,
            font=("Tahoma", 11),
            bg="#c0c0c0",
            fg="black",
            justify="left"
        )
        label.pack(padx=15, pady=20, anchor="w")


# =========================
# START APP
# =========================
root = tk.Tk()
app = ToolLauncher(root)
root.mainloop()