"""Gabarit : application Tkinter avec PLACE (positions relatives → s'adapte au redimensionnement).

Règle : relx/rely/relwidth/relheight entre 0 et 1, relatifs au PARENT (fenêtre ou frame).
"""
import tkinter as tk
from tkinter import ttk, messagebox

CATEGORIES = ["Catégorie 1", "Catégorie 2", "Catégorie 3"]


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application avec place()")
        self.geometry("700x500")
        self.create_widgets()

    def create_widgets(self):
        # ---------- Titres centrés : relx=0.5 + anchor="n" (haut-centre du widget sur le point) ----------
        tk.Label(self, text="TITRE PRINCIPAL", font=("Arial", 18, "bold")).place(relx=0.5, rely=0.02, anchor="n")
        tk.Label(self, text="Sous-titre").place(relx=0.5, rely=0.09, anchor="n")

        # ---------- Deux cadres côte à côte : 5 % marge | 42 % | 6 % espace | 42 % | 5 % marge ----------
        frame_gauche = tk.LabelFrame(self, text="SAISIE", font=("Arial", 9, "bold"))
        frame_gauche.place(relx=0.05, rely=0.15, relwidth=0.42, relheight=0.5)

        frame_droite = tk.LabelFrame(self, text="RÉSULTAT", font=("Arial", 9, "bold"))
        frame_droite.place(relx=0.53, rely=0.15, relwidth=0.42, relheight=0.5)

        # ---------- Dans un frame : les rel* sont relatifs AU FRAME, pas à la fenêtre ----------
        # Patron « label au-dessus, champ en dessous » : rely du label, puis rely + 0.09 pour le champ
        tk.Label(frame_gauche, text="Nom").place(relx=0.08, rely=0.05)
        self.entry_nom = tk.Entry(frame_gauche)
        self.entry_nom.place(relx=0.08, rely=0.14, relwidth=0.84)

        tk.Label(frame_gauche, text="Courriel").place(relx=0.08, rely=0.28)
        self.entry_courriel = tk.Entry(frame_gauche)
        self.entry_courriel.place(relx=0.08, rely=0.37, relwidth=0.84)

        tk.Label(frame_gauche, text="Catégorie").place(relx=0.08, rely=0.51)
        self.combo = ttk.Combobox(frame_gauche, values=CATEGORIES, state="readonly")
        self.combo.place(relx=0.08, rely=0.60, relwidth=0.84)
        self.combo.current(0)

        tk.Label(frame_gauche, text="Quantité").place(relx=0.08, rely=0.74)
        self.entry_quantite = tk.Entry(frame_gauche)
        self.entry_quantite.place(relx=0.08, rely=0.83, relwidth=0.84)

        self.label_resultat = tk.Label(frame_droite, text="---", justify="left", anchor="nw", wraplength=260)
        self.label_resultat.place(relx=0.08, rely=0.08, relwidth=0.84, relheight=0.84)

        # ---------- Boutons alignés : même relwidth, relx décalé ----------
        tk.Button(self, text="VALIDER", command=self.valider).place(relx=0.25, rely=0.69, relwidth=0.15)
        tk.Button(self, text="EFFACER", command=self.effacer).place(relx=0.425, rely=0.69, relwidth=0.15)
        tk.Button(self, text="QUITTER", command=self.destroy).place(relx=0.60, rely=0.69, relwidth=0.15)

        # ---------- Bandeau du bas ----------
        frame_statut = tk.LabelFrame(self, text="STATUT")
        frame_statut.place(relx=0.05, rely=0.78, relwidth=0.9, relheight=0.15)
        self.label_statut = tk.Label(frame_statut, text="Prêt", anchor="w")
        self.label_statut.place(relx=0.02, rely=0.1, relwidth=0.96)

        # Positions absolues (pixels) — fixes, ne bougent pas si on agrandit :
        # widget.place(x=100, y=50, width=150, height=40)

    def valider(self):
        nom = self.entry_nom.get().strip()
        courriel = self.entry_courriel.get().strip()
        try:
            quantite = int(self.entry_quantite.get())
        except ValueError:
            messagebox.showerror("Erreur", "La quantité doit être un entier.")
            return
        if not nom or "@" not in courriel or quantite <= 0:
            messagebox.showerror("Erreur", "Nom obligatoire, courriel avec @, quantité > 0.")
            return
        self.label_resultat.config(text=f"Nom : {nom}\nCourriel : {courriel}\n"
                                        f"Catégorie : {self.combo.get()}\nQuantité : {quantite}")
        self.label_statut.config(text=f"{nom} enregistré.")

    def effacer(self):
        for entry in (self.entry_nom, self.entry_courriel, self.entry_quantite):
            entry.delete(0, tk.END)
        self.combo.current(0)
        self.label_resultat.config(text="---")
        self.label_statut.config(text="Prêt")


if __name__ == "__main__":
    Application().mainloop()
