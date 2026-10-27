import tkinter as tk
from tkinter import messagebox
import random


class Compte:
    def __init__(self, numero, detenteur):
        self.__numero = numero
        self.detenteur = detenteur
        self.__solde = 0.0

    @property
    def numero(self):
        return self.__numero

    @property
    def detenteur(self):
        return self.__detenteur

    @detenteur.setter
    def detenteur(self, valeur):
        if not valeur.strip():
            raise ValueError("Le détenteur ne peut pas être vide.")
        self.__detenteur = valeur.strip()

    @property
    def solde(self):
        return self.__solde

    def deposer(self, montant):
        if montant <= 0:
            raise ValueError("Le montant doit être positif.")
        self.__solde += montant

    def retirer(self, montant):
        if montant <= 0:
            raise ValueError("Le montant doit être positif.")
        if montant > self.__solde:
            raise ValueError("Solde insuffisant.")
        self.__solde -= montant


class SimulateurCompte(tk.Tk):
    PLAGES = {"0 à 1": (0.01, 1, 0.01), "1 à 10": (1, 10, 0.5),
              "10 à 100": (10, 100, 5), "100 à 1000": (100, 1000, 50)}

    def __init__(self):
        super().__init__()
        self.title("Simulateur de Compte")
        self.geometry("750x450")
        self.compte = Compte(f"{random.randint(10000, 99999)}", "Client")
        self.create_widgets()
        self.rafraichir()

    def create_widgets(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        cadre_compte = tk.LabelFrame(self, text="Données du compte", padx=10, pady=5)
        cadre_compte.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        cadre_compte.columnconfigure(1, weight=1)

        self.var_numero = tk.StringVar()
        self.var_detenteur = tk.StringVar(value=self.compte.detenteur)
        self.var_solde = tk.StringVar()

        tk.Label(cadre_compte, text="Numéro :").grid(row=0, column=0, sticky="e")
        tk.Entry(cadre_compte, textvariable=self.var_numero, state="readonly").grid(row=0, column=1, sticky="ew", pady=2)
        tk.Label(cadre_compte, text="Détenteur :").grid(row=1, column=0, sticky="e")
        entry_detenteur = tk.Entry(cadre_compte, textvariable=self.var_detenteur)
        entry_detenteur.grid(row=1, column=1, sticky="ew", pady=2)
        entry_detenteur.bind("<FocusOut>", self.changer_detenteur)
        tk.Label(cadre_compte, text="Solde :").grid(row=2, column=0, sticky="e")
        tk.Entry(cadre_compte, textvariable=self.var_solde, state="readonly").grid(row=2, column=1, sticky="ew", pady=2)

        self.gele = tk.BooleanVar(value=False)
        tk.Checkbutton(cadre_compte, text="Gelé", variable=self.gele,
                       command=self.maj_etat_boutons).grid(row=0, column=2, padx=10)

        cadre_montant = tk.LabelFrame(self, text="Montant", padx=10, pady=5)
        cadre_montant.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        cadre_montant.columnconfigure(0, weight=1)

        self.spin_montant = tk.Spinbox(cadre_montant, from_=0.01, to=1, increment=0.01, justify="right")
        self.spin_montant.grid(row=0, column=0, rowspan=4, sticky="ew", padx=(0, 10))

        self.plage = tk.StringVar(value="0 à 1")
        for i, nom in enumerate(self.PLAGES):
            tk.Radiobutton(cadre_montant, text=nom, variable=self.plage, value=nom,
                           command=self.changer_plage).grid(row=i, column=1, sticky="w")

        barre = tk.Frame(self)
        barre.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)
        barre.columnconfigure((0, 1, 2, 3), weight=1)
        self.btn_deposer = tk.Button(barre, text="Déposer", command=self.deposer)
        self.btn_deposer.grid(row=0, column=0, sticky="ew", padx=3)
        self.btn_retirer = tk.Button(barre, text="Retirer", command=self.retirer)
        self.btn_retirer.grid(row=0, column=1, sticky="ew", padx=3)
        tk.Button(barre, text="Vider", command=lambda: self.journal.delete("1.0", "end")).grid(row=0, column=2, sticky="ew", padx=3)
        tk.Button(barre, text="Reset", command=self.reset).grid(row=0, column=3, sticky="ew", padx=3)

        cadre_journal = tk.Frame(self)
        cadre_journal.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        cadre_journal.columnconfigure(0, weight=1)
        cadre_journal.rowconfigure(0, weight=1)
        self.journal = tk.Text(cadre_journal, wrap="word")
        self.journal.grid(row=0, column=0, sticky="nsew")
        # Scrollbar : les deux lignes vont toujours ensemble (scroll -> texte et texte -> scroll)
        scroll = tk.Scrollbar(cadre_journal, command=self.journal.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.journal.config(yscrollcommand=scroll.set)

    def lire_montant(self):
        try:
            return float(self.spin_montant.get())
        except ValueError:
            raise ValueError("Le montant doit être un nombre.")

    def deposer(self):
        try:
            montant = self.lire_montant()
            self.compte.deposer(montant)
        except ValueError as e:
            messagebox.showerror("Dépôt refusé", str(e))
            return
        self.ecrire(f"Dépôt de {montant:.2f} $")
        self.rafraichir()

    def retirer(self):
        try:
            montant = self.lire_montant()
            self.compte.retirer(montant)
        except ValueError as e:
            messagebox.showerror("Retrait refusé", str(e))
            return
        self.ecrire(f"Retrait de {montant:.2f} $")
        self.rafraichir()

    def changer_detenteur(self, event=None):
        try:
            self.compte.detenteur = self.var_detenteur.get()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            self.var_detenteur.set(self.compte.detenteur)

    def changer_plage(self):
        mini, maxi, pas = self.PLAGES[self.plage.get()]
        self.spin_montant.config(from_=mini, to=maxi, increment=pas)
        self.spin_montant.delete(0, "end")
        self.spin_montant.insert(0, mini)

    def maj_etat_boutons(self):
        etat = "disabled" if self.gele.get() else "normal"
        self.btn_deposer.config(state=etat)
        self.btn_retirer.config(state=etat)
        self.ecrire("Compte gelé" if self.gele.get() else "Compte dégelé")

    def reset(self):
        self.compte = Compte(self.compte.numero, self.compte.detenteur)
        self.gele.set(False)
        self.maj_etat_boutons()
        self.journal.delete("1.0", "end")
        self.rafraichir()

    def ecrire(self, message):
        self.journal.insert("end", message + "\n")
        self.journal.see("end")

    def rafraichir(self):
        self.var_numero.set(self.compte.numero)
        self.var_solde.set(f"{self.compte.solde:.2f} $")
        self.title(f"Simulateur de Compte --- {self.compte.detenteur}")


if __name__ == "__main__":
    SimulateurCompte().mainloop()
