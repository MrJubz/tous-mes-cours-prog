import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Event handlers")
        self.geometry("300x300")
        self.box = ttk.Label(self, text="(Ctrl+H) — Afficher/Masquer")
        self.box.pack(padx=12, pady=12)
        self.bind_all("<Control-h>", self.basculer)

    def basculer(self, e=None):
        if self.box.winfo_viewable():
            self.box.pack_forget()
        else:
            self.box.pack()

if __name__ == "__main__":
    App().mainloop()
