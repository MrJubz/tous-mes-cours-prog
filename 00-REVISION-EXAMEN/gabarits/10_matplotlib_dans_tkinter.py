"""Gabarit : graphique Matplotlib DANS une fenêtre Tkinter, mis à jour par l'utilisateur.

Schéma minimal (cours 14) :
    fig = Figure(); ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().grid(...)
    ... ax.clear(); ax.plot(...); canvas.draw()
"""
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class AppCourbes(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Courbes scientifiques")
        self.geometry("850x620")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.var_fonction = tk.StringVar(value="sin")
        self.var_frequence = tk.DoubleVar(value=1.0)
        self.var_amplitude = tk.DoubleVar(value=1.0)
        self.donnees_csv = None

        self.creer_controles()
        self.creer_graphique()
        self.tracer()

    def creer_controles(self):
        f = ttk.Frame(self)
        f.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        f.columnconfigure((0, 1, 2), weight=1)

        ttk.Label(f, text="Fréquence (Hz)").grid(row=0, column=0)
        ttk.Label(f, text="Amplitude").grid(row=0, column=1)
        ttk.Label(f, text="Fonction").grid(row=0, column=2)
        ttk.Entry(f, textvariable=self.var_frequence, width=10).grid(row=1, column=0)
        ttk.Entry(f, textvariable=self.var_amplitude, width=10).grid(row=1, column=1)
        combo = ttk.Combobox(f, textvariable=self.var_fonction, state="readonly",
                             values=["sin", "cos", "exp", "barres", "histogramme", "CSV"])
        combo.grid(row=1, column=2)
        combo.bind("<<ComboboxSelected>>", lambda e: self.tracer())  # mise à jour automatique

        ttk.Button(f, text="Tracer", command=self.tracer).grid(row=0, column=3, rowspan=2, sticky="ns", padx=5)
        ttk.Button(f, text="Charger CSV", command=self.charger_csv).grid(row=0, column=4, rowspan=2, sticky="ns")

    def creer_graphique(self):
        cadre = ttk.Frame(self)
        cadre.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        cadre.columnconfigure(0, weight=1)
        cadre.rowconfigure(0, weight=1)

        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=cadre)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Barre zoom/déplacement/sauvegarde (optionnelle). Elle utilise pack en interne → son propre frame
        barre_outils = ttk.Frame(cadre)
        barre_outils.grid(row=1, column=0, sticky="ew")
        NavigationToolbar2Tk(self.canvas, barre_outils)

    def tracer(self):
        try:
            freq = self.var_frequence.get()   # DoubleVar.get() lève TclError si le champ n'est pas un nombre
            amp = self.var_amplitude.get()
        except tk.TclError:
            messagebox.showerror("Erreur", "Fréquence et amplitude doivent être des nombres.")
            return

        self.ax.clear()
        fct = self.var_fonction.get()
        x = np.linspace(0, 10, 500)

        if fct == "sin":
            self.ax.plot(x, amp * np.sin(2 * np.pi * freq * x), label="sin")
        elif fct == "cos":
            self.ax.plot(x, amp * np.cos(2 * np.pi * freq * x), color="red", label="cos")
        elif fct == "exp":
            self.ax.plot(x, amp * np.exp(-freq * x), color="green", label="exp")
        elif fct == "barres":
            self.ax.bar(["A", "B", "C", "D"], [3 * amp, 7 * amp, 2 * amp, 5 * amp], label="valeurs")
        elif fct == "histogramme":
            self.ax.hist(amp * np.random.standard_normal(500), bins=20, edgecolor="black", label="N(0, amp)")
        elif fct == "CSV":
            if self.donnees_csv is None:
                messagebox.showinfo("CSV", "Chargez d'abord un fichier CSV (colonnes x,y).")
                return
            xs, ys = self.donnees_csv
            self.ax.plot(xs, ys, "o-", label="données CSV")

        self.ax.set_title(f"Courbe {fct}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.canvas.draw()

    def charger_csv(self):
        chemin = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not chemin:
            return
        try:
            xs, ys = [], []
            with open(chemin, newline="", encoding="utf-8") as f:
                for ligne in csv.DictReader(f):
                    xs.append(float(ligne["x"]))
                    ys.append(float(ligne["y"]))
            self.donnees_csv = (np.array(xs), np.array(ys))
            self.var_fonction.set("CSV")
            self.tracer()
        except (OSError, KeyError, ValueError) as e:
            messagebox.showerror("Erreur CSV", f"Fichier attendu avec colonnes x,y : {e}")


if __name__ == "__main__":
    AppCourbes().mainloop()
