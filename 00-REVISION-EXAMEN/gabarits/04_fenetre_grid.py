"""Gabarit : application Tkinter avec GRID (formulaire + calcul + résumé + boutons).

Pour un nouvel exercice : copier ce fichier, renommer les champs, garder la structure.
"""
import tkinter as tk
from tkinter import ttk, messagebox

PRIX_FORFAITS = {"Base": 50, "Plus": 80, "Premium": 120}
PRIX_OPTIONS = {"Option A": 10, "Option B": 15, "Option C": 25}
DUREES = {"1 mois": 1, "3 mois": 3, "6 mois": 6}


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Titre de la fenêtre")
        self.geometry("650x520")
        self.create_widgets()
        self.reinitialiser()

    def create_widgets(self):
        # Fenêtre principale : 2 colonnes (gauche plus large) ; la ligne 2 prend l'espace vertical
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # ---------- Titre sur toute la largeur (columnspan=2) ----------
        tk.Label(self, text="TITRE DE L'APPLICATION", bg="navy", fg="white",
                 font=("Arial", 16, "bold"), pady=6).grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # ---------- Cadre formulaire : label (col 0) + champ (col 1) ----------
        frame_form = tk.LabelFrame(self, text="Informations", padx=10, pady=10)
        frame_form.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        frame_form.columnconfigure(1, weight=1)  # la colonne des champs s'étire

        tk.Label(frame_form, text="Nom :").grid(row=0, column=0, sticky="e", pady=3)
        self.entry_nom = tk.Entry(frame_form)
        self.entry_nom.grid(row=0, column=1, sticky="ew", pady=3)

        tk.Label(frame_form, text="Quantité :").grid(row=1, column=0, sticky="e", pady=3)
        self.spin_quantite = tk.Spinbox(frame_form, from_=1, to=99, width=5)
        self.spin_quantite.grid(row=1, column=1, sticky="w", pady=3)

        tk.Label(frame_form, text="Durée :").grid(row=2, column=0, sticky="e", pady=3)
        self.combo_duree = ttk.Combobox(frame_form, values=list(DUREES), state="readonly")
        self.combo_duree.grid(row=2, column=1, sticky="ew", pady=3)

        # Radiobuttons : UNE StringVar partagée, une value différente par bouton
        tk.Label(frame_form, text="Forfait :").grid(row=3, column=0, sticky="ne", pady=3)
        self.var_forfait = tk.StringVar()
        for i, (forfait, prix) in enumerate(PRIX_FORFAITS.items()):
            tk.Radiobutton(frame_form, text=f"{forfait} ({prix} $)", variable=self.var_forfait,
                           value=forfait).grid(row=3 + i, column=1, sticky="w")

        # Checkbuttons : UNE BooleanVar par case → dictionnaire
        tk.Label(frame_form, text="Options :").grid(row=6, column=0, sticky="ne", pady=(10, 3))
        self.vars_options = {}
        for i, (option, prix) in enumerate(PRIX_OPTIONS.items()):
            self.vars_options[option] = tk.BooleanVar()
            tk.Checkbutton(frame_form, text=f"{option} (+{prix} $)", variable=self.vars_options[option]).grid(
                row=6 + i, column=1, sticky="w", pady=(10 if i == 0 else 0, 0))

        # ---------- Cadre résumé : titre (col 0) + valeur (col 1, collée à droite) ----------
        frame_resume = tk.LabelFrame(self, text="Résumé", padx=10, pady=10)
        frame_resume.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_resume.columnconfigure(1, weight=1)

        self.labels_resume = {}
        for i, titre in enumerate(["Client", "Forfait", "Options", "Sous-total", "Taxes", "TOTAL"]):
            tk.Label(frame_resume, text=f"{titre} :").grid(row=i, column=0, sticky="w", pady=2)
            self.labels_resume[titre] = tk.Label(frame_resume, text="-")
            self.labels_resume[titre].grid(row=i, column=1, sticky="e", pady=2)
        self.labels_resume["TOTAL"].config(font=("Arial", 12, "bold"))

        # ---------- Barre de boutons : 3 colonnes de même poids = 3 boutons de même largeur ----------
        frame_boutons = tk.Frame(self)
        frame_boutons.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        frame_boutons.columnconfigure((0, 1, 2), weight=1)
        tk.Button(frame_boutons, text="Calculer", command=self.calculer).grid(row=0, column=0, sticky="ew", padx=3)
        tk.Button(frame_boutons, text="Réinitialiser", command=self.reinitialiser).grid(row=0, column=1, sticky="ew", padx=3)
        tk.Button(frame_boutons, text="Quitter", command=self.destroy).grid(row=0, column=2, sticky="ew", padx=3)

        self.label_statut = tk.Label(self, text="", anchor="w")
        self.label_statut.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))

    def calculer(self):
        nom = self.entry_nom.get().strip()
        if not nom:
            messagebox.showerror("Erreur", "Le nom est obligatoire.")
            return
        try:
            quantite = int(self.spin_quantite.get())
        except ValueError:
            messagebox.showerror("Erreur", "La quantité doit être un entier.")
            return

        mois = DUREES[self.combo_duree.get()]
        prix_forfait = PRIX_FORFAITS[self.var_forfait.get()] * mois * quantite
        options = [opt for opt, var in self.vars_options.items() if var.get()]
        prix_options = sum(PRIX_OPTIONS[opt] for opt in options) * quantite
        sous_total = prix_forfait + prix_options
        taxes = sous_total * 0.14975
        total = sous_total + taxes

        self.labels_resume["Client"].config(text=nom)
        self.labels_resume["Forfait"].config(text=f"{self.var_forfait.get()} × {mois} mois")
        self.labels_resume["Options"].config(text=", ".join(options) or "aucune")
        self.labels_resume["Sous-total"].config(text=f"{sous_total:.2f} $")
        self.labels_resume["Taxes"].config(text=f"{taxes:.2f} $")
        self.labels_resume["TOTAL"].config(text=f"{total:.2f} $")
        self.label_statut.config(text=f"Calcul effectué pour {nom}")

    def reinitialiser(self):
        self.entry_nom.delete(0, tk.END)
        self.spin_quantite.delete(0, tk.END)
        self.spin_quantite.insert(0, "1")
        self.combo_duree.current(0)
        self.var_forfait.set("Base")
        for var in self.vars_options.values():
            var.set(False)
        for label in self.labels_resume.values():
            label.config(text="-")
        self.label_statut.config(text="")
        self.entry_nom.focus_set()


if __name__ == "__main__":
    Application().mainloop()
