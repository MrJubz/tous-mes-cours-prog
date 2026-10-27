import tkinter as tk
from tkinter import ttk, messagebox

PRIX_ACTIVITES = {"Natation": 80, "Tennis": 100, "Yoga": 60}
PRIX_FORMULES = {"1 mois": 0, "3 mois": 150, "6 mois": 250}
PRIX_OPTIONS = {"Accès illimité": 30, "Équipement": 20, "Entraîneur personnel": 50, "Casier personnel": 15}
NIVEAUX = ["Débutant", "Intermédiaire", "Avancé"]


class CentreSportif(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Centre sportif Active+")
        self.geometry("680x640")
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        tk.Label(self, text="CENTRE SPORTIF Gym+", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2)
        tk.Label(self, text="INSCRIPTION À UNE ACTIVITÉ", font=("Arial", 11)).grid(row=1, column=0, columnspan=2, pady=(0, 5))

        # ---------- Participant ----------
        frame_part = tk.LabelFrame(self, text="Participant", padx=5, pady=5)
        frame_part.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        frame_part.columnconfigure((1, 3), weight=1)

        self.entries = {}
        champs = [("Nom", 0, 0), ("Prénom", 0, 2), ("Âge", 1, 0), ("Téléphone", 1, 2)]
        for nom, row, col in champs:
            tk.Label(frame_part, text=f"{nom} :").grid(row=row, column=col, sticky="e", padx=5, pady=3)
            self.entries[nom] = tk.Entry(frame_part)
            self.entries[nom].grid(row=row, column=col + 1, sticky="ew", padx=5, pady=3)

        tk.Label(frame_part, text="Niveau :").grid(row=2, column=0, sticky="e", padx=5)
        self.niveau = tk.StringVar(value=NIVEAUX[0])
        for i, niveau in enumerate(NIVEAUX):
            tk.Radiobutton(frame_part, text=niveau, variable=self.niveau, value=niveau).grid(row=2, column=1 + i, sticky="w")

        # ---------- Activité ----------
        frame_act = tk.LabelFrame(self, text="Activité", padx=5, pady=5)
        frame_act.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        frame_act.columnconfigure(1, weight=1)
        self.activite = tk.StringVar(value="Natation")
        for i, (activite, prix) in enumerate(PRIX_ACTIVITES.items()):
            tk.Radiobutton(frame_act, text=activite, variable=self.activite, value=activite).grid(row=i, column=0, sticky="w")
            tk.Label(frame_act, text=f"{prix} $").grid(row=i, column=1, sticky="e")

        # ---------- Formule ----------
        frame_form = tk.LabelFrame(self, text="Formule", padx=5, pady=5)
        frame_form.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        frame_form.columnconfigure((0, 1, 2), weight=1)
        tk.Label(frame_form, text="Choisir une formule :").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_formule = ttk.Combobox(frame_form, values=list(PRIX_FORMULES), state="readonly")
        self.combo_formule.grid(row=0, column=1, columnspan=2, sticky="ew")
        self.combo_formule.current(0)
        for i, (formule, prix) in enumerate(PRIX_FORMULES.items()):
            tk.Label(frame_form, text=f"{formule} : + {prix} $").grid(row=1, column=i)

        # ---------- Options ----------
        frame_opt = tk.LabelFrame(self, text="Options", padx=5, pady=5)
        frame_opt.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        frame_opt.columnconfigure((0, 1), weight=1)
        self.options = {}
        for i, (option, prix) in enumerate(PRIX_OPTIONS.items()):
            self.options[option] = tk.BooleanVar()
            # i // 2 = ligne, i % 2 = colonne → 2 colonnes automatiquement
            tk.Checkbutton(frame_opt, text=f"{option} (+{prix} $)", variable=self.options[option]).grid(
                row=i // 2, column=i % 2, sticky="w", padx=20)

        # ---------- Informations + Tarification ----------
        frame_info = tk.LabelFrame(self, text="Informations sur l'activité", padx=5, pady=5)
        frame_info.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        frame_info.columnconfigure(1, weight=1)
        self.infos = self.creer_lignes(frame_info, ["Activité choisie", "Niveau", "Durée", "Nombre d'options"])

        frame_tarif = tk.LabelFrame(self, text="Tarification", padx=5, pady=5)
        frame_tarif.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
        frame_tarif.columnconfigure(1, weight=1)
        self.tarifs = self.creer_lignes(frame_tarif, ["Activité", "Formule", "Options", "TOTAL"])
        self.tarifs["TOTAL"].config(font=("Arial", 12, "bold"))

        # ---------- Boutons + statut ----------
        frame_btn = tk.Frame(self)
        frame_btn.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        frame_btn.columnconfigure((0, 1, 2), weight=1)
        tk.Button(frame_btn, text="CALCULER", command=self.calculer).grid(row=0, column=0, sticky="ew", padx=3)
        tk.Button(frame_btn, text="INSCRIRE", command=self.inscrire).grid(row=0, column=1, sticky="ew", padx=3)
        tk.Button(frame_btn, text="RÉINITIALISER", command=self.reinitialiser).grid(row=0, column=2, sticky="ew", padx=3)

        self.label_statut = tk.Label(self, text="Statut :", font=("Arial", 10, "bold"))
        self.label_statut.grid(row=7, column=0, columnspan=2, sticky="w", padx=10)

        self.afficher_vide()

    def creer_lignes(self, parent, titres):
        """Crée 'Titre : valeur' sur plusieurs lignes et retourne {titre: label_valeur}."""
        valeurs = {}
        for i, titre in enumerate(titres):
            tk.Label(parent, text=f"{titre} :").grid(row=i, column=0, sticky="w", pady=2)
            valeurs[titre] = tk.Label(parent)
            valeurs[titre].grid(row=i, column=1, sticky="e", pady=2)
        return valeurs

    def calculer(self):
        prix_activite = PRIX_ACTIVITES[self.activite.get()]
        prix_formule = PRIX_FORMULES[self.combo_formule.get()]
        options_choisies = [opt for opt, var in self.options.items() if var.get()]
        prix_options = sum(PRIX_OPTIONS[opt] for opt in options_choisies)
        total = prix_activite + prix_formule + prix_options

        self.infos["Activité choisie"].config(text=self.activite.get())
        self.infos["Niveau"].config(text=self.niveau.get())
        self.infos["Durée"].config(text=self.combo_formule.get())
        self.infos["Nombre d'options"].config(text=str(len(options_choisies)))

        self.tarifs["Activité"].config(text=f"{prix_activite:.2f} $")
        self.tarifs["Formule"].config(text=f"{prix_formule:.2f} $")
        self.tarifs["Options"].config(text=f"{prix_options:.2f} $")
        self.tarifs["TOTAL"].config(text=f"{total:.2f} $")
        return total

    def inscrire(self):
        valeurs = {nom: entry.get().strip() for nom, entry in self.entries.items()}
        if not all(valeurs.values()):
            messagebox.showerror("Erreur", "Remplissez toutes les informations du participant.")
            return
        if not valeurs["Âge"].isdigit() or not 5 <= int(valeurs["Âge"]) <= 120:
            messagebox.showerror("Erreur", "L'âge doit être un nombre entre 5 et 120.")
            return

        total = self.calculer()
        resume = "\n".join(f"{nom} : {val}" for nom, val in valeurs.items())
        resume += (f"\nNiveau : {self.niveau.get()}\nActivité : {self.activite.get()}"
                   f"\nFormule : {self.combo_formule.get()}\nTotal : {total:.2f} $")
        messagebox.showinfo("Inscription confirmée", resume)
        self.label_statut.config(
            text=f"Statut : {valeurs['Prénom']} {valeurs['Nom']} est inscrit(e) à {self.activite.get()}")

    def afficher_vide(self):
        for label in self.infos.values():
            label.config(text="--")
        self.infos["Nombre d'options"].config(text="0")
        for label in self.tarifs.values():
            label.config(text="0.00 $")

    def reinitialiser(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.niveau.set(NIVEAUX[0])
        self.activite.set("Natation")
        self.combo_formule.current(0)
        for var in self.options.values():
            var.set(False)
        self.afficher_vide()
        self.label_statut.config(text="Statut :")


if __name__ == "__main__":
    CentreSportif().mainloop()
