"""Vue : application complète « type examen ».

Formulaire (grid) + Treeview + Ajouter / Modifier / Supprimer + validation à la frappe
+ bouton désactivé + import/export JSON et CSV + graphique Matplotlib intégré.
"""
import csv
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import Article, Inventaire

COLONNES = ("nom", "categorie", "quantite", "prix", "total")


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion d'inventaire")
        self.geometry("980x600")
        self.inventaire = Inventaire()
        self.create_widgets()
        self.rafraichir()

    # =================== Construction de l'interface ===================
    def create_widgets(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        tk.Label(self, text="GESTION D'INVENTAIRE", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=8)

        gauche = tk.Frame(self)
        gauche.grid(row=1, column=0, sticky="nsew", padx=(10, 5))
        gauche.columnconfigure(0, weight=1)
        gauche.rowconfigure(2, weight=1)
        self.creer_formulaire(gauche)
        self.creer_boutons(gauche)
        self.creer_tableau(gauche)

        self.creer_graphique()

        self.label_statut = tk.Label(self, text="", anchor="w", relief="sunken")
        self.label_statut.grid(row=2, column=0, columnspan=2, sticky="ew")

    def creer_formulaire(self, parent):
        cadre = tk.LabelFrame(parent, text="Article", padx=10, pady=8)
        cadre.grid(row=0, column=0, sticky="ew")
        cadre.columnconfigure((1, 3), weight=1)

        self.var_nom = tk.StringVar()
        self.var_quantite = tk.StringVar()
        self.var_prix = tk.StringVar()
        for var in (self.var_nom, self.var_quantite, self.var_prix):
            var.trace_add("write", self.maj_boutons)

        vcmd_entier = (self.register(lambda p: p == "" or p.isdigit()), "%P")

        tk.Label(cadre, text="Nom :").grid(row=0, column=0, sticky="e", pady=3)
        tk.Entry(cadre, textvariable=self.var_nom).grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(cadre, text="Catégorie :").grid(row=0, column=2, sticky="e")
        self.combo_categorie = ttk.Combobox(cadre, values=list(Article.CATEGORIES), state="readonly")
        self.combo_categorie.grid(row=0, column=3, sticky="ew", padx=5)
        self.combo_categorie.current(0)

        tk.Label(cadre, text="Quantité :").grid(row=1, column=0, sticky="e", pady=3)
        tk.Entry(cadre, textvariable=self.var_quantite, validate="key",
                 validatecommand=vcmd_entier).grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(cadre, text="Prix :").grid(row=1, column=2, sticky="e")
        tk.Entry(cadre, textvariable=self.var_prix).grid(row=1, column=3, sticky="ew", padx=5)

    def creer_boutons(self, parent):
        barre = tk.Frame(parent)
        barre.grid(row=1, column=0, sticky="ew", pady=5)
        barre.columnconfigure(tuple(range(7)), weight=1)

        self.btn_ajouter = tk.Button(barre, text="Ajouter", command=self.ajouter, state="disabled")
        self.btn_ajouter.grid(row=0, column=0, sticky="ew", padx=2)
        self.btn_modifier = tk.Button(barre, text="Modifier", command=self.modifier, state="disabled")
        self.btn_modifier.grid(row=0, column=1, sticky="ew", padx=2)
        tk.Button(barre, text="Supprimer", command=self.supprimer).grid(row=0, column=2, sticky="ew", padx=2)
        tk.Button(barre, text="Import JSON", command=self.importer_json).grid(row=0, column=3, sticky="ew", padx=2)
        tk.Button(barre, text="Import CSV", command=self.importer_csv).grid(row=0, column=4, sticky="ew", padx=2)
        tk.Button(barre, text="Export JSON", command=self.exporter_json).grid(row=0, column=5, sticky="ew", padx=2)
        tk.Button(barre, text="Export CSV", command=self.exporter_csv).grid(row=0, column=6, sticky="ew", padx=2)

    def creer_tableau(self, parent):
        cadre = tk.Frame(parent)
        cadre.grid(row=2, column=0, sticky="nsew")
        cadre.columnconfigure(0, weight=1)
        cadre.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(cadre, columns=COLONNES, show="headings", selectmode="browse")
        for col, titre, largeur in [("nom", "Nom", 140), ("categorie", "Catégorie", 110), ("quantite", "Qté", 50),
                                    ("prix", "Prix", 70), ("total", "Total TTC", 90)]:
            self.tree.heading(col, text=titre)
            self.tree.column(col, width=largeur, anchor="w" if col in ("nom", "categorie") else "e")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(cadre, orient="vertical", command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self.remplir_formulaire)

    def creer_graphique(self):
        cadre = tk.LabelFrame(self, text="Valeur par catégorie ($)")
        cadre.grid(row=1, column=1, sticky="nsew", padx=(5, 10))
        cadre.columnconfigure(0, weight=1)
        cadre.rowconfigure(0, weight=1)
        self.fig = Figure(figsize=(4, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=cadre)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # =================== Synchronisation affichage ===================
    def rafraichir(self):
        self.tree.delete(*self.tree.get_children())
        for a in self.inventaire.articles:
            self.tree.insert("", "end", values=(a.nom, a.categorie, a.quantite, f"{a.prix:.2f}", f"{a.total():.2f}"))

        totaux = self.inventaire.total_par_categorie()
        self.ax.clear()
        self.ax.bar(list(totaux.keys()), list(totaux.values()), color=["tab:green", "tab:blue", "tab:orange"])
        self.ax.tick_params(axis="x", labelrotation=15)
        self.fig.tight_layout()
        self.canvas.draw()

        self.label_statut.config(text=f"  {len(self.inventaire.articles)} article(s) — "
                                      f"valeur totale {self.inventaire.valeur_totale():.2f} $")
        self.maj_boutons()

    def index_selectionne(self):
        selection = self.tree.selection()
        return self.tree.index(selection[0]) if selection else None

    def maj_boutons(self, *args):
        rempli = all(v.get().strip() for v in (self.var_nom, self.var_quantite, self.var_prix))
        self.btn_ajouter.config(state="normal" if rempli else "disabled")
        self.btn_modifier.config(state="normal" if rempli and self.index_selectionne() is not None else "disabled")

    def lire_formulaire(self):
        return Article(self.var_nom.get(), self.combo_categorie.get(), self.var_quantite.get(), self.var_prix.get())

    def vider_formulaire(self):
        for var in (self.var_nom, self.var_quantite, self.var_prix):
            var.set("")
        self.combo_categorie.current(0)
        self.tree.selection_remove(*self.tree.selection())

    def remplir_formulaire(self, event=None):
        index = self.index_selectionne()
        if index is None:
            return
        a = self.inventaire.articles[index]
        self.var_nom.set(a.nom)
        self.combo_categorie.set(a.categorie)
        self.var_quantite.set(str(a.quantite))
        self.var_prix.set(str(a.prix))

    # =================== Actions ===================
    def ajouter(self):
        try:
            self.inventaire.ajouter(self.lire_formulaire())
        except (ValueError, TypeError) as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.vider_formulaire()
        self.rafraichir()

    def modifier(self):
        index = self.index_selectionne()
        if index is None:
            messagebox.showwarning("Sélection", "Sélectionnez un article à modifier.")
            return
        try:
            self.inventaire.remplacer(index, self.lire_formulaire())
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.vider_formulaire()
        self.rafraichir()

    def supprimer(self):
        index = self.index_selectionne()
        if index is None:
            messagebox.showwarning("Sélection", "Sélectionnez un article à supprimer.")
            return
        nom = self.inventaire.articles[index].nom
        if messagebox.askyesno("Confirmer", f"Supprimer « {nom} » ?"):
            self.inventaire.supprimer(index)
            self.vider_formulaire()
            self.rafraichir()

    # =================== Fichiers ===================
    def charger(self, lignes):
        # Tout ou rien : on remplit un inventaire temporaire ; une ligne invalide (ou un doublon) annule l'import
        nouvel_inventaire = Inventaire()
        for d in lignes:
            nouvel_inventaire.ajouter(Article.from_dict(d))
        self.inventaire = nouvel_inventaire
        self.rafraichir()

    def importer_json(self):
        chemin = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not chemin:
            return
        try:
            with open(chemin, encoding="utf-8") as f:
                self.charger(json.load(f))
        except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
            messagebox.showerror("Import JSON", f"Fichier invalide : {e}")

    def importer_csv(self):
        chemin = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not chemin:
            return
        try:
            with open(chemin, newline="", encoding="utf-8") as f:
                self.charger(list(csv.DictReader(f)))
        except (OSError, KeyError, ValueError, TypeError) as e:
            messagebox.showerror("Import CSV", f"Fichier invalide : {e}")

    def exporter_json(self):
        chemin = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if chemin:
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump([a.to_dict() for a in self.inventaire.articles], f, indent=4, ensure_ascii=False)
            self.label_statut.config(text=f"  Exporté vers {chemin}")

    def exporter_csv(self):
        chemin = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if chemin:
            with open(chemin, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["nom", "categorie", "quantite", "prix"])
                writer.writeheader()
                writer.writerows(a.to_dict() for a in self.inventaire.articles)
            self.label_statut.config(text=f"  Exporté vers {chemin}")


if __name__ == "__main__":
    Application().mainloop()
