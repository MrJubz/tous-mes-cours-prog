import tkinter as tk
from tkinter import messagebox

PRIX_CHAMBRES = {"Standard": 120, "Double": 160, "Suite": 250}
PRIX_OPTIONS = {"Petit-déjeuner": 15, "Stationnement": 20, "Lit supplémentaire": 30}
TAUX_TAXES = 0.14975


class ReservationHotel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Réservation d'hôtel")
        self.geometry("620x480")
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        tk.Label(self, text="RÉSERVATION D'HÔTEL", bg="blue", fg="white",
                 font=("Arial", 16, "bold"), pady=8).grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # ---------- Informations du client ----------
        frame_client = tk.LabelFrame(self, text="Informations du client", padx=8, pady=8)
        frame_client.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_client.columnconfigure(1, weight=1)

        tk.Label(frame_client, text="Nom :").grid(row=0, column=0, sticky="w")
        self.entry_nom = tk.Entry(frame_client)
        self.entry_nom.grid(row=0, column=1, sticky="ew", pady=3)

        tk.Label(frame_client, text="Prénom :").grid(row=1, column=0, sticky="w")
        self.entry_prenom = tk.Entry(frame_client)
        self.entry_prenom.grid(row=1, column=1, sticky="ew", pady=3)

        tk.Label(frame_client, text="Téléphone :").grid(row=2, column=0, sticky="w")
        self.entry_telephone = tk.Entry(frame_client)
        self.entry_telephone.grid(row=2, column=1, sticky="ew", pady=3)

        tk.Label(frame_client, text="Type de chambre :").grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.type_chambre = tk.StringVar(value="Standard")
        for i, (chambre, prix) in enumerate(PRIX_CHAMBRES.items()):
            tk.Radiobutton(frame_client, text=f"{chambre} - {prix} $", variable=self.type_chambre,
                           value=chambre).grid(row=4 + i, column=0, columnspan=2, sticky="w")

        tk.Label(frame_client, text="Nombre de nuits :").grid(row=7, column=0, sticky="w", pady=(10, 0))
        self.entry_nuits = tk.Entry(frame_client)
        self.entry_nuits.grid(row=7, column=1, sticky="ew", pady=(10, 0))

        # ---------- Résumé (chaque label a SA ligne : row 0 à 5) ----------
        frame_resume = tk.LabelFrame(self, text="Résumé de la réservation", padx=8, pady=8)
        frame_resume.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.label_chambre = tk.Label(frame_resume)
        self.label_chambre.grid(row=0, column=0, sticky="w", pady=3)
        self.label_nuits = tk.Label(frame_resume)
        self.label_nuits.grid(row=1, column=0, sticky="w", pady=3)
        self.label_prix = tk.Label(frame_resume)
        self.label_prix.grid(row=2, column=0, sticky="w", pady=3)
        self.label_sous_total = tk.Label(frame_resume)
        self.label_sous_total.grid(row=3, column=0, sticky="w", pady=(15, 3))
        self.label_taxes = tk.Label(frame_resume)
        self.label_taxes.grid(row=4, column=0, sticky="w", pady=3)
        self.label_total = tk.Label(frame_resume, font=("Arial", 14, "bold"))
        self.label_total.grid(row=5, column=0, sticky="w", pady=(15, 3))

        # ---------- Options ----------
        frame_options = tk.LabelFrame(self, text="Options supplémentaires", padx=8, pady=5)
        frame_options.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        frame_options.columnconfigure((0, 1, 2), weight=1)

        self.options = {}
        for i, option in enumerate(PRIX_OPTIONS):
            self.options[option] = tk.BooleanVar()
            tk.Checkbutton(frame_options, text=option, variable=self.options[option]).grid(row=0, column=i)

        # ---------- Boutons ----------
        frame_boutons = tk.Frame(self)
        frame_boutons.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        frame_boutons.columnconfigure((0, 1, 2), weight=1)
        tk.Button(frame_boutons, text="Calculer", command=self.calculer).grid(row=0, column=0, sticky="ew", padx=3)
        tk.Button(frame_boutons, text="Réinitialiser", command=self.reinitialiser).grid(row=0, column=1, sticky="ew", padx=3)
        tk.Button(frame_boutons, text="Quitter", command=self.destroy).grid(row=0, column=2, sticky="ew", padx=3)

        self.afficher_resume_vide()

    def calculer(self):
        if not self.entry_nom.get().strip() or not self.entry_prenom.get().strip():
            messagebox.showerror("Erreur", "Le nom et le prénom sont obligatoires.")
            return
        try:
            nuits = int(self.entry_nuits.get())
            if nuits <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre de nuits doit être un entier positif.")
            return

        chambre = self.type_chambre.get()
        prix_nuit = PRIX_CHAMBRES[chambre]
        sous_total = prix_nuit * nuits
        for option, var in self.options.items():
            if var.get():
                sous_total += PRIX_OPTIONS[option] * nuits

        taxes = round(sous_total * TAUX_TAXES, 2)
        total = round(sous_total + taxes, 2)

        self.label_chambre.config(text=f"Chambre : {chambre}")
        self.label_nuits.config(text=f"Nombre de nuits : {nuits}")
        self.label_prix.config(text=f"Prix/nuit : {prix_nuit} $")
        self.label_sous_total.config(text=f"Sous-total : {sous_total} $")
        self.label_taxes.config(text=f"Taxes : {taxes} $")
        self.label_total.config(text=f"TOTAL : {total} $")

    def afficher_resume_vide(self):
        self.label_chambre.config(text="Chambre : -")
        self.label_nuits.config(text="Nombre de nuits : -")
        self.label_prix.config(text="Prix/nuit : -")
        self.label_sous_total.config(text="Sous-total : -")
        self.label_taxes.config(text="Taxes : -")
        self.label_total.config(text="TOTAL : -")

    def reinitialiser(self):
        for entry in (self.entry_nom, self.entry_prenom, self.entry_telephone, self.entry_nuits):
            entry.delete(0, tk.END)
        self.type_chambre.set("Standard")
        for var in self.options.values():
            var.set(False)
        self.afficher_resume_vide()


if __name__ == "__main__":
    ReservationHotel().mainloop()
