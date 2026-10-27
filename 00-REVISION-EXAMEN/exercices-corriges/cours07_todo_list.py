import tkinter as tk
from tkinter import messagebox


class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de tâches")
        self.geometry("450x600")
        self.taches = []
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        tk.Label(self, text="Ma To-Do List", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=10)

        saisie = tk.Frame(self)
        saisie.grid(row=1, column=0, pady=5)
        self.champ_tache = tk.Entry(saisie, width=30)
        self.champ_tache.grid(row=0, column=0, padx=5)
        self.champ_tache.bind("<Return>", lambda e: self.ajouter_tache())
        tk.Button(saisie, text="Ajouter la tâche", command=self.ajouter_tache).grid(row=0, column=1, padx=5)

        # exportselection=False : la sélection reste active quand on clique dans la zone de notes
        self.liste_taches = tk.Listbox(self, height=10, exportselection=False)
        self.liste_taches.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.liste_taches.bind("<<ListboxSelect>>", self.afficher_notes)

        options = tk.Frame(self)
        options.grid(row=3, column=0, pady=5)
        self.prioritaire = tk.BooleanVar(value=False)
        tk.Checkbutton(options, text="Toutes les nouvelles tâches sont prioritaires",
                       variable=self.prioritaire).grid(row=0, column=0, columnspan=2)
        self.type_tache = tk.StringVar(value="Personnel")
        tk.Radiobutton(options, text="Personnel", variable=self.type_tache,
                       value="Personnel").grid(row=1, column=0)
        tk.Radiobutton(options, text="Professionnel", variable=self.type_tache,
                       value="Professionnel").grid(row=1, column=1)

        tk.Label(self, text="Notes sur la tâche sélectionnée :").grid(row=4, column=0, pady=(10, 0))
        self.notes = tk.Text(self, height=5, wrap="word")
        self.notes.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.notes.bind("<KeyRelease>", self.sauver_notes)

    def ajouter_tache(self):
        titre = self.champ_tache.get().strip()
        if not titre:
            messagebox.showwarning("Tâche vide", "Veuillez saisir une tâche.")
            return
        self.taches.append({"titre": titre, "type": self.type_tache.get(),
                            "prioritaire": self.prioritaire.get(), "notes": ""})
        self.champ_tache.delete(0, tk.END)
        self.rafraichir_liste()

    def rafraichir_liste(self):
        self.liste_taches.delete(0, tk.END)
        for tache in self.taches:
            self.liste_taches.insert(tk.END, self.formater(tache))

    def formater(self, tache):
        p = "[P]" if tache["prioritaire"] else ""
        t = "[Prof]" if tache["type"] == "Professionnel" else "[Pers]"
        return f"{p}{t} {tache['titre']}"

    def index_selectionne(self):
        selection = self.liste_taches.curselection()
        return selection[0] if selection else None

    def afficher_notes(self, event=None):
        index = self.index_selectionne()
        if index is None:
            return
        self.notes.delete("1.0", tk.END)
        self.notes.insert("1.0", self.taches[index]["notes"])

    def sauver_notes(self, event=None):
        index = self.index_selectionne()
        if index is not None:
            self.taches[index]["notes"] = self.notes.get("1.0", "end-1c")


if __name__ == "__main__":
    ToDoApp().mainloop()
