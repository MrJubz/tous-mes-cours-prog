import tkinter as tk
from tkinter import messagebox


class Calculatrice(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x400")
        self.num1 = ""
        self.num2 = ""
        self.operation = ""
        self.create_widgets()

    def create_widgets(self):
        for col in range(4):
            self.columnconfigure(col, weight=1)
        for row in range(1, 6):
            self.rowconfigure(row, weight=1)

        self.affichage = tk.Label(self, text="0", font=("Arial", 20, "bold"), bg="white",
                                  anchor="e", relief="groove", borderwidth=8)
        self.affichage.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

        # (texte, ligne, colonne, columnspan) : une seule boucle crée les 18 boutons
        boutons = [
            ("C", 1, 0, 2), ("/", 1, 2, 1), ("*", 1, 3, 1),
            ("7", 2, 0, 1), ("8", 2, 1, 1), ("9", 2, 2, 1), ("-", 2, 3, 1),
            ("4", 3, 0, 1), ("5", 3, 1, 1), ("6", 3, 2, 1), ("+", 3, 3, 1),
            ("1", 4, 0, 1), ("2", 4, 1, 1), ("3", 4, 2, 1), ("=", 4, 3, 1),
            ("0", 5, 0, 2), (".", 5, 2, 2),
        ]
        for texte, row, col, span in boutons:
            # t=texte fige la valeur ; sans ça, tous les boutons enverraient "." (la dernière valeur de la boucle)
            tk.Button(self, text=texte, font=("Arial", 15, "bold"),
                      command=lambda t=texte: self.on_click(t)).grid(
                row=row, column=col, columnspan=span, sticky="nsew")

    def on_click(self, valeur):
        if valeur.isdigit() or valeur == ".":
            if self.operation == "":
                self.num1 += valeur
            else:
                self.num2 += valeur
        elif valeur == "C":
            self.effacer()
        elif valeur == "=":
            self.calculer()
        elif self.num1 != "":
            self.operation = valeur
        self.rafraichir()

    def rafraichir(self):
        texte = self.num1 + self.operation + self.num2
        self.affichage.config(text=texte or "0")

    def effacer(self):
        self.num1 = ""
        self.num2 = ""
        self.operation = ""

    def calculer(self):
        if self.num1 == "" or self.num2 == "" or self.operation == "":
            messagebox.showerror("Erreur", "Entrez deux nombres et un opérateur.")
            return
        try:
            a = float(self.num1)
            b = float(self.num2)
        except ValueError:
            messagebox.showerror("Erreur", "Nombre invalide (ex. deux points).")
            self.effacer()
            return

        if self.operation == "+":
            resultat = a + b
        elif self.operation == "-":
            resultat = a - b
        elif self.operation == "*":
            resultat = a * b
        else:
            if b == 0:
                messagebox.showerror("Erreur", "Division par zéro impossible.")
                return
            resultat = a / b

        self.num1 = str(resultat)
        self.num2 = ""
        self.operation = ""


if __name__ == "__main__":
    Calculatrice().mainloop()
