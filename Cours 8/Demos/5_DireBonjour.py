import tkinter as tk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bonjour ")
        self.geometry("300x200")

        self.creer_widget()

    def creer_widget(self):
        btn = tk.Button(self, text="Cliquez-moi", command=self.dire_bonjour)
        btn.pack(expand=True)

    def dire_bonjour(self):
        messagebox.showinfo("salutation", "Bonjour")

# Démarrer l'application
if __name__ == "__main__":
    App().mainloop()

