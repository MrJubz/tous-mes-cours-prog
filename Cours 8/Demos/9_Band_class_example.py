import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Band Class Example")
        self.geometry("300x300")
        row = ttk.Frame(self)
        row.pack(padx=12, pady=12)
        for t in ("A","B","C"):
            ttk.Button(row, text=f"Bouton {t}").pack(side="left", padx=6)
        self.bind_class("TButton", "<Enter>", self.on_hover)

    def on_hover(self, e):
        self.title(f"Survol: {e.widget.cget('text')}")

if __name__ == "__main__":
    App().mainloop()
