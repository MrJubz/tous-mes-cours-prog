import tkinter as tk
from tkinter import messagebox

DUREE_MIN = 1
DUREE_MAX = 480


class ToDoValidation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de tâches")
        self.geometry("450x600")
        self.taches = []
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)

        tk.Label(self, text="Ma To-Do List", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # 1) Les StringVar + trace_add : à chaque modification, on réévalue l'état du bouton
        self.var_titre = tk.StringVar()
        self.var_duree = tk.StringVar()
        self.var_titre.trace_add("write", self.maj_bouton)
        self.var_duree.trace_add("write", self.maj_bouton)

        tk.Label(self, text="Taper la tâche à ajouter :").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self, textvariable=self.var_titre).grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # 2) Validation à la source : register + %P (valeur du champ APRÈS la frappe)
        vcmd = (self.register(self.valider_frappe_duree), "%P")
        invcmd = (self.register(self.frappe_refusee),)
        tk.Label(self, text="Durée estimée (minutes) :").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_duree = tk.Entry(self, textvariable=self.var_duree, validate="key",
                                    validatecommand=vcmd, invalidcommand=invcmd)
        self.entry_duree.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        self.couleur_normale = self.entry_duree.cget("background")

        self.prioritaire = tk.BooleanVar()
        tk.Checkbutton(self, text="Toutes les nouvelles tâches sont prioritaires",
                       variable=self.prioritaire).grid(row=3, column=0, columnspan=2, sticky="w", padx=10)

        tk.Label(self, text="Choisir le type de tâche :").grid(row=4, column=0, sticky="nw", padx=10, pady=5)
        self.type_tache = tk.StringVar(value="Personnel")
        cadre_radio = tk.Frame(self)
        cadre_radio.grid(row=4, column=1, sticky="w", padx=10)
        tk.Radiobutton(cadre_radio, text="Personnel", variable=self.type_tache, value="Personnel").grid(row=0, column=0, sticky="w")
        tk.Radiobutton(cadre_radio, text="Professionnel", variable=self.type_tache, value="Professionnel").grid(row=1, column=0, sticky="w")

        # 3) Bouton désactivé au départ
        self.btn_ajouter = tk.Button(self, text="Ajouter la tâche", command=self.ajouter_tache, state="disabled")
        self.btn_ajouter.grid(row=5, column=0, columnspan=2, pady=15)

        self.liste = tk.Listbox(self)
        self.liste.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))

    def valider_frappe_duree(self, nouvelle_valeur):
        if nouvelle_valeur == "":
            return True  # on doit pouvoir effacer le champ
        return nouvelle_valeur.isdigit() and DUREE_MIN <= int(nouvelle_valeur) <= DUREE_MAX

    def frappe_refusee(self):
        self.bell()  # retour discret : petit son + champ rouge 0,5 s
        self.entry_duree.config(background="#ffb3b3")
        self.after(500, lambda: self.entry_duree.config(background=self.couleur_normale))

    def formulaire_valide(self):
        titre = self.var_titre.get().strip()
        duree = self.var_duree.get()
        return bool(titre) and duree.isdigit() and DUREE_MIN <= int(duree) <= DUREE_MAX

    def maj_bouton(self, *args):
        # trace_add envoie 3 arguments (nom, index, mode) : *args les accepte sans s'en servir
        self.btn_ajouter.config(state="normal" if self.formulaire_valide() else "disabled")

    def ajouter_tache(self):
        if not self.formulaire_valide():  # double vérification côté logique
            messagebox.showerror("Saisie invalide", "Titre obligatoire et durée entre 1 et 480.")
            return
        tache = {"titre": self.var_titre.get().strip(), "duree": int(self.var_duree.get()),
                 "type": self.type_tache.get(), "prioritaire": self.prioritaire.get()}
        self.taches.append(tache)
        self.liste.insert(tk.END, self.formater(tache))
        self.var_titre.set("")
        self.var_duree.set("")

    def formater(self, tache):
        p = "[P]" if tache["prioritaire"] else ""
        t = "[Prof]" if tache["type"] == "Professionnel" else "[Pers]"
        return f"{p}{t}[{tache['duree']}] {tache['titre']}"


if __name__ == "__main__":
    ToDoValidation().mainloop()
