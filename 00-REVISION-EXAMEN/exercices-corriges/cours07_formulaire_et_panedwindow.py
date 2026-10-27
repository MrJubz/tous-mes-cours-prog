import tkinter as tk
from tkinter import messagebox


class Formulaire(tk.Tk):
    """Interface 2 : Nom / Email + Valider, dans un cadre."""

    def __init__(self):
        super().__init__()
        self.title("Formulaire")
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        cadre = tk.Frame(self, relief="groove", borderwidth=2, padx=15, pady=15)
        cadre.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        cadre.columnconfigure(1, weight=1)

        tk.Label(cadre, text="Nom :").grid(row=0, column=0, sticky="e", pady=2)
        self.entry_nom = tk.Entry(cadre, width=40)
        self.entry_nom.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(cadre, text="Email :").grid(row=1, column=0, sticky="e", pady=2)
        self.entry_email = tk.Entry(cadre, width=40)
        self.entry_email.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # rowspan=2 : le bouton est centré à côté des deux lignes
        tk.Button(cadre, text="Valider", command=self.valider).grid(row=0, column=2, rowspan=2, padx=10)

    def valider(self):
        nom = self.entry_nom.get().strip()
        email = self.entry_email.get().strip()
        if not nom or "@" not in email:
            messagebox.showerror("Erreur", "Nom obligatoire et email avec un @.")
            return
        messagebox.showinfo("OK", f"Bonjour {nom} ({email})")


class DemoPanedWindow(tk.Tk):
    """Interface 3 : liste à gauche, notes à droite, séparateur déplaçable."""

    def __init__(self):
        super().__init__()
        self.title("Pannedwindow")
        self.geometry("800x400")
        self.create_widgets()

    def create_widgets(self):
        paned = tk.PanedWindow(self, orient="horizontal", sashwidth=6)
        paned.pack(fill="both", expand=True)  # un seul widget dans la fenêtre : pack ou grid, peu importe

        gauche = tk.LabelFrame(paned, text="Liste d'éléments", padx=5, pady=5)
        gauche.columnconfigure((0, 1), weight=1)
        gauche.rowconfigure(0, weight=1)
        self.liste = tk.Listbox(gauche)
        self.liste.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.liste.insert("end", "Pomme", "Poire", "Banane", "Ananas", "Mangue")
        tk.Button(gauche, text="Lire sélection", command=self.lire_selection).grid(row=1, column=0, sticky="ew", pady=5)
        tk.Button(gauche, text="Supprimer", command=self.supprimer).grid(row=1, column=1, sticky="ew", pady=5)

        droite = tk.LabelFrame(paned, text="Notes", padx=5, pady=5)
        droite.columnconfigure((0, 1, 2, 3), weight=1)
        droite.rowconfigure(0, weight=1)
        self.notes = tk.Text(droite, wrap="word", undo=True)
        self.notes.grid(row=0, column=0, columnspan=4, sticky="nsew")
        tk.Button(droite, text="Insérer démo", command=self.inserer_demo).grid(row=1, column=0, sticky="ew", pady=5)
        tk.Button(droite, text="Tout lire", command=self.tout_lire).grid(row=1, column=1, sticky="ew", pady=5)
        tk.Button(droite, text="Effacer", command=lambda: self.notes.delete("1.0", "end")).grid(row=1, column=2, sticky="ew", pady=5)
        tk.Button(droite, text="(Option)", command=self.surligner).grid(row=1, column=3, sticky="ew", pady=5)

        paned.add(gauche, minsize=150)
        paned.add(droite, minsize=300)

    def lire_selection(self):
        for i in self.liste.curselection():
            self.notes.insert("end", f"Sélection : {self.liste.get(i)}\n")

    def supprimer(self):
        # reversed : on supprime de la fin vers le début pour ne pas décaler les index
        for i in reversed(self.liste.curselection()):
            self.liste.delete(i)

    def inserer_demo(self):
        self.notes.insert("end", "Ligne de démo — important.\n")

    def tout_lire(self):
        messagebox.showinfo("Contenu", self.notes.get("1.0", "end-1c") or "(vide)")

    def surligner(self):
        debut = self.notes.search("important", "1.0", stopindex="end")
        if debut:
            self.notes.tag_add("surligne", debut, f"{debut}+{len('important')}c")
            self.notes.tag_config("surligne", background="yellow")


if __name__ == "__main__":
    Formulaire().mainloop()
    DemoPanedWindow().mainloop()
