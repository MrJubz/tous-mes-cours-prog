import tkinter as tk
from tkinter import messagebox


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formulaire")
        self.geometry("700x500")
        self.create_widget()
        self.taches = []

    def create_widget(self):
        vcmd = (self.register(self.valider_entree), '%P')
        invcmd = (self.register(self.entree_invalide),)

        self.tache_var = tk.StringVar()
        self.duree_var = tk.StringVar()

        self.tache_var.trace_add("write", self.validate_personne)
        self.duree_var.trace_add("write", self.validate_personne)

        tk.Label(self, text="Nom", font=("Arial", 10)).place(relx=0.05, rely=0.05)
        self.entry_name = tk.Entry()
        self.entry_name.place(relx=0.05, rely=0.1, relwidth=0.18)

        tk.Label(self, text="Email", font=("Arial", 10)).place(relx=0.25, rely=0.05)
        self.entry_email = tk.Entry()
        self.entry_email.place(relx=0.25, rely=0.1, relwidth=0.33)

        tk.Label(self, text="Âge", font=("Arial", 10)).place(relx=0.6, rely=0.05)
        self.entry_age = tk.Entry()
        self.entry_age.place(relx=0.6, rely=0.1, relwidth=0.1)

        self.button_add = tk.Button(self, text="Ajouter", command=self.add_task, state="disabled")
        self.button_add.place(relx=0.71, rely=0.09)

        self.button_delete = tk.Button(self, text="Supprimer sélection", command=self.delete_selection)
        self.button_delete.place(relx=0.8, rely=0.09)

        self.button_import_json = tk.Button(self, text="Importer JSON", command=self.import_json)
        self.button_import_json.place(relx=0.05,rely=0.9)

        self.button_import_csv = tk.Button(self, text="Importer CSV", command=self.import_csv)
        self.button_import_csv.place(relx=0.19, rely=0.9)

        self.button_export_json = tk.Button(self, text="Exporter JSON", command=self.export_json)
        self.button_export_json.place(relx=0.705, rely=0.9)

        self.button_export_csv = tk.Button(self, text="Exporter CSV", command=self.export_csv)
        self.button_export_csv.place(relx=0.84, rely=0.9)


    def import_json(self):
        pass

    def import_csv(self):
        pass

    def export_json(self):
        pass

    def export_csv(self):
        pass

    def delete_selection(self):
        pass







        self.button_valider = tk.Button(self, text="Ajouter la tâche", command=self.ajouter_tache, state="disabled")
        self.button_valider.place(relx=0.37, rely=0.4, anchor="nw")

        self.list_tache = tk.Listbox(self)
        self.list_tache.place(relx=0.02, rely=0.5, relwidth=0.96, anchor="nw")

    def validate_personne(self, *args):
        tache = self.entry_tache.get()
        duree = self.entry_duree.get()

        tache_valide = (tache != "")
        duree_valide = (duree != "")

        if tache_valide and duree_valide:
            self.button_valider.config(state="normal")
        else:
            self.button_valider.config(state="disabled")

    def add_task(self):
        tache = self.entry_tache.get()
        duree = self.entry_duree.get().strip()

        tache = {"titre": tache, "Durée": duree, "Type": self.type_tache.get(), "Prioritaire": self.tache_prioritaire.get()}
        self.taches.append(tache)
        self.refresh_listbox()

    def refresh_listbox(self):
        self.list_tache.delete(0, tk.END)
        for tache in self.taches:
            self.list_tache.insert(tk.END, self.affichage(tache))

    def affichage(self, tache):
        p = "[P]"
        t = "[Prof]" if tache["Type"] == "Professionel" else "[Pers]"
        d = tache["Durée"]

        return f"{p}{t}{d}{tache["titre"]}"


    def valider_entree(self, nouvelle_valeur):
        if nouvelle_valeur.isdigit() and 1 <= int(nouvelle_valeur) <=480 or nouvelle_valeur == "":
            self.entry_duree.config(background=self.couleur_originale)
            return True
        return False

    def entree_invalide(self):
        self.entry_duree.config(background="red")

        self.after(5000, self.reinitialiser_couleur)

        messagebox.showwarning("Entrée invalide", "Veuillez entrer un entier (positif ou négatif).")

    def reinitialiser_couleur(self):
        self.entry_duree.config(background=self.couleur_originale)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
