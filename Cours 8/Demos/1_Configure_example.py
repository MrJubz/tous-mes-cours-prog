import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configure Example")
        self.geometry("300x200")
        self.lbl = tk.Label(self, text="Bonjour")
        self.lbl.pack(padx=10, pady=10)
        tk.Button(self, text="Mettre à jour", command=self.maj).pack()

    def maj(self):
        self.lbl.configure(text="Salut !")
        print("Texte actuel =", self.lbl.cget("text"))

if __name__ == "__main__":
    App().mainloop()
