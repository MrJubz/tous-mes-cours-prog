"""Gabarit : tous les widgets du cours et leurs méthodes get / insert / delete / config.

Lancer le fichier puis cliquer sur les boutons : chaque méthode montre UNE opération.
"""
import tkinter as tk
from tkinter import ttk, messagebox


class DemoWidgets(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Widgets et méthodes")
        self.geometry("760x560")
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.creer_entry_et_variables(row=0, column=0)
        self.creer_text(row=0, column=1)
        self.creer_listbox(row=1, column=0)
        self.creer_treeview(row=1, column=1)

    # ---------- Entry, StringVar, Checkbutton, Radiobutton, Combobox, Spinbox ----------
    def creer_entry_et_variables(self, row, column):
        f = tk.LabelFrame(self, text="Entry + variables", padx=8, pady=8)
        f.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)

        self.entry = tk.Entry(f, width=25)
        self.entry.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.entry.insert(0, "Texte par défaut")          # insert(index, texte) : 0 = début, "end" = fin

        tk.Button(f, text="get", command=lambda: print("Entry =", self.entry.get())).grid(row=1, column=0)
        tk.Button(f, text="delete", command=lambda: self.entry.delete(0, "end")).grid(row=1, column=1)
        tk.Button(f, text="sélection", command=lambda: self.entry.selection_range(0, "end")).grid(row=1, column=2)

        self.mdp = tk.Entry(f, show="*")                  # champ mot de passe
        self.mdp.grid(row=2, column=0, columnspan=3, sticky="ew", pady=4)

        self.var_check = tk.BooleanVar(value=True)        # IntVar() marche aussi (0 / 1)
        tk.Checkbutton(f, text="Case", variable=self.var_check).grid(row=3, column=0, sticky="w")

        self.var_radio = tk.StringVar(value="A")
        tk.Radiobutton(f, text="A", variable=self.var_radio, value="A").grid(row=3, column=1)
        tk.Radiobutton(f, text="B", variable=self.var_radio, value="B").grid(row=3, column=2)

        self.combo = ttk.Combobox(f, values=["Un", "Deux", "Trois"], state="readonly")
        self.combo.grid(row=4, column=0, columnspan=2, sticky="ew", pady=4)
        self.combo.current(0)                             # sélectionne l'index 0 ; .get() lit le texte

        self.spin = tk.Spinbox(f, from_=0, to=10, increment=1, width=5)
        self.spin.grid(row=4, column=2)

        self.btn_etat = tk.Button(f, text="Lire tout", command=self.lire_tout)
        self.btn_etat.grid(row=5, column=0, columnspan=3, sticky="ew", pady=4)
        tk.Button(f, text="Activer / désactiver ce bouton ↑", command=self.basculer_etat).grid(
            row=6, column=0, columnspan=3, sticky="ew")

    def lire_tout(self):
        messagebox.showinfo("Valeurs", f"Entry : {self.entry.get()}\nCase : {self.var_check.get()}\n"
                                       f"Radio : {self.var_radio.get()}\nCombo : {self.combo.get()}\n"
                                       f"Spinbox : {self.spin.get()}")

    def basculer_etat(self):
        # cget lit une option, config la modifie
        nouvel_etat = "normal" if self.btn_etat.cget("state") == "disabled" else "disabled"
        self.btn_etat.config(state=nouvel_etat)

    # ---------- Text : index "ligne.colonne" (ligne commence à 1, colonne à 0) ----------
    def creer_text(self, row, column):
        f = tk.LabelFrame(self, text="Text (multiligne)", padx=8, pady=8)
        f.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
        f.columnconfigure((0, 1, 2), weight=1)
        f.rowconfigure(0, weight=1)

        self.text = tk.Text(f, height=6, wrap="word", undo=True)
        self.text.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.text.insert("end", "Ligne 1 — important.\nLigne 2 — à supprimer.\nLigne 3.\n")

        tk.Button(f, text="Lire ligne 1", command=lambda: print(self.text.get("1.0", "1.end"))).grid(row=1, column=0, sticky="ew")
        tk.Button(f, text="Suppr. ligne 2", command=lambda: self.text.delete("2.0", "2.end+1c")).grid(row=1, column=1, sticky="ew")
        tk.Button(f, text="Surligner", command=self.surligner).grid(row=1, column=2, sticky="ew")
        # Tout lire : self.text.get("1.0", "end-1c")   Tout effacer : self.text.delete("1.0", "end")

    def surligner(self):
        debut = self.text.search("important", "1.0", stopindex="end")
        if debut:
            self.text.tag_add("jaune", debut, f"{debut}+{len('important')}c")
            self.text.tag_config("jaune", background="yellow", foreground="red")

    # ---------- Listbox ----------
    def creer_listbox(self, row, column):
        f = tk.LabelFrame(self, text="Listbox", padx=8, pady=8)
        f.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
        f.columnconfigure((0, 1, 2), weight=1)
        f.rowconfigure(0, weight=1)

        self.lb = tk.Listbox(f, selectmode="extended")    # "single" (défaut "browse") ou "extended"/"multiple"
        self.lb.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.lb.insert("end", "Pomme", "Poire", "Banane")

        tk.Button(f, text="Lire sélection", command=self.lire_listbox).grid(row=1, column=0, sticky="ew")
        tk.Button(f, text="Supprimer", command=self.supprimer_listbox).grid(row=1, column=1, sticky="ew")
        tk.Button(f, text="Ajouter", command=self.ajouter_listbox).grid(row=1, column=2, sticky="ew")

    def lire_listbox(self):
        for i in self.lb.curselection():                  # tuple d'index sélectionnés
            print("Sélection :", self.lb.get(i))

    def supprimer_listbox(self):
        for i in reversed(self.lb.curselection()):        # de la fin vers le début
            self.lb.delete(i)

    def ajouter_listbox(self):
        self.lb.insert("end", f"Élément {self.lb.size() + 1}")
        self.lb.see("end")                                # fait défiler jusqu'au dernier

    # ---------- Treeview (tableau) ----------
    def creer_treeview(self, row, column):
        f = tk.LabelFrame(self, text="Treeview (tableau)", padx=8, pady=8)
        f.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
        f.columnconfigure(0, weight=1)
        f.rowconfigure(0, weight=1)

        colonnes = ("nom", "age")
        self.tree = ttk.Treeview(f, columns=colonnes, show="headings", height=5)
        self.tree.heading("nom", text="Nom")
        self.tree.heading("age", text="Âge")
        self.tree.column("age", width=60, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(f, orient="vertical", command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

        for nom, age in [("Alice", 20), ("Bob", 25), ("Chloé", 31)]:
            self.tree.insert("", "end", values=(nom, age))

        barre = tk.Frame(f)
        barre.grid(row=1, column=0, columnspan=2, sticky="ew")
        tk.Button(barre, text="Lire sélection", command=self.lire_tree).grid(row=0, column=0)
        tk.Button(barre, text="Supprimer", command=lambda: self.tree.delete(*self.tree.selection())).grid(row=0, column=1)
        tk.Button(barre, text="Tout vider", command=lambda: self.tree.delete(*self.tree.get_children())).grid(row=0, column=2)
        self.tree.bind("<<TreeviewSelect>>", lambda e: print("Sélection changée"))

    def lire_tree(self):
        for item in self.tree.selection():
            valeurs = self.tree.item(item, "values")      # tuple de TEXTES ("Bob", "25")
            print("Ligne", self.tree.index(item), ":", valeurs)


if __name__ == "__main__":
    DemoWidgets().mainloop()
