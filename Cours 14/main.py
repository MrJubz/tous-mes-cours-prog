import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ApplicationCourbe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualisation de courbes scientifiques")
        self.geometry("800x600")

        # Configuration de la grille principale
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ---- ParamÃ¨tres par dÃ©faut ----
        self.fonction = tk.StringVar(value="Courbe linéaire")

        # ---- Interface graphique ----
        self.creer_widgets()
        self.creer_plot()

    def creer_widgets(self):
        """CrÃ©ation de la partie interface (contrÃ´les)"""
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Rendre les colonnes extensibles si besoin
        for i in range(3):
            frame.columnconfigure(i, weight=1)

        # labels
        lbl_fonc = ttk.Label(frame, text="Fonction :")
        lbl_fonc.grid(row=0, column=0,sticky="ew", padx=25)

        #inputs

        combo = ttk.Combobox(frame, textvariable=self.fonction, values=["Courbe linéaire", "Nuage de points", "Diagramme en barres"], width=10)
        combo.grid(row=1, column=0, sticky="ew", padx=25)
        combo.current(0)

        # Bouton Tracer
        btn_tracer = ttk.Button(frame, text="Tracer", command=self.tracer_courbe)
        btn_tracer.grid(row=0, column=2, columnspan=2, rowspan=2, padx=10, sticky="sn")

    def creer_plot(self):
        """Initialise le graphique Matplotlib"""
        self.fig, self.ax = plt.subplots(figsize=(8, 4)) #CrÃ©er le graphique
        #self.fig : reprÃ©sente la figure complÃ¨te, self.ax : reprÃ©sente la zone oÃ¹ l'on trace les courbes.
        #figsize=(8, 4) : dÃ©finit les dimensions de la figure .
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        #IntÃ©grer Matplotlib dans Tkinter
        #master=self indique que le parent est la fenÃªtre actuelle.
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def tracer_courbe(self):
        """Trace la courbe sÃ©lectionnÃ©e"""
        self.ax.clear()

        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        fct = self.fonction.get()

        if fct == "Courbe linéaire":
            self.ax.plot(x, y, label="sin(x)", color="blue")
        elif fct == "Nuage de points":
            self.ax.scatter(x, y, label="sin(x)", color="red")
        elif fct == "Diagramme en barres":
            self.ax.bar(["jay","james","job","jack","jiz"], [12, 14, 20, 30, 23], label="sin(x)", color="green")
        else:
            y = np.zeros_like(x)

        self.ax.set_title(f"Courbe {fct}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.ax.legend()

        self.canvas.draw()


# --------- Lancement de l'application ---------
if __name__ == "__main__":
    app = ApplicationCourbe()
    app.mainloop()