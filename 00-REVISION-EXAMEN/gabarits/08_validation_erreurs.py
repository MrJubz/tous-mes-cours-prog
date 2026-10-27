"""Gabarit : les 4 niveaux de validation vus au cours 12.

1. Validation à la frappe (validatecommand + %P)     → bloque les caractères interdits
2. Retour visuel (invalidcommand + bell + couleur)    → l'utilisateur voit le refus
3. Bouton désactivé tant que le formulaire est faux   → StringVar.trace_add
4. Validation finale au clic (try / except / else / finally) + règles métier séparées
"""
import tkinter as tk
from tkinter import messagebox


# ---------- Règles métier : AUCUN tkinter ici (testable seul) ----------
class ErreurSaisie(ValueError):
    """Exception personnalisée : hérite de ValueError, donc un except ValueError l'attrape aussi."""


def valider_commande(nom, quantite_txt, prix_txt):
    if not nom.strip():
        raise ErreurSaisie("Le nom est obligatoire.")
    try:
        quantite = int(quantite_txt)
        prix = float(prix_txt)
    except ValueError:
        raise ErreurSaisie("Quantité entière et prix numérique attendus.")
    if not 1 <= quantite <= 100:
        raise ErreurSaisie("La quantité doit être entre 1 et 100.")
    if prix <= 0:
        raise ErreurSaisie("Le prix doit être positif.")
    return nom.strip(), quantite, prix


class FormulaireValide(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Validation de saisie")
        self.geometry("420x260")
        self.columnconfigure(1, weight=1)

        self.var_nom = tk.StringVar()
        self.var_quantite = tk.StringVar()
        self.var_prix = tk.StringVar()
        # 3) À chaque écriture dans une variable → on recalcule l'état du bouton
        for var in (self.var_nom, self.var_quantite, self.var_prix):
            var.trace_add("write", self.maj_bouton)

        # 1) register transforme la méthode en commande Tcl ; %P = valeur APRÈS la frappe
        vcmd_entier = (self.register(self.frappe_entier), "%P")
        vcmd_decimal = (self.register(self.frappe_decimal), "%P")
        invcmd = (self.register(self.frappe_refusee), "%W")  # %W = nom du widget concerné

        tk.Label(self, text="Nom :").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(self, textvariable=self.var_nom).grid(row=0, column=1, sticky="ew", padx=10)

        tk.Label(self, text="Quantité (1-100) :").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(self, textvariable=self.var_quantite, validate="key",
                 validatecommand=vcmd_entier, invalidcommand=invcmd).grid(row=1, column=1, sticky="ew", padx=10)

        tk.Label(self, text="Prix :").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(self, textvariable=self.var_prix, validate="key",
                 validatecommand=vcmd_decimal, invalidcommand=invcmd).grid(row=2, column=1, sticky="ew", padx=10)

        self.btn = tk.Button(self, text="Commander", state="disabled", command=self.commander)
        self.btn.grid(row=3, column=0, columnspan=2, pady=15)

        self.label_info = tk.Label(self, text="", fg="gray")
        self.label_info.grid(row=4, column=0, columnspan=2)

    # ---------- 1) Validation à la frappe : retourner True (accepté) ou False (refusé) ----------
    def frappe_entier(self, valeur):
        return valeur == "" or (valeur.isdigit() and int(valeur) <= 100)

    def frappe_decimal(self, valeur):
        if valeur == "":
            return True
        try:
            float(valeur)
            return True
        except ValueError:
            return False

    # ---------- 2) Retour quand une frappe est refusée ----------
    def frappe_refusee(self, nom_widget):
        widget = self.nametowidget(nom_widget)
        self.bell()
        widget.config(highlightthickness=2, highlightbackground="red", highlightcolor="red")
        self.after(600, lambda: widget.config(highlightthickness=0))

    # ---------- 3) Bouton actif seulement si tout est valide ----------
    def maj_bouton(self, *args):
        try:
            valider_commande(self.var_nom.get(), self.var_quantite.get(), self.var_prix.get())
            self.btn.config(state="normal")
            self.label_info.config(text="")
        except ErreurSaisie as e:
            self.btn.config(state="disabled")
            self.label_info.config(text=str(e))

    # ---------- 4) Validation finale + try / except / else / finally ----------
    def commander(self):
        try:
            nom, quantite, prix = valider_commande(self.var_nom.get(), self.var_quantite.get(), self.var_prix.get())
        except ErreurSaisie as e:
            messagebox.showerror("Saisie invalide", str(e))
        else:  # seulement si AUCUNE exception
            messagebox.showinfo("OK", f"{nom} : {quantite} × {prix:.2f} $ = {quantite * prix:.2f} $")
            self.var_nom.set("")
            self.var_quantite.set("")
            self.var_prix.set("")
        finally:  # toujours exécuté (succès ou échec)
            print("Tentative de commande terminée")


if __name__ == "__main__":
    FormulaireValide().mainloop()
