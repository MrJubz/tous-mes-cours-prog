"""Gabarit : command, lambda, bind, bind_all, bind_class, événements virtuels."""
import tkinter as tk
from tkinter import ttk


class DemoEvenements(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Événements")
        self.geometry("500x380")
        self.columnconfigure(0, weight=1)

        # 1) command : clic sur un bouton. La fonction NE reçoit PAS d'event.
        tk.Button(self, text="command simple", command=self.clic).grid(row=0, column=0, pady=4)

        # 2) command + argument : il FAUT une lambda (sinon la fonction s'exécute tout de suite)
        tk.Button(self, text="command avec argument", command=lambda: self.afficher("Bonjour !")).grid(row=1, column=0, pady=4)

        # 3) bind : la fonction REÇOIT un objet event (event.widget, event.char, event.keysym, event.x...)
        self.entry = ttk.Entry(self, width=30)
        self.entry.grid(row=2, column=0, pady=4)
        self.entry.bind("<Return>", self.sur_entree)           # touche Entrée
        self.entry.bind("<KeyRelease>", self.sur_touche)       # après chaque frappe
        self.entry.bind("<FocusIn>", lambda e: self.afficher("Focus sur le champ"))

        zone = tk.Label(self, text="Clic gauche / droit / double-clic ici", bg="lightgray", height=3)
        zone.grid(row=3, column=0, sticky="ew", padx=20, pady=4)
        zone.bind("<Button-1>", lambda e: self.afficher(f"Clic gauche en ({e.x}, {e.y})"))
        zone.bind("<Button-3>", lambda e: self.afficher("Clic droit"))
        zone.bind("<Double-Button-1>", lambda e: self.afficher("Double-clic"))

        # 4) bind_class : TOUS les widgets d'une classe (ici tous les ttk.Button)
        rangee = ttk.Frame(self)
        rangee.grid(row=4, column=0, pady=4)
        for i, t in enumerate(("A", "B", "C")):
            ttk.Button(rangee, text=f"Bouton {t}").grid(row=0, column=i, padx=4)
        self.bind_class("TButton", "<Enter>", lambda e: self.afficher(f"Survol : {e.widget.cget('text')}"))

        # 5) Événement virtuel d'un widget : <<ComboboxSelected>>, <<ListboxSelect>>, <<TreeviewSelect>>
        self.combo = ttk.Combobox(self, values=["Rouge", "Vert", "Bleu"], state="readonly")
        self.combo.grid(row=5, column=0, pady=4)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.afficher(f"Choix : {self.combo.get()}"))

        # 6) Événement virtuel PERSONNALISÉ : on le déclenche nous-même avec event_generate
        self.bind("<<FormulaireValide>>", lambda e: self.title("Formulaire valide !"))
        ttk.Button(self, text="Valider (événement perso)", command=self.valider).grid(row=6, column=0, pady=4)

        # 7) bind_all : raccourci global, peu importe le widget actif
        self.bind_all("<Control-h>", self.basculer_message)
        self.bind_all("<Escape>", lambda e: self.destroy())

        self.message = tk.Label(self, text="(Ctrl+H masque ce message, Échap ferme)", fg="navy")
        self.message.grid(row=7, column=0, pady=8)

        # Redimensionnement de la fenêtre
        self.bind("<Configure>", self.sur_redimension)

    def sur_redimension(self, event):
        if event.widget is self:  # <Configure> sur la fenêtre arrive aussi pour chaque enfant
            self.title(f"Événements {event.width}×{event.height}")

    def clic(self):
        self.afficher("Bouton cliqué")

    def afficher(self, texte):
        self.message.config(text=texte)

    def sur_entree(self, event):
        self.afficher(f"Vous avez saisi : {self.entry.get()}")

    def sur_touche(self, event):
        print("Touche :", repr(event.char), event.keysym)

    def valider(self):
        if self.entry.get().strip():
            self.event_generate("<<FormulaireValide>>")

    def basculer_message(self, event=None):
        if self.message.winfo_viewable():
            self.message.grid_remove()   # cache en gardant row/column ; grid() le remet au même endroit
        else:
            self.message.grid()


if __name__ == "__main__":
    DemoEvenements().mainloop()
