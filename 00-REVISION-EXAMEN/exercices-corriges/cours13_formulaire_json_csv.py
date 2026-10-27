import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv

FIELDS = ("nom", "email", "age")


class Formulaire(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formulaire")
        self.geometry("720x450")
        self.rows = []  # la "vraie" liste de données ; le Treeview n'est que l'affichage
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ---------- En-tête : champs + Ajouter / Supprimer ----------
        header = tk.Frame(self)
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=5)
        header.columnconfigure((0, 1, 2), weight=1)

        tk.Label(header, text="Nom").grid(row=0, column=0, sticky="w")
        tk.Label(header, text="Email").grid(row=0, column=1, sticky="w")
        tk.Label(header, text="Âge").grid(row=0, column=2, sticky="w")

        self.entry_nom = tk.Entry(header)
        self.entry_nom.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        self.entry_email = tk.Entry(header, width=35)
        self.entry_email.grid(row=1, column=1, sticky="ew", padx=5)
        self.entry_age = tk.Entry(header, width=8)
        self.entry_age.grid(row=1, column=2, sticky="ew", padx=5)

        tk.Button(header, text="Ajouter", command=self.ajouter).grid(row=1, column=3, padx=5)
        tk.Button(header, text="Supprimer sélection", command=self.supprimer).grid(row=1, column=4)

        # ---------- Tableau ----------
        self.tree = ttk.Treeview(self, columns=FIELDS, show="headings", selectmode="extended")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("email", text="Email")
        self.tree.heading("age", text="Âge")
        self.tree.column("nom", width=180)
        self.tree.column("email", width=300)
        self.tree.column("age", width=80, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        # ---------- Pied : import / export ----------
        footer = tk.Frame(self)
        footer.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        footer.columnconfigure(2, weight=1)  # colonne vide qui pousse les boutons Exporter à droite
        tk.Button(footer, text="Importer JSON", command=self.importer_json).grid(row=0, column=0, padx=(0, 5))
        tk.Button(footer, text="Importer CSV", command=self.importer_csv).grid(row=0, column=1)
        tk.Button(footer, text="Exporter JSON", command=self.exporter_json).grid(row=0, column=3, padx=5)
        tk.Button(footer, text="Exporter CSV", command=self.exporter_csv).grid(row=0, column=4)

    # ---------- Ajouter / Supprimer ----------
    def valider(self, nom, email, age):
        nom = str(nom).strip()
        email = str(email).strip()
        age = str(age).strip()
        if not nom:
            raise ValueError("Le nom est obligatoire.")
        if "@" not in email:
            raise ValueError(f"Email invalide : « {email} ».")
        if not age.isdigit():
            raise ValueError(f"L'âge doit être un entier (reçu « {age} »).")
        return {"nom": nom, "email": email, "age": int(age)}

    def ajouter(self):
        try:
            ligne = self.valider(self.entry_nom.get(), self.entry_email.get(), self.entry_age.get())
        except ValueError as e:
            messagebox.showwarning("Validation", str(e))
            return
        self.rows.append(ligne)
        self.rafraichir_tableau()
        for entry in (self.entry_nom, self.entry_email, self.entry_age):
            entry.delete(0, tk.END)

    def supprimer(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Validation", "Aucun élément sélectionné.")
            return
        # On supprime par index, du plus grand au plus petit, pour ne pas décaler les suivants
        indices = sorted((self.tree.index(item) for item in selection), reverse=True)
        for index in indices:
            self.rows.pop(index)
        self.rafraichir_tableau()

    def rafraichir_tableau(self):
        self.tree.delete(*self.tree.get_children())
        for ligne in self.rows:
            self.tree.insert("", "end", values=(ligne["nom"], ligne["email"], ligne["age"]))

    # ---------- Import ----------
    def charger_lignes(self, donnees_brutes):
        """Valide chaque ligne lue ; les lignes invalides sont comptées puis ignorées."""
        valides, rejetees = [], 0
        for r in donnees_brutes:
            try:
                valides.append(self.valider(r.get("nom", ""), r.get("email", ""), r.get("age", "")))
            except (ValueError, AttributeError):
                rejetees += 1
        self.rows = valides
        self.rafraichir_tableau()
        message = f"{len(valides)} ligne(s) importée(s)."
        if rejetees:
            message += f"\n{rejetees} ligne(s) invalide(s) ignorée(s)."
        messagebox.showinfo("Import", message)

    def importer_json(self):
        path = filedialog.askopenfilename(title="Importer JSON", filetypes=[("JSON", "*.json"), ("Tous", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Le fichier JSON doit contenir une liste d'objets.")
            self.charger_lignes(data)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            messagebox.showerror("Erreur d'importation", str(e))

    def importer_csv(self):
        path = filedialog.askopenfilename(title="Importer CSV", filetypes=[("CSV", "*.csv"), ("Tous", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", newline="", encoding="utf-8") as f:
                self.charger_lignes(list(csv.DictReader(f)))
        except (OSError, csv.Error) as e:
            messagebox.showerror("Erreur d'importation", str(e))

    # ---------- Export ----------
    def exporter_json(self):
        if not self.rows:
            messagebox.showinfo("Export JSON", "Rien à exporter.")
            return
        path = filedialog.asksaveasfilename(title="Exporter JSON", defaultextension=".json",
                                            filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                # ensure_ascii=False : les accents restent lisibles dans le fichier (sinon codes \uXXXX)
                json.dump(self.rows, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Export JSON", "Export terminé.")
        except OSError as e:
            messagebox.showerror("Échec export", str(e))

    def exporter_csv(self):
        if not self.rows:
            messagebox.showinfo("Export CSV", "Rien à exporter.")
            return
        path = filedialog.asksaveasfilename(title="Exporter CSV", defaultextension=".csv",
                                            filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(self.rows)
            messagebox.showinfo("Export CSV", "Export terminé.")
        except OSError as e:
            messagebox.showerror("Échec export", str(e))


if __name__ == "__main__":
    Formulaire().mainloop()
