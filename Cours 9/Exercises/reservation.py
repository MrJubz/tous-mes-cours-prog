import tkinter as tk

class Reservation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reservation")
        self.geometry("500x500")

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)

        titre = tk.Label(self, text="Reservation d'hotel", bg="blue", fg="white", font=("Arial", 12), padx=5, pady=5)
        titre.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        frame_client = tk.LabelFrame(self, text="Info client", padx=5, pady=5)
        frame_client.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        frame_client.columnconfigure(1, weight=1)

        tk.Label(frame_client, text="Nom: ").grid(row=0, column=0, sticky="w")
        self.entry_nom = tk.Entry(frame_client)
        self.entry_nom.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame_client, text="Prenom: ").grid(row=1, column=0, sticky="w")
        self.entry_prenom = tk.Entry(frame_client)
        self.entry_prenom.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame_client, text="Telephone: ").grid(row=2, column=0, sticky="w")
        self.entry_telephone = tk.Entry(frame_client)
        self.entry_telephone.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame_client, text="type chambre: ").grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        self.type_chambre = tk.StringVar(value="Standard")
        tk.Radiobutton(frame_client, text="Standard - 120 $", variable=self.type_chambre, value="Standard").grid(row=4, column=0, sticky="w")
        tk.Radiobutton(frame_client, text="Double - 160 $", variable=self.type_chambre, value="Double").grid(row=5, column=0, sticky="w")
        tk.Radiobutton(frame_client, text="Suite - 250 $", variable=self.type_chambre, value="Suite").grid(row=6, column=0, sticky="w")

        tk.Label(frame_client, text="Nombre de nuit: ").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.entry_nuit = tk.Entry(frame_client)
        self.entry_nuit.grid(row=7, column=1, sticky="ew")

        frame_resume = tk.LabelFrame(self, text="Resume reservation", padx=10, pady=10)
        frame_resume.grid(row=1, column=1, sticky="nsew")

        self.label_chambre = tk.Label(frame_resume, text="Chambre: -")
        self.label_chambre.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.label_nb_nuits = tk.Label(frame_resume, text="Nombre de nuits: -")
        self.label_nb_nuits.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.label_prix = tk.Label(frame_resume, text="Prix/nuit: -")
        self.label_prix.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.label_sous_total = tk.Label(frame_resume, text="Sous-total: -")
        self.label_sous_total.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.label_taxes = tk.Label(frame_resume, text="Taxes: -")
        self.label_taxes.grid(row=4, column=0, sticky="w", padx=5, pady=(20, 5))

        self.label_total = tk.Label(frame_resume, text="TOTAL: -",font=("Arial", 15, "bold"))
        self.label_total.grid(row=4, column=0, sticky="w", padx=5, pady=(20, 5))

        frame_options = tk.LabelFrame(self, text="Options supp", padx=5, pady=10)
        frame_options.grid(row=2, column=0, columnspan=2, sticky="ew")
        frame_options.columnconfigure(1, weight=1)


        self.petit_dejeuner = tk.BooleanVar()
        self.stationnement = tk.BooleanVar()
        self.Lit_supp = tk.BooleanVar()

        tk.Checkbutton(frame_options, text="Petit déjeuner", variable=self.petit_dejeuner).grid(row=0, column=0, sticky="ew")
        tk.Checkbutton(frame_options, text="Stationnement", variable=self.stationnement).grid(row=0, column=1, sticky="ew")
        tk.Checkbutton(frame_options, text="Lit supplementaire", variable=self.Lit_supp).grid(row=0, column=2, sticky="ew")

        frame_boutons = tk.Frame(self)
        frame_boutons.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        frame_boutons.columnconfigure(0, weight=1)
        frame_boutons.columnconfigure(1, weight=1)
        frame_boutons.columnconfigure(2, weight=1)

        self.btn_calculer = tk.Button(frame_boutons, text="Calculer", command=self.calculer)
        self.btn_calculer.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_renitialiser = tk.Button(frame_boutons, text="Réinitialisation", command=self.renitialiser)
        self.btn_renitialiser.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.btn_quitter = tk.Button(frame_boutons, text="Quitter", command=self.destroy)
        self.btn_quitter.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

    def calculer(self):
        if self.entry_nuit.get() == "":
            return

        nuits = int(self.entry_nuit.get())
        chambre = self.type_chambre.get()

        if chambre == "Standard":
            prix = 120
        elif chambre == "Double":
            prix = 160
        else:
            prix = 250

        sous_total = prix * nuits

        if self.petit_dejeuner.get():
            sous_total += 15 * nuits
        if self.stationnement.get():
            sous_total += 20 * nuits
        if self.Lit_supp.get():
            sous_total += 30 * nuits

        taxe = round(sous_total * 0.14975, 2)
        total = round(sous_total + taxe, 2)

        self.label_nb_nuits.config(text="Nuits: " + str(nuits))
        self.label_chambre.config(text="Chambre: " + chambre)
        self.label_prix.config(text="Prix: " + str(prix) + "$")
        self.label_sous_total.config(text="Sous-total: " + str(sous_total) + "$")
        self.label_taxes.config(text="Taxes: " + str(taxe) + "$")
        self.label_total.config(text="Total: " + str(total) + "$")
        self.label_taxes.config(text="Taxes: " + str(taxe))





    def renitialiser(self):
        self.entry_nuit.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.entry_nom.delete(0, tk.END)
        self.entry_telephone.delete(0, tk.END)

        self.type_chambre.set("Standard")

        self.petit_dejeuner.set(False)
        self.stationnement.set(False)
        self.Lit_supp.set(False)

        self.label_nb_nuits.config(text="Nuits: -")
        self.label_chambre.config(text="Chambre: -")
        self.label_prix.config(text="Prix: -")
        self.label_sous_total.config(text="Sous-total: -")
        self.label_taxes.config(text="Taxes: -")
        self.label_total.config(text="Total: -")
        self.label_taxes.config(text="Taxes: -")









if __name__ == "__main__":
    app = Reservation()
    app.mainloop()