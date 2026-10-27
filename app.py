import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

CATEGORIES = ["Roman", "Essai", "Science", "Biographie", "Technologie"]
STATUTS = ["Disponible", "Emprunté"]

class Livre:

    def __init__(self, titre, auteur, categorie, statut):
        self.titre = titre
        self.auteur = auteur
        self.categorie = categorie
        self.statut = statut


    @property
    def titre(self):
        return self.__titre

    @titre.setter
    def titre(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le titre ne peux pas etre vide")
        self.__titre = valeur

    @property
    def auteur(self):
        return self.__auteur

    @auteur.setter
    def auteur(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("L'auteur ne peux pas etre vide")
        self.__auteur = valeur

    @property
    def categorie(self):
        return self.__categorie

    @categorie.setter
    def categorie(self, valeur):
        if not isinstance(valeur, str) or valeur not in CATEGORIES:
            raise ValueError("La categorie doit exister")
        self.__categorie = valeur

    @property
    def statut(self):
        return self.__statut

    @statut.setter
    def statut(self, valeur):
        if not isinstance(valeur, str) or valeur not in STATUTS:
            raise ValueError("Le statut doit exister")
        self.__statut = valeur

    def to_dict(self):
        return {"titre": self.titre, "auteur": self.auteur, "categorie": self.categorie, "statut": self.statut}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de Bibliothèque")
        self.geometry("950x350")
        self.livres = []
        self.nouveau_livre = True

        self.create_widgets()

    def create_widgets(self):
        frame_fiche = tk.LabelFrame(self, text="Fiche du livre", padx=10, pady=4)
        frame_fiche.place(relx=0.01, rely=0.015, relwidth=0.35, relheight=0.9)

        tk.Label(frame_fiche, text="Titre").place(relx=0.05, rely=0.05, anchor="nw")
        self.entry_titre = tk.Entry(frame_fiche)
        self.entry_titre.place(relx=0.4, rely=0.05, relwidth=0.6)

        tk.Label(frame_fiche, text="Auteur").place(relx=0.05, rely=0.2, anchor="nw")
        self.entry_auteur = tk.Entry(frame_fiche)
        self.entry_auteur.place(relx=0.4, rely=0.2, relwidth=0.6)

        tk.Label(frame_fiche, text="Categorie").place(relx=0.05, rely=0.35, anchor="nw")
        self.var_categorie = tk.StringVar()
        self.entry_categorie = ttk.Combobox(frame_fiche, textvariable=self.var_categorie, values=CATEGORIES, state="readonly")
        self.entry_categorie.place(relx=0.4, rely=0.35, relwidth=0.6)

        tk.Label(frame_fiche, text="Statut").place(relx=0.05, rely=0.5, anchor="nw")
        self.var_statut = tk.StringVar(value=STATUTS[0])
        self.entry_statut = ttk.Combobox(frame_fiche, textvariable=self.var_statut, values=STATUTS, state="readonly")
        self.entry_statut.place(relx=0.4, rely=0.5, relwidth=0.6)


        frame_outils = tk.LabelFrame(frame_fiche, text="Outils de gestion", padx=10, pady=4)
        frame_outils.place(relx=0.005, rely=0.65, relwidth=0.995, relheight=0.3)

        self.btn_ajouter = tk.Button(frame_outils, text="Nouveau", font=("Arial", 8), command=self.nouveau)
        self.btn_ajouter.place(relx=0.01, rely=0, relwidth=0.32, relheight=0.4)
        self.btn_modifier = tk.Button(frame_outils, text="Ajouter", font=("Arial", 8), command=self.ajouter)
        self.btn_modifier.place(relx=0.34, rely=0, relwidth=0.32, relheight=0.4)
        self.btn_supprimer = tk.Button(frame_outils, text="Supprimer", font=("Arial", 8), command=self.supprimer)
        self.btn_supprimer.place(relx=0.67, rely=0, relwidth=0.32, relheight=0.4)
        self.btn_ajouter = tk.Button(frame_outils, text="Importer JSON", font=("Arial", 8), command=self.importer_json)
        self.btn_ajouter.place(relx=0.01, rely=0.5, relwidth=0.32, relheight=0.4)
        self.btn_modifier = tk.Button(frame_outils, text="Exporter JSON", font=("Arial", 8), command=self.exporter_json)
        self.btn_modifier.place(relx=0.34, rely=0.5, relwidth=0.32, relheight=0.4)
        self.btn_supprimer = tk.Button(frame_outils, text="Quitter", font=("Arial", 8), command=self.destroy)
        self.btn_supprimer.place(relx=0.67, rely=0.5, relwidth=0.32, relheight=0.4)

        self.columns = ("titre", "auteur", "categorie", "dispo")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        self.tree.column("titre", width=120)
        self.tree.column("auteur", width=120)
        self.tree.column("categorie", width=80, anchor="e")
        self.tree.column("dispo", width=80, anchor="center")
        self.tree.heading("titre", text="Titre")
        self.tree.heading("auteur", text="Auteur")
        self.tree.heading("categorie", text="Catégorie")
        self.tree.heading("dispo", text="Disponibilité")
        self.tree.place(relx=0.38, rely=0.025, relwidth=0.6, relheight=0.9)

    def nouveau(self):
        self.nouveau_livre = True

        self.entry_titre.delete(0, tk.END)
        self.entry_auteur.delete(0, tk.END)
        self.entry_categorie.set(value="")
        self.entry_statut.set(value=STATUTS[0])

        messagebox.showinfo("Mode Nouveau", "Vous pouvez maintenant ajouter un nouveau livre.")

    def ajouter(self):
        if self.livres and not self.nouveau_livre:
            messagebox.showwarning("Action requise", "Le tableau contient deja des livres.\n"
                                           "Cliquer sur 'Nouveau' avant d'ajouter un autre.")
            return
        titre = self.entry_titre.get()
        auteur = self.entry_auteur.get()
        categorie = self.entry_categorie.get()
        statut = self.entry_statut.get()
        try:
            livre = Livre(titre, auteur, categorie, statut)
            for livre_in_liste in self.livres:
                if (livre.titre == livre_in_liste.titre and
                        livre.auteur == livre_in_liste.auteur and
                        livre.categorie == livre_in_liste.categorie):
                    messagebox.showwarning("Action requise", "Le tableau contient deja ce livre.")
                    return
            self.livres.append(livre)

            self.tree.insert('', 'end', values=(livre.titre, livre.auteur, livre.categorie, livre.statut))
            self.nouveau_livre = False
            messagebox.showinfo("Succès", f"Le livre '{livre.titre}' a été ajouté.")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("selection obligatoire", "Merci de choisir un produit à supprimer")
            return
        for item in selected:
            values = self.tree.item(item, "values")
            for livre in self.livres:
                if (livre.titre == values[0] and
                        livre.auteur == values[1] and
                        livre.categorie == values[2]):
                    self.livres.remove(livre)

            self.tree.delete(item)

    def importer_json(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not filepath:
            return

        try:
            with open(filepath, mode="r", newline='', encoding='utf-8') as file:
                data = json.load(file)

            if not isinstance(data, list):
                messagebox.showerror("Erreur", "le fichier json doit contenir une liste d'objets")
                return

            for item in data:
                livre = Livre(item["titre"], item["auteur"], item["categorie"], item["statut"])
                for livre_in_liste in self.livres:
                    if (livre.titre == livre_in_liste.titre and
                            livre.auteur == livre_in_liste.auteur and
                            livre.categorie == livre_in_liste.categorie):
                        self.livres.remove(livre)
                self.livres.append(livre)
                self.tree.insert("", "end", values=(livre.titre, livre.auteur, livre.categorie, livre.statut))
            messagebox.showinfo("importation", f"{len(data)} livre(s) importé(s)")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def exporter_json(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not filepath:
            return

        data = []

        for livre in self.livres:
            data.append(livre.to_dict())

        with open(filepath, mode="w", newline="", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("sauvegarde", "les livres sont enregistrés dans un fichier json")





if __name__ == "__main__":
    app = App()
    app.mainloop()