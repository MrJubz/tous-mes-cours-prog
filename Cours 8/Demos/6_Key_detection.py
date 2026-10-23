import tkinter as tk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Détecteur de touches")
        self.geometry("400x400")
        self.creer_widget()

    def creer_widget(self):
        self.champ = tk.Entry(self)
        self.champ.pack()
        self.champ.bind("<KeyRelease>", self.touche_appuyee)

    def touche_appuyee(self, event):
        #print("Touche appuyée :", repr(event.char)) # s'affiche dans le console
        messagebox.showinfo("Touche appuyee", repr(event.char))
        # repr(event.char) obtenir la représentation textuelle d'un caractère

if __name__ == "__main__":
    app = App()
    app.mainloop()
