import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.t = tk.Text(self, width=40, height=6)
        self.t.pack(padx=10, pady=10)
        self.t.insert("end", "Ligne 1 — important.\n")
        self.t.insert("end", "Ligne 2 — à supprimer.\n")
        self.t.insert("end", "Ligne 3 — fin.\n")

        bar = tk.Frame(self); bar.pack()
        tk.Button(bar, text="Lire 1ère ligne", command=self.lire).pack(side="left", padx=4)
        tk.Button(bar, text="Supprimer ligne 2", command=self.sup2).pack(side="left", padx=4)
        tk.Button(bar, text="Surligner 'important'", command=self.hl).pack(side="left", padx=4)

    def lire(self):
        print("1ère ligne =", self.t.get("1.0", "1.end"))
        #Dans un widget Text, les indices sont de la forme ligne.colonne et
        # la numérotation commence à 1 pour les lignes et à 0 pour les colonnes

    def sup2(self):
        self.t.delete("2.0", "2.end+1c")
        #1.end+1c = un caractère après → ça inclut le saut de ligne.

    def hl(self):
        idx = self.t.search("important", "1.0", stopindex="end")
        if idx:
            fin = f"{idx}+{len('important')}c"
            self.t.tag_add("surligne", idx, fin)
            self.t.tag_config("surligne", background="yellow", foreground="red")

if __name__ == "__main__":
    App().mainloop()
