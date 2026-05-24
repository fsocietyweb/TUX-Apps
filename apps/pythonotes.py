# notes.py
# Windows 7 Dark Themed Notes App

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_NAME = "TUX Notes"
FILE_EXTENSION = ".pynote"

# Get folder where this python file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Save folder inside program folder
SAVE_DIR = os.path.join(BASE_DIR, "save")

# Create save folder automatically
os.makedirs(SAVE_DIR, exist_ok=True)


class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TUX Notes")
        self.root.geometry("1000x650")
        self.root.minsize(800, 500)

        self.current_file = None

        self.setup_theme()
        self.create_ui()
        self.load_notes_list()

    def setup_theme(self):
        self.bg = "#1e1e1e"
        self.sidebar = "#252526"
        self.text_bg = "#2d2d30"
        self.text_fg = "#ffffff"
        self.button_bg = "#3a3d41"
        self.button_hover = "#4b4f54"
        self.border = "#555555"
        self.accent = "#0078d7"

        self.root.configure(bg=self.bg)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Dark.TButton",
            background=self.button_bg,
            foreground="white",
            borderwidth=1,
            padding=6,
        )

        style.map(
            "Dark.TButton",
            background=[("active", self.button_hover)],
        )

        style.configure(
            "Dark.TFrame",
            background=self.bg
        )

        style.configure(
            "Sidebar.TFrame",
            background=self.sidebar
        )

    def create_ui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Dark.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar_frame = ttk.Frame(
            self.main_frame,
            style="Sidebar.TFrame",
            width=250
        )
        self.sidebar_frame.pack(side="left", fill="y")

        # App title
        title = tk.Label(
            self.sidebar_frame,
            text="TUX Notes",
            bg=self.sidebar,
            fg="white",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=15)

        # Buttons
        self.new_button = ttk.Button(
            self.sidebar_frame,
            text="New Note",
            style="Dark.TButton",
            command=self.new_note
        )
        self.new_button.pack(fill="x", padx=10, pady=5)

        self.save_button = ttk.Button(
            self.sidebar_frame,
            text="Save Note",
            style="Dark.TButton",
            command=self.save_note
        )
        self.save_button.pack(fill="x", padx=10, pady=5)

        self.delete_button = ttk.Button(
            self.sidebar_frame,
            text="Delete Note",
            style="Dark.TButton",
            command=self.delete_note
        )
        self.delete_button.pack(fill="x", padx=10, pady=5)

        self.about_button = ttk.Button(
            self.sidebar_frame,
            text="About",
            style="Dark.TButton",
            command=self.show_about
        )
        self.about_button.pack(fill="x", padx=10, pady=5)

        # Notes label
        notes_label = tk.Label(
            self.sidebar_frame,
            text="Saved Notes",
            bg=self.sidebar,
            fg="#cccccc",
            font=("Segoe UI", 10)
        )
        notes_label.pack(anchor="w", padx=10, pady=(20, 5))

        # Notes list
        self.notes_listbox = tk.Listbox(
            self.sidebar_frame,
            bg=self.text_bg,
            fg="white",
            selectbackground=self.accent,
            selectforeground="white",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.border,
            font=("Consolas", 11)
        )
        self.notes_listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.notes_listbox.bind("<<ListboxSelect>>", self.open_selected_note)

        # Editor frame
        self.editor_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.editor_frame.pack(side="right", fill="both", expand=True)

        # File label
        self.file_label = tk.Label(
            self.editor_frame,
            text="No file selected",
            bg=self.bg,
            fg="#cccccc",
            font=("Segoe UI", 10)
        )
        self.file_label.pack(anchor="w", padx=10, pady=5)

        # Text editor
        self.text_area = tk.Text(
            self.editor_frame,
            wrap="word",
            undo=True,
            bg=self.text_bg,
            fg=self.text_fg,
            insertbackground="white",
            selectbackground=self.accent,
            borderwidth=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=self.border,
            font=("Consolas", 12)
        )
        self.text_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def load_notes_list(self):
        self.notes_listbox.delete(0, tk.END)

        files = sorted(os.listdir(SAVE_DIR))

        for file in files:
            if file.endswith(FILE_EXTENSION) or file.endswith(".txt"):
                self.notes_listbox.insert(tk.END, file)

    def new_note(self):
        self.current_file = None
        self.text_area.delete("1.0", tk.END)
        self.file_label.config(text="New Note")

    def save_note(self):
        content = self.text_area.get("1.0", tk.END).strip()

        if not content:
            messagebox.showwarning("Empty Note", "Cannot save an empty note.")
            return

        if self.current_file is None:
            filename = filedialog.asksaveasfilename(
                initialdir=SAVE_DIR,
                defaultextension=FILE_EXTENSION,
                filetypes=[
                    ("PyNotes Files", "*.pynote"),
                    ("Text Files", "*.txt")
                ],
                title="Save Note"
            )

            if not filename:
                return

            self.current_file = filename

        with open(self.current_file, "w", encoding="utf-8") as file:
            file.write(content)

        name = os.path.basename(self.current_file)

        self.file_label.config(text=name)

        self.load_notes_list()

        messagebox.showinfo("Saved", f"Saved:\n{name}")

    def open_selected_note(self, event=None):
        selection = self.notes_listbox.curselection()

        if not selection:
            return

        filename = self.notes_listbox.get(selection[0])

        path = os.path.join(SAVE_DIR, filename)

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)

            self.current_file = path

            self.file_label.config(text=filename)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_note(self):
        selection = self.notes_listbox.curselection()

        if not selection:
            messagebox.showwarning("No Selection", "Select a note to delete.")
            return

        filename = self.notes_listbox.get(selection[0])

        path = os.path.join(SAVE_DIR, filename)

        confirm = messagebox.askyesno(
            "Delete Note",
            f"Delete '{filename}'?"
        )

        if confirm:
            try:
                os.remove(path)

                self.text_area.delete("1.0", tk.END)

                self.current_file = None

                self.file_label.config(text="No file selected")

                self.load_notes_list()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def show_about(self):
        about_text = (
            "Made by techx32\n\n"
            "Powered by Python\n"
            "and Linux free use"
        )

        messagebox.showinfo("About PyNotes", about_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()