import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json


class Produit:
    def __init__(self, nom, quantite, prix):
        self.nom = nom
        self.quantite = quantite
        self.prix = prix

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le nom du produit doit être une chaîne non vide.")
        self.__nom = valeur.strip()

    @property
    def quantite(self):
        return self.__quantite

    @quantite.setter
    def quantite(self, valeur):
        texte = str(valeur).strip()
        if not texte.isdigit():  # isdigit refuse aussi "-3" et "2.5"
            raise ValueError("La quantité doit être un entier positif (0 inclus).")
        self.__quantite = int(texte)

    @property
    def prix(self):
        return self.__prix

    @prix.setter
    def prix(self, valeur):
        try:
            valeur = float(valeur)
        except (ValueError, TypeError):
            raise ValueError("Le prix doit être un nombre.")
        if valeur < 0:
            raise ValueError("Le prix ne peut pas être négatif.")
        self.__prix = valeur

    def to_dict(self):
        return {"name": self.nom, "quantity": self.quantite, "price": self.prix}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["quantity"], d["price"])


class ProductManagerApp(tk.Tk):
    COLONNES = ("name", "quantity", "price")

    def __init__(self):
        super().__init__()
        self.title("Gestion des produits")
        self.produits = []
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # ---------- Ajouter ----------
        frame_ajout = tk.LabelFrame(self, text="Ajouter un produit", padx=10, pady=10)
        frame_ajout.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        frame_ajout.columnconfigure(1, weight=1)

        self.entries = {}
        for i, (cle, texte) in enumerate([("nom", "Produit :"), ("quantite", "Quantité :"), ("prix", "Prix :")]):
            tk.Label(frame_ajout, text=texte).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            self.entries[cle] = tk.Entry(frame_ajout)
            self.entries[cle].grid(row=i, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(frame_ajout, text="Ajouter Produit", command=self.ajouter_produit).grid(
            row=0, column=2, rowspan=3, sticky="ns", padx=10)

        # ---------- Gestion ----------
        frame_gestion = tk.LabelFrame(self, text="Gestion des produits", padx=10, pady=10)
        frame_gestion.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        frame_gestion.columnconfigure((0, 1, 2, 3), weight=1)

        tk.Button(frame_gestion, text="Supprimer Produit", command=self.supprimer_produit).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Button(frame_gestion, text="Modifier Produit", command=self.modifier_produit).grid(row=0, column=2, columnspan=2, pady=5)
        tk.Button(frame_gestion, text="Sauvegarder CSV", command=self.sauvegarder_csv).grid(row=1, column=0, padx=5)
        tk.Button(frame_gestion, text="Sauvegarder JSON", command=self.sauvegarder_json).grid(row=1, column=1, padx=5)
        tk.Button(frame_gestion, text="Importer CSV", command=self.importer_csv).grid(row=1, column=2, padx=5)
        tk.Button(frame_gestion, text="Importer JSON", command=self.importer_json).grid(row=1, column=3, padx=5)

        # ---------- Tableau ----------
        self.tree = ttk.Treeview(self, columns=self.COLONNES, show="headings", selectmode="browse")
        self.tree.heading("name", text="Produit")
        self.tree.heading("quantity", text="Quantité")
        self.tree.heading("price", text="Prix")
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        # Cliquer sur une ligne remplit les champs : on modifie puis on clique « Modifier Produit »
        self.tree.bind("<<TreeviewSelect>>", self.remplir_champs)

    # ---------- Outils ----------
    def lire_champs(self):
        return Produit(self.entries["nom"].get(), self.entries["quantite"].get(), self.entries["prix"].get())

    def vider_champs(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def index_selectionne(self):
        selection = self.tree.selection()
        return self.tree.index(selection[0]) if selection else None

    def rafraichir_tableau(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.produits:
            self.tree.insert("", "end", values=(p.nom, p.quantite, f"{p.prix:.2f}"))

    def remplir_champs(self, event=None):
        index = self.index_selectionne()
        if index is None:
            return
        p = self.produits[index]
        self.vider_champs()
        self.entries["nom"].insert(0, p.nom)
        self.entries["quantite"].insert(0, str(p.quantite))
        self.entries["prix"].insert(0, str(p.prix))

    # ---------- Actions ----------
    def ajouter_produit(self):
        try:
            produit = self.lire_champs()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.produits.append(produit)
        self.rafraichir_tableau()
        self.vider_champs()

    def supprimer_produit(self):
        index = self.index_selectionne()
        if index is None:
            messagebox.showwarning("Sélection obligatoire", "Choisissez un produit à supprimer.")
            return
        # Grâce à l'index, on supprime LE bon produit (même s'il existe un doublon identique)
        del self.produits[index]
        self.rafraichir_tableau()
        self.vider_champs()

    def modifier_produit(self):
        index = self.index_selectionne()
        if index is None:
            messagebox.showwarning("Sélection requise", "Choisissez un produit à modifier.")
            return
        try:
            self.produits[index] = self.lire_champs()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.rafraichir_tableau()
        self.vider_champs()

    # ---------- Fichiers ----------
    def sauvegarder_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.COLONNES)
            writer.writeheader()
            for p in self.produits:
                writer.writerow(p.to_dict())
        messagebox.showinfo("Sauvegarde", "Produits enregistrés en CSV.")

    def sauvegarder_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.produits], f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Sauvegarde", "Produits enregistrés en JSON.")

    def importer(self, lignes):
        nouveaux = []
        for ligne in lignes:
            nouveaux.append(Produit.from_dict(ligne))  # lève KeyError/ValueError si la ligne est mauvaise
        self.produits.extend(nouveaux)  # on ajoute seulement si TOUT le fichier est valide
        self.rafraichir_tableau()
        messagebox.showinfo("Importation", f"{len(nouveaux)} produit(s) importé(s).")

    def importer_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            with open(path, "r", newline="", encoding="utf-8") as f:
                self.importer(list(csv.DictReader(f)))
        except (OSError, KeyError, ValueError) as e:
            messagebox.showerror("Erreur", f"Import impossible : {e}")

    def importer_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Le fichier JSON doit contenir une liste d'objets.")
            self.importer(data)
        except (OSError, KeyError, ValueError, json.JSONDecodeError) as e:
            messagebox.showerror("Erreur", f"Import impossible : {e}")


if __name__ == "__main__":
    ProductManagerApp().mainloop()
