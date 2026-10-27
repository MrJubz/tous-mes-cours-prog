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
    # Plan de la fenêtre en fractions (0 à 1) :
    #   gauche relx 0.01 → 0.59, droite (statistiques) relx 0.60 → 0.99
    #   formulaire rely 0.015 → 0.265, boutons 0.28, recherche 0.35, tableau 0.41 → 0.88, fichiers 0.895
    def creer_widgets(self):
        self.creer_formulaire()
        self.creer_boutons()
        self.creer_recherche()
        self.creer_tableau()
        self.creer_fichiers()
        self.creer_statistiques()

        self.label_etat = tk.Label(self, anchor="w", relief="sunken", padx=6)
        self.label_etat.place(relx=0, rely=1, anchor="sw", relwidth=1)  # collée en bas, toute la largeur

    def creer_formulaire(self):
        cadre = tk.LabelFrame(self, text="Étudiant", padx=10, pady=4)
        cadre.place(relx=0.01, rely=0.015, relwidth=0.58, relheight=0.25)

        # 3 colonnes : libellé collé à droite de relx (anchor="e"), champ qui commence juste après (anchor="w")
        valider_matricule = (self.register(lambda p: p == "" or (p.isdigit() and len(p) <= 7)), "%P")
        tk.Label(cadre, text="Matricule :").place(relx=0.14, rely=0.17, anchor="e")
        self.entry_matricule = tk.Entry(cadre, textvariable=self.var_matricule,
                                        validate="key", validatecommand=valider_matricule)
        self.entry_matricule.place(relx=0.15, rely=0.17, relwidth=0.17, anchor="w")
        tk.Label(cadre, text="Nom :").place(relx=0.47, rely=0.17, anchor="e")
        tk.Entry(cadre, textvariable=self.var_nom).place(relx=0.48, rely=0.17, relwidth=0.50, anchor="w")

        tk.Label(cadre, text="Programme :").place(relx=0.14, rely=0.5, anchor="e")
        ttk.Combobox(cadre, textvariable=self.var_programme, values=Etudiant.PROGRAMMES,
                     state="readonly").place(relx=0.15, rely=0.5, relwidth=0.30, anchor="w")
        tk.Checkbutton(cadre, text="En reprise", variable=self.var_reprise,
                       command=self.maj_reprise).place(relx=0.47, rely=0.5, anchor="w")
        tk.Label(cadre, text="Ancien examen :").place(relx=0.80, rely=0.5, anchor="e")
        self.spin_ancien = tk.Spinbox(cadre, from_=0, to=100, textvariable=self.var_ancien, state="disabled")
        self.spin_ancien.place(relx=0.81, rely=0.5, relwidth=0.17, anchor="w")

        for i, (texte, var) in enumerate((("TP1 :", self.var_tp1), ("TP2 :", self.var_tp2), ("Examen :", self.var_examen))):
            tk.Label(cadre, text=texte).place(relx=0.14 + i * 0.33, rely=0.83, anchor="e")
            tk.Spinbox(cadre, from_=0, to=100, textvariable=var).place(relx=0.15 + i * 0.33, rely=0.83,
                                                                       relwidth=0.17, anchor="w")

    def creer_boutons(self):
        cadre = tk.Frame(self)
        cadre.place(relx=0.01, rely=0.28, relwidth=0.58, relheight=0.055)
        self.btn_ajouter = tk.Button(cadre, text="Ajouter", command=self.ajouter)
        self.btn_modifier = tk.Button(cadre, text="Modifier", command=self.modifier)
        self.btn_supprimer = tk.Button(cadre, text="Supprimer", command=self.supprimer)
        self.btn_effacer = tk.Button(cadre, text="Effacer les champs", command=self.effacer)
        # 4 boutons de 24 % avec 1 % d'espace entre eux
        for i, bouton in enumerate((self.btn_ajouter, self.btn_modifier, self.btn_supprimer, self.btn_effacer)):
            bouton.place(relx=0.005 + i * 0.25, rely=0, relwidth=0.24, relheight=1)

    def creer_recherche(self):
        cadre = tk.Frame(self)
        cadre.place(relx=0.01, rely=0.35, relwidth=0.58, relheight=0.05)
        tk.Label(cadre, text="Rechercher (nom ou matricule) :").place(relx=0, rely=0.5, anchor="w")
        tk.Entry(cadre, textvariable=self.var_recherche).place(relx=0.32, rely=0.5, relwidth=0.68, anchor="w")

    def creer_tableau(self):
        cadre = tk.Frame(self)
        cadre.place(relx=0.01, rely=0.41, relwidth=0.58, relheight=0.47)

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
        self.tree.place(relx=0, rely=0, relwidth=0.97, relheight=1)

        barre = ttk.Scrollbar(cadre, orient="vertical", command=self.tree.yview)
        barre.place(relx=0.97, rely=0, relwidth=0.03, relheight=1)
        self.tree.configure(yscrollcommand=barre.set)

        self.tree.bind("<<TreeviewSelect>>", self.sur_selection)
        self.tree.bind("<Delete>", lambda e: self.supprimer())

    def creer_fichiers(self):
        cadre = tk.Frame(self)
        cadre.place(relx=0.01, rely=0.895, relwidth=0.58, relheight=0.05)
        # Importer à gauche, exporter à droite, le trou du milieu reste vide
        boutons = (("Importer JSON", self.importer_json, 0), ("Importer CSV", self.importer_csv, 0.17),
                   ("Exporter JSON", self.exporter_json, 0.66), ("Exporter CSV", self.exporter_csv, 0.83))
        for texte, commande, relx in boutons:
            tk.Button(cadre, text=texte, command=commande).place(relx=relx, rely=0, relwidth=0.17, relheight=1)

    def creer_statistiques(self):
        cadre = tk.LabelFrame(self, text="Statistiques", padx=8, pady=8)
        cadre.place(relx=0.60, rely=0.015, relwidth=0.39, relheight=0.93)

        combo = ttk.Combobox(cadre, textvariable=self.var_graphique, values=GRAPHIQUES, state="readonly")
        combo.place(relx=0, rely=0, relwidth=1)
        combo.bind("<<ComboboxSelected>>", lambda e: self.dessiner())

        self.figure = Figure(figsize=(4.6, 3.6), dpi=90)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=cadre)
        self.canvas.get_tk_widget().place(relx=0, rely=0.07, relwidth=1, relheight=0.68)

        self.label_stats = tk.Label(cadre, justify="left", anchor="nw", font=("Consolas", 10))
        self.label_stats.place(relx=0, rely=0.77, relwidth=1, relheight=0.23)

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
