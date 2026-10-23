import tkinter as tk
from tkinter import messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des réservations")
        self.geometry("400x700")
        self.create_widget()
        self.taches = []




    def create_widget(self):
        vcmd = (self.register(self.valider_entree), '%P')
        invcmd = (self.register(self.entree_invalide),)

        self.tache_var = tk.StringVar()
        self.duree_var = tk.StringVar()

        self.tache_var.trace_add("write", self.validate_tache)
        self.duree_var.trace_add("write", self.validate_tache)

        tk.Label(self, text="Ma To-Do List", font=("Arial", 18, "bold")).place(relx=0.5, rely=0.03, anchor="n")

        tk.Label(self, text="Taper la tâche à ajouter :", font=("Arial", 8)).place(relx=0.05, rely=0.1, anchor="nw")
        self.entry_tache = tk.Entry()
        self.entry_tache.place(relx=0.55, rely=0.1, anchor="nw", relwidth=0.43)
        self.couleur_originale = self.entry_tache.cget("background")

        tk.Label(self, text="Durée estimée de la tâche en minutes :", font=("Arial", 8)).place(relx=0.05, rely=0.15,
                                                                                               anchor="nw")
        self.entry_duree = tk.Entry(validate='key', validatecommand=vcmd, invalidcommand=invcmd, textvariable=self.tache_var)
        self.entry_duree.place(relx=0.55, rely=0.15, anchor="nw", relwidth=0.43)

        self.tache_prioritaire = tk.BooleanVar()
        tk.Checkbutton(self, text="Toutes les nouvelles tâches sont prioritaires", variable=self.tache_prioritaire).place(relx=0.03, rely=0.2, anchor="nw")

        tk.Label(self, text="Choisir le type de tâche :", font=("Arial", 8)).place(relx=0.05, rely=0.27, anchor="nw")

        self.type_tache = tk.StringVar(value="Personnel")
        tk.Radiobutton(self, text="Personnel", font=("Arial", 8), variable=self.type_tache, value="Personnel").place(relx=0.43, rely=0.25, anchor="nw")
        tk.Radiobutton(self, text="Professionnel", font=("Arial", 8), variable=self.type_tache, value="Professionnel").place(relx=0.43, rely=0.29, anchor="nw")

        self.button_valider = tk.Button(self, text="Ajouter la tâche", command=self.ajouter_tache, state="disabled")
        self.button_valider.place(relx=0.37, rely=0.4, anchor="nw")

        self.list_tache = tk.Listbox(self)
        self.list_tache.place(relx=0.02, rely=0.5, relwidth=0.96, anchor="nw")

    def validate_tache(self, *args):
        tache = self.entry_tache.get()
        duree = self.entry_duree.get()

        tache_valide = (tache != "")
        duree_valide = (duree != "")

        if tache_valide and duree_valide:
            self.button_valider.config(state="normal")
        else:
            self.button_valider.config(state="disabled")

    def ajouter_tache(self):
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
