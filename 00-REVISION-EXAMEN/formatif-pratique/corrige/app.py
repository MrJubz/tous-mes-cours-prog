import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json

from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from model import Etudiant, EtudiantReprise, Groupe, etudiant_depuis_dict

COLONNES = {"matricule": "Matricule", "nom": "Nom", "programme": "Programme", "moyenne": "Moyenne", "statut": "Statut"}
CHAMPS_CSV = ["type", "matricule", "nom", "programme", "tp1", "tp2", "examen", "ancien_examen"]
GRAPHIQUES = ("Histogramme des moyennes", "Moyenne par programme", "Réussite / échec")


class GestionResultats(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des résultats")
        self.geometry("1180x660")
        self.minsize(1000, 560)

        self.groupe = Groupe()
        self.tri_colonne, self.tri_inverse = "nom", False

        self.var_matricule = tk.StringVar()
        self.var_nom = tk.StringVar()
        self.var_programme = tk.StringVar(value=Etudiant.PROGRAMMES[0])
        self.var_tp1, self.var_tp2, self.var_examen = tk.StringVar(value="0"), tk.StringVar(value="0"), tk.StringVar(value="0")
        self.var_reprise = tk.BooleanVar(value=False)
        self.var_ancien = tk.StringVar(value="0")
        self.var_recherche = tk.StringVar()
        self.var_graphique = tk.StringVar(value=GRAPHIQUES[0])

        self.creer_widgets()

        self.var_matricule.trace_add("write", lambda *args: self.maj_boutons())
        self.var_nom.trace_add("write", lambda *args: self.maj_boutons())
        self.var_recherche.trace_add("write", lambda *args: self.rafraichir())
        self.bind("<Return>", lambda e: self.ajouter())
        self.bind("<Escape>", lambda e: self.effacer())

        self.rafraichir()

    # ---------- Construction ----------
    def creer_widgets(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        gauche = tk.Frame(self)
        gauche.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        gauche.columnconfigure(0, weight=1)
        gauche.rowconfigure(3, weight=1)

        self.creer_formulaire(gauche)
        self.creer_boutons(gauche)
        self.creer_recherche(gauche)
        self.creer_tableau(gauche)
        self.creer_fichiers(gauche)
        self.creer_statistiques()

        self.label_etat = tk.Label(self, anchor="w", relief="sunken", padx=6)
        self.label_etat.grid(row=1, column=0, columnspan=2, sticky="ew")

    def creer_formulaire(self, parent):
        cadre = tk.LabelFrame(parent, text="Étudiant", padx=10, pady=8)
        cadre.grid(row=0, column=0, sticky="ew")
        cadre.columnconfigure((1, 3, 5), weight=1)

        valider_matricule = (self.register(lambda p: p == "" or (p.isdigit() and len(p) <= 7)), "%P")
        tk.Label(cadre, text="Matricule :").grid(row=0, column=0, sticky="e", pady=3)
        self.entry_matricule = tk.Entry(cadre, textvariable=self.var_matricule,
                                        validate="key", validatecommand=valider_matricule)
        self.entry_matricule.grid(row=0, column=1, sticky="ew", padx=5)
        tk.Label(cadre, text="Nom :").grid(row=0, column=2, sticky="e")
        tk.Entry(cadre, textvariable=self.var_nom).grid(row=0, column=3, columnspan=3, sticky="ew", padx=5)

        tk.Label(cadre, text="Programme :").grid(row=1, column=0, sticky="e", pady=3)
        ttk.Combobox(cadre, textvariable=self.var_programme, values=Etudiant.PROGRAMMES,
                     state="readonly").grid(row=1, column=1, sticky="ew", padx=5)
        tk.Checkbutton(cadre, text="En reprise", variable=self.var_reprise,
                       command=self.maj_reprise).grid(row=1, column=2, columnspan=2, sticky="w")
        tk.Label(cadre, text="Ancien examen :").grid(row=1, column=4, sticky="e")
        self.spin_ancien = tk.Spinbox(cadre, from_=0, to=100, textvariable=self.var_ancien, width=6, state="disabled")
        self.spin_ancien.grid(row=1, column=5, sticky="ew", padx=5)

        for col, (texte, var) in enumerate((("TP1 :", self.var_tp1), ("TP2 :", self.var_tp2), ("Examen :", self.var_examen))):
            tk.Label(cadre, text=texte).grid(row=2, column=col * 2, sticky="e", pady=3)
            tk.Spinbox(cadre, from_=0, to=100, textvariable=var, width=6).grid(row=2, column=col * 2 + 1, sticky="ew", padx=5)

    def creer_boutons(self, parent):
        cadre = tk.Frame(parent)
        cadre.grid(row=1, column=0, sticky="ew", pady=6)
        cadre.columnconfigure((0, 1, 2, 3), weight=1)
        self.btn_ajouter = tk.Button(cadre, text="Ajouter", command=self.ajouter)
        self.btn_modifier = tk.Button(cadre, text="Modifier", command=self.modifier)
        self.btn_supprimer = tk.Button(cadre, text="Supprimer", command=self.supprimer)
        self.btn_effacer = tk.Button(cadre, text="Effacer les champs", command=self.effacer)
        for col, bouton in enumerate((self.btn_ajouter, self.btn_modifier, self.btn_supprimer, self.btn_effacer)):
            bouton.grid(row=0, column=col, sticky="ew", padx=3)

    def creer_recherche(self, parent):
        cadre = tk.Frame(parent)
        cadre.grid(row=2, column=0, sticky="ew")
        cadre.columnconfigure(1, weight=1)
        tk.Label(cadre, text="Rechercher (nom ou matricule) :").grid(row=0, column=0, sticky="w")
        tk.Entry(cadre, textvariable=self.var_recherche).grid(row=0, column=1, sticky="ew", padx=5)

    def creer_tableau(self, parent):
        cadre = tk.Frame(parent)
        cadre.grid(row=3, column=0, sticky="nsew", pady=6)
        cadre.columnconfigure(0, weight=1)
        cadre.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(cadre, columns=tuple(COLONNES), show="headings", selectmode="browse")
        for col, titre in COLONNES.items():
            # col=col : sans ça, tous les en-têtes trieraient par la dernière colonne de la boucle
            self.tree.heading(col, text=titre, command=lambda col=col: self.trier(col))
        self.tree.column("matricule", width=90, anchor="center")
        self.tree.column("nom", width=170)
        self.tree.column("programme", width=150)
        self.tree.column("moyenne", width=80, anchor="e")
        self.tree.column("statut", width=80, anchor="center")
        self.tree.tag_configure("echec", foreground="#c62828")
        self.tree.grid(row=0, column=0, sticky="nsew")

        barre = ttk.Scrollbar(cadre, orient="vertical", command=self.tree.yview)
        barre.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=barre.set)

        self.tree.bind("<<TreeviewSelect>>", self.sur_selection)
        self.tree.bind("<Delete>", lambda e: self.supprimer())

    def creer_fichiers(self, parent):
        cadre = tk.Frame(parent)
        cadre.grid(row=4, column=0, sticky="ew")
        cadre.columnconfigure(2, weight=1)
        tk.Button(cadre, text="Importer JSON", command=self.importer_json).grid(row=0, column=0, padx=(0, 5))
        tk.Button(cadre, text="Importer CSV", command=self.importer_csv).grid(row=0, column=1)
        tk.Button(cadre, text="Exporter JSON", command=self.exporter_json).grid(row=0, column=3, padx=5)
        tk.Button(cadre, text="Exporter CSV", command=self.exporter_csv).grid(row=0, column=4)

    def creer_statistiques(self):
        cadre = tk.LabelFrame(self, text="Statistiques", padx=8, pady=8)
        cadre.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        cadre.columnconfigure(0, weight=1)
        cadre.rowconfigure(1, weight=1)

        combo = ttk.Combobox(cadre, textvariable=self.var_graphique, values=GRAPHIQUES, state="readonly")
        combo.grid(row=0, column=0, sticky="ew")
        combo.bind("<<ComboboxSelected>>", lambda e: self.dessiner())

        self.figure = Figure(figsize=(4.6, 3.6), dpi=90)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=cadre)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", pady=6)

        self.label_stats = tk.Label(cadre, justify="left", anchor="w", font=("Consolas", 10))
        self.label_stats.grid(row=2, column=0, sticky="ew")

    # ---------- État des widgets ----------
    def formulaire_pret(self):
        return len(self.var_matricule.get()) == 7 and self.var_nom.get().strip() != ""

    def maj_boutons(self):
        self.btn_ajouter.config(state="normal" if self.formulaire_pret() else "disabled")
        etat = "normal" if self.tree.selection() else "disabled"
        self.btn_modifier.config(state=etat)
        self.btn_supprimer.config(state=etat)

    def maj_reprise(self):
        self.spin_ancien.config(state="normal" if self.var_reprise.get() else "disabled")

    # ---------- Formulaire ----------
    def lire_formulaire(self):
        """Construit l'objet à partir des champs. Les setters lèvent ValueError si une valeur est invalide."""
        args = (self.var_matricule.get(), self.var_nom.get(), self.var_programme.get(),
                self.var_tp1.get(), self.var_tp2.get(), self.var_examen.get())
        if self.var_reprise.get():
            return EtudiantReprise(*args, self.var_ancien.get())
        return Etudiant(*args)

    def remplir_formulaire(self, e):
        self.entry_matricule.config(state="normal")
        self.var_matricule.set(e.matricule)
        self.entry_matricule.config(state="readonly")  # le matricule ne se modifie pas
        self.var_nom.set(e.nom)
        self.var_programme.set(e.programme)
        self.var_tp1.set(f"{e.tp1:g}")
        self.var_tp2.set(f"{e.tp2:g}")
        self.var_examen.set(f"{e.examen:g}")
        self.var_reprise.set(isinstance(e, EtudiantReprise))
        self.var_ancien.set(f"{e.ancien_examen:g}" if isinstance(e, EtudiantReprise) else "0")
        self.maj_reprise()

    def effacer(self):
        self.tree.selection_remove(self.tree.selection())
        self.entry_matricule.config(state="normal")
        self.var_matricule.set("")
        self.var_nom.set("")
        for var in (self.var_tp1, self.var_tp2, self.var_examen, self.var_ancien):
            var.set("0")
        self.var_programme.set(Etudiant.PROGRAMMES[0])
        self.var_reprise.set(False)
        self.maj_reprise()
        self.entry_matricule.focus_set()

    def sur_selection(self, event=None):
        selection = self.tree.selection()
        if selection:
            self.remplir_formulaire(self.groupe.trouver(selection[0]))  # iid de la ligne = matricule
        self.maj_boutons()

    # ---------- CRUD ----------
    def ajouter(self):
        if not self.formulaire_pret():
            return
        try:
            self.groupe.ajouter(self.lire_formulaire())
        except ValueError as e:
            messagebox.showerror("Ajout impossible", str(e))
            return
        self.effacer()
        self.rafraichir()

    def modifier(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Modifier", "Sélectionnez un étudiant.")
            return
        try:
            self.groupe.remplacer(selection[0], self.lire_formulaire())
        except ValueError as e:
            messagebox.showerror("Modification impossible", str(e))
            return
        self.rafraichir()
        self.tree.selection_set(selection[0])

    def supprimer(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Supprimer", "Sélectionnez un étudiant.")
            return
        etudiant = self.groupe.trouver(selection[0])
        if messagebox.askyesno("Confirmer", f"Supprimer {etudiant.nom} ({etudiant.matricule}) ?"):
            self.groupe.supprimer(etudiant.matricule)
            self.effacer()
            self.rafraichir()

    # ---------- Tableau ----------
    def trier(self, colonne):
        if colonne == self.tri_colonne:
            self.tri_inverse = not self.tri_inverse
        else:
            self.tri_colonne, self.tri_inverse = colonne, False
        self.rafraichir()

    def cle_tri(self, e):
        if self.tri_colonne == "moyenne":
            return e.moyenne()
        if self.tri_colonne == "statut":
            return e.statut()
        return getattr(e, self.tri_colonne).lower()

    def rafraichir(self):
        selection = self.tree.selection()
        self.tree.delete(*self.tree.get_children())
        visibles = sorted(self.groupe.rechercher(self.var_recherche.get()), key=self.cle_tri, reverse=self.tri_inverse)
        for e in visibles:
            tags = ("echec",) if e.statut() == "Échec" else ()
            self.tree.insert("", "end", iid=e.matricule, tags=tags,
                             values=(e.matricule, e.nom, e.programme, f"{e.moyenne():.1f}", e.statut()))
        for iid in selection:
            if self.tree.exists(iid):
                self.tree.selection_set(iid)

        for col, titre in COLONNES.items():
            fleche = (" ▼" if self.tri_inverse else " ▲") if col == self.tri_colonne else ""
            self.tree.heading(col, text=titre + fleche)

        self.label_etat.config(text=f"{len(self.groupe)} étudiant(s) · {len(visibles)} affiché(s)")
        self.maj_boutons()
        self.dessiner()

    # ---------- Statistiques et graphique ----------
    def dessiner(self):
        stats = self.groupe.statistiques()
        self.ax.clear()
        if stats is None:
            self.ax.text(0.5, 0.5, "Aucune donnée", ha="center", va="center", transform=self.ax.transAxes)
            self.ax.set_axis_off()
            self.label_stats.config(text="Aucun étudiant.")
        else:
            self.ax.set_axis_on()
            choix = self.var_graphique.get()
            if choix == GRAPHIQUES[0]:
                self.ax.hist([e.moyenne() for e in self.groupe.etudiants], bins=range(0, 101, 10),
                             color="#1976d2", edgecolor="white")
                self.ax.axvline(Etudiant.SEUIL, color="#c62828", linestyle="--", label="Seuil 60 %")
                self.ax.set_xlabel("Moyenne (%)")
                self.ax.set_ylabel("Nombre d'étudiants")
                self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # pas de « 0,5 étudiant »
                self.ax.legend()
            elif choix == GRAPHIQUES[1]:
                par_prog = self.groupe.moyennes_par_programme()
                self.ax.bar([p.replace(" ", "\n", 1) for p in par_prog], list(par_prog.values()), color="#1976d2")
                self.ax.set_ylim(0, 100)
                self.ax.set_ylabel("Moyenne (%)")
            else:
                reussites = round(stats["reussite"] * stats["n"] / 100)
                self.ax.pie([reussites, stats["n"] - reussites], labels=["Réussite", "Échec"],
                            colors=["#2e7d32", "#c62828"], autopct="%1.0f%%")
            self.ax.set_title(choix)
            self.label_stats.config(text=(
                f"Moyenne du groupe : {stats['moyenne']:6.1f} %\n"
                f"Médiane           : {stats['mediane']:6.1f} %\n"
                f"Écart-type        : {stats['ecart_type']:6.1f}\n"
                f"Min / Max         : {stats['min']:.1f} / {stats['max']:.1f}\n"
                f"Taux de réussite  : {stats['reussite']:6.1f} %"))
        self.figure.tight_layout()
        self.canvas.draw()

    # ---------- Fichiers ----------
    def importer_lignes(self, lignes, premiere_ligne):
        ajoutes, erreurs = 0, []
        for no, ligne in enumerate(lignes, start=premiere_ligne):
            try:
                self.groupe.ajouter(etudiant_depuis_dict(ligne))  # le constructeur valide chaque ligne
                ajoutes += 1
            except ValueError as e:
                erreurs.append(f"Ligne {no} : {e}")
        self.rafraichir()
        message = f"{ajoutes} étudiant(s) importé(s)."
        if erreurs:
            message += f"\n\n{len(erreurs)} ligne(s) rejetée(s) :\n" + "\n".join(erreurs)
            messagebox.showwarning("Import", message)
        else:
            messagebox.showinfo("Import", message)

    def importer_json(self):
        chemin = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not chemin:
            return
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            messagebox.showerror("Import JSON", f"Fichier illisible : {e}")
            return
        if not isinstance(donnees, list):
            messagebox.showerror("Import JSON", "Le fichier doit contenir une liste d'objets.")
            return
        self.importer_lignes(donnees, premiere_ligne=1)

    def importer_csv(self):
        chemin = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not chemin:
            return
        try:
            with open(chemin, "r", newline="", encoding="utf-8") as f:
                lignes = list(csv.DictReader(f))
        except (OSError, csv.Error) as e:
            messagebox.showerror("Import CSV", f"Fichier illisible : {e}")
            return
        self.importer_lignes(lignes, premiere_ligne=2)  # la ligne 1 du fichier est l'en-tête

    def exporter_json(self):
        if not len(self.groupe):
            messagebox.showinfo("Export JSON", "Rien à exporter.")
            return
        chemin = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not chemin:
            return
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump([e.to_dict() for e in self.groupe.etudiants], f, indent=4, ensure_ascii=False)
        except OSError as e:
            messagebox.showerror("Export JSON", str(e))
            return
        messagebox.showinfo("Export JSON", f"{len(self.groupe)} étudiant(s) exporté(s).")

    def exporter_csv(self):
        if not len(self.groupe):
            messagebox.showinfo("Export CSV", "Rien à exporter.")
            return
        chemin = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not chemin:
            return
        try:
            with open(chemin, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CHAMPS_CSV)  # restval="" : colonne vide si absente
                writer.writeheader()
                writer.writerows(e.to_dict() for e in self.groupe.etudiants)
        except OSError as e:
            messagebox.showerror("Export CSV", str(e))
            return
        messagebox.showinfo("Export CSV", f"{len(self.groupe)} étudiant(s) exporté(s).")


if __name__ == "__main__":
    GestionResultats().mainloop()
