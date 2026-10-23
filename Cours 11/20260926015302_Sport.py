import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Sport(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Centre sportif Active+")
        self.geometry("700x700")
        self.create_widget()

    def create_widget(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        # Titre
        tk.Label(self, text="CENTRE SPORTIF Gym+", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, sticky="ew")

        # Sous-titre
        tk.Label(self, text="INSCRIPTION À UNE ACTIVITÉ", font=("Arial", 10)).grid(row=1, column=0, columnspan=2, sticky="ew")

        # Le frame participant
        frame_participant = tk.LabelFrame(self, text="Participant")
        frame_participant.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        frame_participant.columnconfigure(1, weight=1)
        frame_participant.columnconfigure(3, weight=1)

        self.label_nom = tk.Label(frame_participant, text="Nom:")
        self.label_nom.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entree_nom = tk.Entry(frame_participant)
        self.entree_nom.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.label_prenom = tk.Label(frame_participant, text="Prénom:")
        self.label_prenom.grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.entree_prenom = tk.Entry(frame_participant)
        self.entree_prenom.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        self.label_age = tk.Label(frame_participant, text="Âge:")
        self.label_age.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entree_age = tk.Entry(frame_participant)
        self.entree_age.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.label_telephone = tk.Label(frame_participant, text="Téléphone:")
        self.label_telephone.grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.entree_telephone = tk.Entry(frame_participant)
        self.entree_telephone.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        self.label_niveau = tk.Label(frame_participant, text="Niveau:")
        self.label_niveau.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.type_niveau = tk.StringVar(self, value="Débutant")
        self.debutant = tk.Radiobutton(frame_participant, text="Débutant", variable=self.type_niveau, value="Débutant")
        self.debutant.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.intermediaire = tk.Radiobutton(frame_participant, text="Intermédiaire", variable=self.type_niveau, value="Intermédiaire")
        self.intermediaire.grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.avance = tk.Radiobutton(frame_participant, text="Avancé", variable=self.type_niveau, value="Avancé")
        self.avance.grid(row=2, column=3, sticky="e", padx=5, pady=5)

        # Le frame des activités
        frame_activite = tk.LabelFrame(self, text="Activité")
        frame_activite.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        frame_activite.columnconfigure(0, weight=1)
        frame_activite.columnconfigure(1, weight=1)

        self.type_activite = tk.StringVar(self, value="Natation")
        self.natation = tk.Radiobutton(frame_activite, text="Natation", variable=self.type_activite, value="Natation")
        self.natation.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Label(frame_activite, text="80 $").grid(row=0, column=1, sticky="e", padx=5, pady=5)
        self.tennis = tk.Radiobutton(frame_activite, text="Tennis", variable=self.type_activite, value="Tennis")
        self.tennis.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Label(frame_activite, text="100 $").grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.yoga = tk.Radiobutton(frame_activite, text="Yoga", variable=self.type_activite, value="Yoga")
        self.yoga.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Label(frame_activite, text="60 $").grid(row=2, column=1, sticky="e", padx=5, pady=5)

        # Le frame des formules
        frame_formule = tk.LabelFrame(self, text="Formule")
        frame_formule.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

        frame_formule.columnconfigure(0, weight=1)
        frame_formule.columnconfigure(1, weight=1)
        frame_formule.columnconfigure(2, weight=1)


        self.label_formule = tk.Label(frame_formule, text="Choisir une formule:")
        self.label_formule.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.formule_box = ttk.Combobox(frame_formule,values=["1 mois", "3 mois", "6 mois"], state="readonly")
        self.formule_box.grid(row=0, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        self.formule_box.current(0)

        self.label_1_mois = tk.Label(frame_formule, text="1 mois: + 0 $")
        self.label_1_mois.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.label_3_mois = tk.Label(frame_formule, text="3 mois: + 150 $")
        self.label_3_mois.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.label_6_mois = tk.Label(frame_formule, text="6 mois: + 250 $")
        self.label_6_mois.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        # Le frame d'options
        frame_options = tk.LabelFrame(self, text="Options")
        frame_options.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        frame_options.columnconfigure(0, weight=1)
        frame_options.columnconfigure(1, weight=1)

        self.var_access = tk.IntVar()
        self.access = tk.Checkbutton(frame_options, text="Accès illimité (+30 $)", variable=self.var_access)
        self.access.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.var_entraineur = tk.IntVar()
        self.entraineur = tk.Checkbutton(frame_options, text="Entraineur (+50 $)", variable=self.var_entraineur)
        self.entraineur.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.var_equipement = tk.IntVar()
        self.equipement = tk.Checkbutton(frame_options, text="Equipement (+20 $)", variable=self.var_equipement)
        self.equipement.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.var_casier = tk.IntVar()
        self.casier = tk.Checkbutton(frame_options, text="Casier (+15 $)", variable=self.var_casier)
        self.casier.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Le frame d'infos
        frame_infos = tk.LabelFrame(self, text="Informations sur l'activité")
        frame_infos.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

        frame_infos.columnconfigure(0, weight=1)
        frame_infos.columnconfigure(1, weight=1)

        self.label_activite = tk.Label(frame_infos, text="Activité choisie:")
        self.label_activite.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.affichage_activite = tk.Label(frame_infos, text="--")
        self.affichage_activite.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        self.label_niveau = tk.Label(frame_infos, text="Niveau:")
        self.label_niveau.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.affichage_niveau = tk.Label(frame_infos, text="--")
        self.affichage_niveau.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        self.label_duree = tk.Label(frame_infos, text="Durée:")
        self.label_duree.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.affichage_duree = tk.Label(frame_infos, text="--")
        self.affichage_duree.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        self.label_nb_options = tk.Label(frame_infos, text="Nombre d'options:")
        self.label_nb_options.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.affichage_nb_options = tk.Label(frame_infos, text="0")
        self.affichage_nb_options.grid(row=3, column=1, sticky="e", padx=5, pady=5)

        # Le frame de tarif
        frame_tarif = tk.LabelFrame(self, text="Tarification")
        frame_tarif.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)

        frame_tarif.columnconfigure(0, weight=1)
        frame_tarif.columnconfigure(1, weight=1)

        self.label_montant_activite = tk.Label(frame_tarif, text="Activité:")
        self.label_montant_activite.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.affichage_montant_activite = tk.Label(frame_tarif, text="0.00 $")
        self.affichage_montant_activite.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        self.label_formule = tk.Label(frame_tarif, text="Formule:")
        self.label_formule.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.affichage_formule = tk.Label(frame_tarif, text="0.00 $")
        self.affichage_formule.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        self.label_options = tk.Label(frame_tarif, text="Options:")
        self.label_options.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.affichage_options = tk.Label(frame_tarif, text="0.00 $")
        self.affichage_options.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        self.label_total = tk.Label(frame_tarif, text="TOTAL:", font=("Arial", 12, "bold"))
        self.label_total.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.affichage_total = tk.Label(frame_tarif, text="0.00 $", font=("Arial", 12, "bold"))
        self.affichage_total.grid(row=3, column=1, sticky="e", padx=5, pady=5)

        frame_buttons = tk.Frame(self)
        frame_buttons.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        frame_buttons.columnconfigure(0, weight=1)
        frame_buttons.columnconfigure(1, weight=1)
        frame_buttons.columnconfigure(2, weight=1)

        tk.Button(frame_buttons, text="CALCULER", command=self.calculer).grid(row=0, column=0, sticky="ew", padx=3, pady=5)
        tk.Button(frame_buttons, text="INSCRIRE", command=self.inscrire).grid(row=0, column=1, sticky="ew", padx=3, pady=5)
        tk.Button(frame_buttons, text="RÉINITIALISER", command=self.reinitialiser).grid(row=0, column=2, sticky="ew", padx=3,pady=5)

        self.label_statut = tk.Label(self, text="Statut : ", font=("Arial", 10, "bold"))
        self.label_statut.grid(row=7, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    def calculer(self):
        self.affichage_activite.config(text=f"{self.type_activite.get()}")
        self.affichage_niveau.config(text=f"{self.type_niveau.get()}")
        self.affichage_duree.config(text=f"{self.formule_box.get()}")
        self.affichage_nb_options.config(text=f"{self.var_access.get() + self.var_entraineur.get() + self.var_equipement.get() + self.var_casier.get()}")

        if self.type_activite.get() == "Natation":
            montant_activite = 80
        elif self.type_activite.get() == "Tennis":
            montant_activite = 100
        else:
            montant_activite = 60
        self.affichage_montant_activite.config(text=f"{montant_activite:.2f} $")

        if self.formule_box.get() == "1 mois":
            montant_formule = 0
        elif self.formule_box.get() == "3 mois":
            montant_formule = 150
        else:
            montant_formule = 250
        self.affichage_formule.config(text=f"{montant_formule:.2f} $")

        montant_options = 0
        montant_options += 30 * self.var_access.get()
        montant_options += 50 * self.var_entraineur.get()
        montant_options += 20 * self.var_equipement.get()
        montant_options += 15 * self.var_casier.get()
        self.affichage_options.config(text=f"{montant_options:.2f} $")

        self.affichage_total.config(text=f"{montant_activite + montant_options + montant_formule:.2f} $")

    def inscrire(self):
        if self.entree_nom.get() == "" or self.entree_prenom.get() == "" or self.entree_age.get() == "" or self.entree_telephone.get() == "":
            messagebox.showerror("Erreur", "Vous n'avez pas rempli toutes les infos du participant")
            return

        if not self.entree_age.get().isdigit():
            messagebox.showerror("Erreur", "L'âge doit être un nombre")
            return

        self.calculer()

        infos = (
            f"Nom : {self.entree_nom.get()}\n"
            f"Prénom : {self.entree_prenom.get()}\n"
            f"Âge : {self.entree_age.get()}\n"
            f"Téléphone : {self.entree_telephone.get()}\n"
            f"Niveau : {self.type_niveau.get()}\n"
            f"Activité : {self.type_activite.get()}\n"
            f"Formule : {self.formule_box.get()}\n"
            f"Nombre d'options : {self.affichage_nb_options.cget('text')}\n"
            f"Total : {self.affichage_total.cget('text')}")
        messagebox.showinfo("Inscription confirmée", infos)

        self.label_statut.config(
            text=f"Statut : {self.entree_prenom.get()} {self.entree_nom.get()} est inscrit(e) à {self.type_activite.get()}")
    def reinitialiser(self):
        self.entree_nom.delete(0, "end")
        self.entree_prenom.delete(0, "end")
        self.entree_age.delete(0, "end")
        self.entree_telephone.delete(0, "end")
        self.type_niveau.set("Débutant")

        self.type_activite.set("Natation")

        self.formule_box.current(0)

        self.var_access.set(False)
        self.var_entraineur.set(False)
        self.var_equipement.set(False)
        self.var_casier.set(False)

        self.affichage_activite.config(text="--")
        self.affichage_niveau.config(text="--")
        self.affichage_duree.config(text="--")
        self.affichage_nb_options.config(text="0")

        self.affichage_montant_activite.config(text="0.00 $")
        self.affichage_formule.config(text="0.00 $")
        self.affichage_options.config(text="0.00 $")
        self.affichage_total.config(text="0.00 $")

        self.label_statut.config(text="Statut : ")




if __name__ == "__main__":
    app = Sport()
    app.mainloop()


