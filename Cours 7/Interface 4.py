import tkinter as tk
from tkinter import messagebox


class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Démo des Messagebox")
        self.geometry("400x200")

        #Labels
        tk.Label(self, text="Boites de messages Tkinter", font=("Arial", 18, "bold")).pack(pady= (10,4))
        tk.Label(self, text="Cliquer sur un bouton pour afficher un type de message").pack(pady= 4)

        #barre de bouton
        bar = tk.Frame(self)
        bar.pack(pady= 10, fill= "x", padx= 10)

        tk.Button(bar, text="Info", command=self.show_info).pack(pady= 10, side="left", expand= True)
        tk.Button(bar, text="Avertissement", command=self.show_warning).pack(pady=10, side="left", expand=True)
        tk.Button(bar, text="Erreur", command=self.show_erreur).pack(pady=10, side="left", expand=True)

    def show_info(self):
        messagebox.showinfo("Info", "Ceci est une information")

    def show_warning(self):
        messagebox.showwarning("Warning", "Ceci est un warning")

    def show_erreur(self):
        messagebox.showerror("Erreur", "Ceci est un erreur")



if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()