import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TYPES_GRAPHIQUES = ["Courbe linéaire", "Nuage de points", "Diagramme en barres"]
AGES = {"Alice": 21, "Bob": 34, "Chloé": 19, "David": 45, "Émile": 28}


class ApplicationGraphiques(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualisation de graphiques scientifiques")
        self.geometry("800x600")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.type_graphique = tk.StringVar(value=TYPES_GRAPHIQUES[0])
        self.creer_controles()
        self.creer_graphique()
        self.tracer()  # un premier graphique dès l'ouverture

    def creer_controles(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ttk.Label(frame, text="Type de graphique :").grid(row=0, column=0, padx=(0, 10))
        combo = ttk.Combobox(frame, textvariable=self.type_graphique, values=TYPES_GRAPHIQUES,
                             state="readonly", width=22)
        combo.grid(row=0, column=1)
        # « Mettre à jour automatiquement » : on redessine dès qu'un choix est fait
        combo.bind("<<ComboboxSelected>>", lambda e: self.tracer())

    def creer_graphique(self):
        # Figure (et non plt.figure) : pas de fenêtre matplotlib séparée, tout reste dans Tkinter
        self.fig = Figure(figsize=(8, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def tracer(self):
        self.ax.clear()
        choix = self.type_graphique.get()

        if choix in ("Courbe linéaire", "Nuage de points"):
            x = np.linspace(0, 10, 100)  # 100 valeurs entre 0 et 10
            y = np.sin(x)
            if choix == "Courbe linéaire":
                self.ax.plot(x, y, color="blue", label="sin(x)")
            else:
                self.ax.scatter(x, y, color="red", s=15, label="sin(x)")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("sin(x)")
            self.ax.legend()
        else:
            self.ax.bar(list(AGES.keys()), list(AGES.values()), color="green")
            self.ax.set_xlabel("Personne")
            self.ax.set_ylabel("Âge")

        self.ax.set_title(choix)
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()  # sans draw(), l'écran ne change pas


if __name__ == "__main__":
    ApplicationGraphiques().mainloop()
