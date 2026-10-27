import tkinter as tk
from tkinter import ttk, messagebox
from model import Reservation


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des réservations")
        self.geometry("700x520")
        self.create_widgets()

    def create_widgets(self):
        # anchor="n" + relx=0.5 : le HAUT-CENTRE du label est placé au milieu → titre centré
        tk.Label(self, text="GESTION DES RÉSERVATIONS", font=("Arial", 18, "bold")).place(relx=0.5, rely=0.02, anchor="n")
        tk.Label(self, text="Inscription aux activités").place(relx=0.5, rely=0.09, anchor="n")

        # ---------- Informations du client ----------
        frame_info = tk.LabelFrame(self, text="INFORMATIONS DU CLIENT", font=("Arial", 9, "bold"))
        frame_info.place(relx=0.05, rely=0.15, relwidth=0.42, relheight=0.5)

        tk.Label(frame_info, text="Nom").place(relx=0.08, rely=0.05)
        self.entry_nom = tk.Entry(frame_info)
        self.entry_nom.place(relx=0.08, rely=0.14, relwidth=0.84)

        tk.Label(frame_info, text="Courriel").place(relx=0.08, rely=0.28)
        self.entry_courriel = tk.Entry(frame_info)
        self.entry_courriel.place(relx=0.08, rely=0.37, relwidth=0.84)

        tk.Label(frame_info, text="Activité").place(relx=0.08, rely=0.51)
        self.combo_activite = ttk.Combobox(frame_info, values=list(Reservation.PRIX_ACTIVITES), state="readonly")
        self.combo_activite.place(relx=0.08, rely=0.60, relwidth=0.84)
        self.combo_activite.current(0)

        tk.Label(frame_info, text="Nombre de places").place(relx=0.08, rely=0.74)
        self.entry_places = tk.Entry(frame_info)
        self.entry_places.place(relx=0.08, rely=0.83, relwidth=0.84)
        self.entry_places.insert(0, "1")

        # ---------- Récapitulatif ----------
        frame_recap = tk.LabelFrame(self, text="RÉCAPITULATIF", font=("Arial", 9, "bold"))
        frame_recap.place(relx=0.53, rely=0.15, relwidth=0.42, relheight=0.5)

        self.recap = {}
        positions = {"Client": (0.08, 0.05), "Activité": (0.08, 0.27), "Nombre de places": (0.08, 0.49),
                     "Prix par place": (0.08, 0.71), "Prix total": (0.55, 0.71)}
        for titre, (x, y) in positions.items():
            tk.Label(frame_recap, text=titre, font=("Arial", 9, "bold")).place(relx=x, rely=y)
            self.recap[titre] = tk.Label(frame_recap, text="---")
            self.recap[titre].place(relx=x, rely=y + 0.09)

        # ---------- Boutons ----------
        tk.Button(self, text="RÉSERVER", command=self.reserver).place(relx=0.25, rely=0.69, relwidth=0.15)
        tk.Button(self, text="EFFACER", command=self.effacer).place(relx=0.425, rely=0.69, relwidth=0.15)
        tk.Button(self, text="QUITTER", command=self.destroy).place(relx=0.60, rely=0.69, relwidth=0.15)

        # ---------- Statut ----------
        frame_statut = tk.LabelFrame(self, text="STATUT")
        frame_statut.place(relx=0.05, rely=0.78, relwidth=0.9, relheight=0.15)
        self.label_statut = tk.Label(frame_statut, text="Aucune réservation", anchor="w", justify="left", wraplength=580)
        self.label_statut.place(relx=0.02, rely=0.1, relwidth=0.96)

    def reserver(self):
        # La vue ne valide rien elle-même : elle passe les textes au modèle et affiche l'erreur s'il y en a une
        try:
            reservation = Reservation(self.entry_nom.get(), self.entry_courriel.get(),
                                      self.combo_activite.get(), self.entry_places.get())
        except ValueError as e:
            messagebox.showerror("Réservation invalide", str(e))
            return

        self.recap["Client"].config(text=reservation.nom)
        self.recap["Activité"].config(text=reservation.activite)
        self.recap["Nombre de places"].config(text=str(reservation.nb_places))
        self.recap["Prix par place"].config(text=f"{reservation.obtenir_prix_unitaire():.2f} $")
        self.recap["Prix total"].config(text=f"{reservation.calculer_prix():.2f} $")
        self.label_statut.config(text=reservation.obtenir_resume())

    def effacer(self):
        self.entry_nom.delete(0, tk.END)
        self.entry_courriel.delete(0, tk.END)
        self.combo_activite.current(0)
        self.entry_places.delete(0, tk.END)
        self.entry_places.insert(0, "1")
        for label in self.recap.values():
            label.config(text="---")
        self.label_statut.config(text="Aucune réservation")


if __name__ == "__main__":
    Application().mainloop()
