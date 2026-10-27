"""Gabarit : lire / écrire JSON et CSV + boîtes de dialogue fichiers.

Les 4 fonctions du haut se copient telles quelles ; la petite app du bas montre comment les brancher.
"""
import json
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

CHAMPS = ["nom", "email", "age"]


# ---------- JSON ----------
def sauver_json(chemin, lignes):
    """lignes = liste de dictionnaires."""
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(lignes, f, indent=4, ensure_ascii=False)  # sérialisation


def charger_json(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        data = json.load(f)                                  # désérialisation
    if not isinstance(data, list):
        raise ValueError("Le JSON doit contenir une liste [ {...}, {...} ].")
    return data
# En mémoire (chaînes) : json.dumps(obj) → str   |   json.loads(texte) → obj


# ---------- CSV ----------
def sauver_csv(chemin, lignes, champs=CHAMPS):
    # newline="" évite les lignes vides en trop sous Windows
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(lignes)


def charger_csv(chemin):
    with open(chemin, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))  # chaque ligne → dict ; ATTENTION : toutes les valeurs sont du texte
# Version « listes » : csv.writer(f).writerow(["a", "b"])  et  for ligne in csv.reader(f): ...
# CSV français avec point-virgule : csv.DictReader(f, delimiter=";")


class AppFichiers(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON / CSV")
        self.geometry("520x320")
        self.lignes = [{"nom": "Alice", "email": "alice@x.ca", "age": 20},
                       {"nom": "Éloïse", "email": "elo@x.ca", "age": 31}]
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=CHAMPS, show="headings")
        for champ in CHAMPS:
            self.tree.heading(champ, text=champ.capitalize())
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        barre = tk.Frame(self)
        barre.grid(row=1, column=0, pady=(0, 10))
        for i, (texte, cmd) in enumerate([("Importer JSON", self.importer_json), ("Importer CSV", self.importer_csv),
                                          ("Exporter JSON", self.exporter_json), ("Exporter CSV", self.exporter_csv)]):
            tk.Button(barre, text=texte, command=cmd).grid(row=0, column=i, padx=4)
        self.rafraichir()

    def rafraichir(self):
        self.tree.delete(*self.tree.get_children())
        for ligne in self.lignes:
            self.tree.insert("", "end", values=[ligne.get(c, "") for c in CHAMPS])

    def importer_json(self):
        chemin = filedialog.askopenfilename(title="Ouvrir", filetypes=[("JSON", "*.json"), ("Tous", "*.*")])
        if not chemin:  # l'utilisateur a cliqué Annuler
            return
        try:
            self.lignes = charger_json(chemin)
            self.rafraichir()
        except (OSError, json.JSONDecodeError, ValueError) as e:
            messagebox.showerror("Erreur", str(e))

    def importer_csv(self):
        chemin = filedialog.askopenfilename(title="Ouvrir", filetypes=[("CSV", "*.csv")])
        if not chemin:
            return
        try:
            self.lignes = charger_csv(chemin)
            self.rafraichir()
        except (OSError, csv.Error) as e:
            messagebox.showerror("Erreur", str(e))

    def exporter_json(self):
        chemin = filedialog.asksaveasfilename(title="Enregistrer", defaultextension=".json",
                                              filetypes=[("JSON", "*.json")], initialfile="donnees.json")
        if chemin:
            sauver_json(chemin, self.lignes)
            messagebox.showinfo("Export", f"{len(self.lignes)} ligne(s) enregistrée(s).")

    def exporter_csv(self):
        chemin = filedialog.asksaveasfilename(title="Enregistrer", defaultextension=".csv",
                                              filetypes=[("CSV", "*.csv")], initialfile="donnees.csv")
        if chemin:
            sauver_csv(chemin, self.lignes)
            messagebox.showinfo("Export", f"{len(self.lignes)} ligne(s) enregistrée(s).")


if __name__ == "__main__":
    AppFichiers().mainloop()
