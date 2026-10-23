import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("virtual_event_example")
        self.geometry("400x300")

        self.combo = ttk.Combobox(
            self,
            values=["A", "B", "C"],
            state="readonly"
        )
        self.combo.pack(padx=12, pady=6)
        self.combo.bind("<<ComboboxSelected>>", self.on_combo)

        self.v = tk.StringVar()

        ttk.Entry( self,textvariable=self.v).pack(padx=12, pady=6)

        ttk.Button(self,text="Valider", command=self.fire_valid
        ).pack()

        self.bind( "<<FormValid>>", lambda e: self.title("Formulaire valide !")
        )

    def on_combo(self, e):
        self.title(f"Sélection: {self.combo.get()}")

    def fire_valid(self):
        if self.v.get().strip():
            self.event_generate("<<FormValid>>")


if __name__ == "__main__":
    App().mainloop()