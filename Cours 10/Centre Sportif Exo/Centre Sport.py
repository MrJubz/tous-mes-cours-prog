import tkinter as tk
from tkinter import ttk

class Reservation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Réservation d'hotel")
        self.geometry("600x700")

        self.creer_widget()

    def creer_widget(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        titre = tk.Label(self, text="CENTRE SPORTIF Gym+", font=("Arial", 18, "bold"), padx=5, pady=5)
        titre.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 0))
        sous_titre = tk.Label(self, text="INSCRIPTION À UNE ACTIVITÉ", font=("Arial", 11), padx=5, pady=5)
        sous_titre.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 5))

        frame_participant=tk.LabelFrame(self,text="Participant",padx=5,pady=5)
        frame_participant.grid(row=2, column=0, sticky="nsew",columnspan=2,padx=5,pady=5)
        frame_participant.columnconfigure(0, weight=1)
        frame_participant.columnconfigure(1, weight=1)
        frame_participant.columnconfigure(2, weight=1)
        frame_participant.columnconfigure(3, weight=1)
        frame_participant.rowconfigure(0, weight=1)
        frame_participant.rowconfigure(1, weight=1)
        frame_participant.rowconfigure(2, weight=1)


        tk.Label(frame_participant, text="Nom: ").grid(row=0, column=0, sticky="e")
        self.entry_nom = tk.Entry(frame_participant)
        self.entry_nom.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame_participant, text="Prenom: ").grid(row=0, column=2, sticky="e")
        self.entry_prenom = tk.Entry(frame_participant)
        self.entry_prenom.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        tk.Label(frame_participant, text="Âge: ").grid(row=1, column=0, sticky="e")
        self.entry_age = tk.Entry(frame_participant)
        self.entry_age.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame_participant, text="Telephone: ").grid(row=1, column=2, sticky="e")
        self.entry_telephone = tk.Entry(frame_participant)
        self.entry_telephone.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        tk.Label(frame_participant, text="Niveau: ").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.niveau = tk.StringVar(value="Débutant")
        tk.Radiobutton(frame_participant, text="Débutant", variable=self.niveau, value="Débutant").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(frame_participant, text="Intermédiaire", variable=self.niveau, value="Intermédiaire").grid(row=2, column=2, sticky="w")
        tk.Radiobutton(frame_participant, text="Avancé", variable=self.niveau, value="Avancé").grid(row=2, column=3, sticky="e")



        frame_activite=tk.LabelFrame(self,text="Activité",padx=5,pady=5)
        frame_activite.grid(row=3, column=0, sticky="nsew",padx=5,pady=5)
        frame_activite.columnconfigure(0, weight=1)
        frame_activite.columnconfigure(1, weight=1)
        frame_activite.rowconfigure(0, weight=1)
        frame_activite.rowconfigure(1, weight=1)
        frame_activite.rowconfigure(2, weight=1)

        self.activite= tk.StringVar(value="Natation")

        tk.Radiobutton(frame_activite, text="Natation", variable= self.niveau, value="Natation").grid(row=0,column=0,sticky="w",padx=5,pady=5)
        tk.Radiobutton(frame_activite, text="Tennis", variable=self.niveau, value="Tennis").grid(row=1,column=0,sticky="w",padx=5,pady=5)
        tk.Radiobutton(frame_activite, text="Yoga", variable=self.niveau, value="Yoga").grid(row=2,column=0,sticky="w",padx=5,pady=5)
        tk.Label(frame_activite,text="80$").grid(row=0,column=1, sticky="e")
        tk.Label(frame_activite,text="100$").grid(row=1,column=1, sticky="e")
        tk.Label(frame_activite,text="60$").grid(row=2,column=1, sticky="e")


        frame_formule=tk.LabelFrame(self,text="formule",padx=5,pady=5)
        frame_formule.grid(row=3, column=1, sticky="nsew",padx=3,pady=5)
        frame_formule.columnconfigure(0, weight=1)
        frame_formule.columnconfigure(1, weight=1)
        frame_formule.columnconfigure(2, weight=1)
        frame_formule.rowconfigure(0, weight=1)
        frame_formule.rowconfigure(1, weight=1)

        tk.Label(frame_formule,text="Choisir une formule:").grid(row=0,column=0, sticky="w")
        tk.Label(frame_formule,text="1 mois: +0$").grid(row=1,column=0, sticky="w")
        tk.Label(frame_formule,text="3 mois: +150$").grid(row=1,column=1, sticky="w")
        tk.Label(frame_formule,text="6 mois: +250$").grid(row=1,column=2, sticky="w")

        self.combo= ttk.Combobox(frame_formule,values= ["1 mois", "3 mois", "6 mois"] , state="readonly")
        self.combo.grid(row=0, column =1, sticky="w")

        frame_options=tk.LabelFrame(self,text="Options",padx=5,pady=5)
        frame_options.grid(row=4, column=0, sticky="nsew",columnspan=2,padx=3,pady=5)
        frame_options.columnconfigure(0, weight=1)
        frame_options.columnconfigure(1, weight=1)
        frame_options.columnconfigure(2, weight=1)
        frame_options.rowconfigure(0, weight=1)
        frame_options.rowconfigure(1, weight=1)
        frame_options.rowconfigure(2, weight=1)

        self.acces_illimite = tk.BooleanVar()
        self.equipement = tk.BooleanVar()
        self.entraineur = tk.BooleanVar()
        self.casier=tk.BooleanVar()

        tk.Checkbutton(frame_options, text="Accès illimité (+30$)", variable=self.acces_illimite).grid(row=0, column=0,sticky="w", padx=5,pady=5)
        tk.Checkbutton(frame_options, text="Équipement (+20$)", variable=self.equipement).grid(row=1, column=0,sticky="w", padx=5,pady=5)
        tk.Checkbutton(frame_options, text="Entraîneur personnel (+50$)", variable=self.entraineur).grid(row=0, column=1, sticky="w", padx=20,pady=5)
        tk.Checkbutton(frame_options, text="Casier personnel (+15$)", variable=self.casier).grid(row=1, column=1, sticky="w", padx=20,pady=5)

        frame_info=tk.LabelFrame(self,text="Informations sur l'activité",padx=5,pady=5)
        frame_info.grid(row=5, column=0, sticky="nsew",padx=3,pady=5)
        frame_info.columnconfigure(5, weight=1)

        tk.Label(frame_info, text="Activité choisie:").grid(row=0, column=0, sticky="w")
        tk.Label(frame_info, text="Niveau:").grid(row=1, column=0, sticky="w")
        tk.Label(frame_info, text="Durée").grid(row=2, column=0, sticky="w")
        tk.Label(frame_info, text="Nombre d'options").grid(row=3, column=0, sticky="w")

        tk.Label(frame_info, text="--").grid(row=0, column=1, sticky="e")
        tk.Label(frame_info, text="--").grid(row=1, column=1, sticky="e")
        tk.Label(frame_info, text="--").grid(row=2, column=1, sticky="e")
        tk.Label(frame_info, text="0").grid(row=3, column=1, sticky="e")

        frame_tarifs = tk.LabelFrame(self, text="Tarification", padx=5, pady=5)
        frame_tarifs.grid(row=5, column=1, sticky="nsew", columnspan=2, padx=3, pady=5)
        frame_tarifs.columnconfigure(4, weight=1)

        tk.Label(frame_tarifs, text="Activité:").grid(row=0, column=0, sticky="w")
        tk.Label(frame_tarifs, text="Formule:").grid(row=1, column=0, sticky="w")
        tk.Label(frame_tarifs, text="Options").grid(row=2, column=0, sticky="w")
        tk.Label(frame_tarifs, text="TOTAL:").grid(row=3, column=0, sticky="w")

        tk.Label(frame_tarifs, text="0.00 $").grid(row=0, column=1, sticky="e")
        tk.Label(frame_tarifs, text="0.00 $").grid(row=1, column=1, sticky="e")
        tk.Label(frame_tarifs, text="0.00 $").grid(row=2, column=1, sticky="e")
        tk.Label(frame_tarifs, text="0.00 $").grid(row=3, column=1, sticky="e")

        frame_boutons = tk.Frame(self)
        frame_boutons.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        frame_boutons.columnconfigure(0, weight=1)
        frame_boutons.columnconfigure(1, weight=1)
        frame_boutons.columnconfigure(2, weight=1)

        self.btn_calculer = tk.Button(frame_boutons, text="Calculer", command=self.calculer)
        self.btn_calculer.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_inscrire = tk.Button(frame_boutons, text="Inscrire", command=self.inscrire)
        self.btn_inscrire.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.btn_renitialiser = tk.Button(frame_boutons, text="Réinitialisation", command=self.renitialiser)
        self.btn_renitialiser.grid(row=0, column=1, sticky="ew", padx=5, pady=5)


    def calculer(self):
        pass

    def inscrire(self):
        pass

    def renitialiser(self):
        pass


if __name__ == "__main__":
    Reservation().mainloop()
