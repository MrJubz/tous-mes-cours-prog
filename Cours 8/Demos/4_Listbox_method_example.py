import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lb = tk.Listbox(self, height=6)
        self.lb.pack(padx=10, pady=10, fill="both")
        self.lb.insert("end", "Élément A", "Élément B", "Élément C")

        bar = tk.Frame(self); bar.pack()
        tk.Button(bar, text="Lire sélection", command=self.lire_sel).pack(side="left", padx=4)
        tk.Button(bar, text="Supprimer sélection", command=self.sup_sel).pack(side="left", padx=4)
        tk.Button(bar, text="Ajouter en fin", command=self.ajout_fin).pack(side="left", padx=4)

    def lire_sel(self):
        for i in self.lb.curselection():
            print("Sélection =", self.lb.get(i))

    def sup_sel(self):
        for i in (self.lb.curselection()):
            self.lb.delete(i)

    def ajout_fin(self):
        self.lb.insert("end", "Nouveau")
        self.lb.see("end")
        #self.lb.see("end") fait défiler la Listbox jusqu’à rendre visible le dernier élément.

if __name__ == "__main__":
    App().mainloop()
