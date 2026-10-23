import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Event handlers")
        self.geometry("300x300")
        self.var = tk.StringVar()
        entry = ttk.Entry(self, textvariable=self.var, width=30)
        entry.pack(padx=12, pady=8)
        entry.bind("<Return>", self.on_return)
        self.msg = ttk.Label(self, text="Tapez puis Entrée")
        self.msg.pack()

    def on_return(self, event):
        self.msg.config(text=f"Vous avez saisi : {self.var.get()}")

if __name__ == "__main__":
    App().mainloop()
