import tkinter as tk
from tkinter import messagebox

class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de tâches")
        self.geometry("500x600")
        self.creer_ui()
        self.tasks = []

    def creer_ui(self):
        self.titre = tk.Label(self, text="Ma To-Do List", font=("Arial", 20, "bold"))
        self.titre.pack(pady=10)

        self.champ_tache = tk.Entry(self, width=30)
        self.champ_tache.pack(pady=10)

        self.btn_ajouter = tk.Button(self, text="Ajouter la tâche", command=self.ajouter_tache)
        self.btn_ajouter.pack(pady=5)

        self.liste_tache = tk.Listbox(self, width=40, height=10)
        self.liste_tache.pack(pady=10)

        self.prioritaire = tk.BooleanVar(value=True)
        self.cb_prioritaire = tk.Checkbutton(self, text="Toutes les tâches sont priotaires", variable=self.prioritaire)
        self.cb_prioritaire.pack(pady=5)

        self.type_tache = tk.StringVar(value= "Personnel")
        self.rb1 = tk.Radiobutton(self, text="Personnel", variable=self.type_tache, value="Personnel")
        self.rb1.pack()
        self.rb2 = tk.Radiobutton(self, text="Professionnel", variable=self.type_tache, value="Professionnel")
        self.rb2.pack()


        self.sous_titre = tk.Label(self, text="Notes sur la tâche sélectionnée :")
        self.sous_titre.pack(pady=10)

        self.notes_tache = tk.Text(self, width=40, height=5)
        self.notes_tache.pack()

    def ajouter_tache(self):
        titre = self.champ_tache.get().strip()
        if not titre:
            messagebox.showwarning("veuillez saisir une tache")
            return
        task = {"titre": titre, "type": self.type_tache.get(), "prioritaire": self.prioritaire.get()}
        self.tasks.append(task)
        self.refresh_listbox()

    def refresh_listbox(self):
        self.liste_tache.delete(0, tk.END)
        for t in self.tasks:
            self.liste_tache.insert(tk.END, self.format_task_to_list(t))

    def format_task_to_list(self, task):
        p = "[P]" if task["prioritaire"] else ""
        titre = "Personnel" if task["type"] == "Personnel" else "Professionnel"
        return f"{p},{titre},{task["titre"]}"








if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()