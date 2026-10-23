import tkinter as tk
from tkinter import ttk
from Model import Reservation

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des réservations")
        self.geometry("700x700")
        self.create_widget()


    def create_widget(self):
        # Titre
        tk.Label(self, text="GESTION DES RÉSERVATIONS", font=("Arial", 18, "bold")).place(relx=0.5, rely=0.03, anchor="n")

        # Sous-titre
        tk.Label(self, text="Inscriptions aux activités", font=("Arial", 10)).place(relx=0.5, rely=0.08, anchor="n")

        # frame informations du client
        frame_info = tk.LabelFrame(self, text="INFORMATIONS DU CLIENT", font=("Arial", 8, "bold"))
        frame_info.place(relx=0.05, rely=0.15, anchor="nw", relwidth=0.4, relheight=0.4)

        self.label_nom = tk.Label(frame_info, text="Nom")
        self.label_nom.place(relx=0.1, rely=0.08)
        self.entree_nom = tk.Entry(frame_info)
        self.entree_nom.place(relx=0.1, rely=0.18, relwidth=0.8)

        self.label_courriel = tk.Label(frame_info, text="Courriel")
        self.label_courriel.place(relx=0.1, rely=0.28)
        self.entree_courriel = tk.Entry(frame_info)
        self.entree_courriel.place(relx=0.1, rely=0.38, relwidth=0.8)

        self.label_activite = tk.Label(frame_info, text="Activité")
        self.label_activite.place(relx=0.1, rely=0.48)
        self.entree_activite = ttk.Combobox(frame_info,values=list(Reservation.INFORMATIONS_CLIENTS.keys()), state="readonly")
        self.entree_activite.place(relx=0.1, rely=0.58, relwidth=0.8)
        self.entree_activite.current(0)

        self.label_nb_place = tk.Label(frame_info, text="Nombre de places")
        self.label_nb_place.place(relx=0.1, rely=0.68)
        self.entree_nb_place = tk.Entry(frame_info)
        self.entree_nb_place.place(relx=0.1, rely=0.78, relwidth=0.8)
        self.entree_nb_place.insert(tk.END, "1")

        # frame recapitulatif
        frame_recap = tk.LabelFrame(self, text="RÉCAPITULATIF", font=("Arial", 8, "bold"))
        frame_recap.place(relx=0.55, rely=0.15, anchor="nw", relwidth=0.4, relheight=0.4)

        self.label_client = tk.Label(frame_recap, text="Client", font=("Arial", 6, "bold"))
        self.label_client.place(relx=0.1, rely=0.08)
        self.affichage_client = tk.Label(frame_recap, text="---")
        self.affichage_client.place(relx=0.1, rely=0.14)

        self.label_activite = tk.Label(frame_recap, text="Activité", font=("Arial", 6, "bold"))
        self.label_activite.place(relx=0.1, rely=0.24)
        self.affichage_activite = tk.Label(frame_recap, text="---")
        self.affichage_activite.place(relx=0.1, rely=0.3)

        self.label_nb_place = tk.Label(frame_recap, text="Nombre de places", font=("Arial", 6, "bold"))
        self.label_nb_place.place(relx=0.1, rely=0.4)
        self.affichage_nb_place = tk.Label(frame_recap, text="---")
        self.affichage_nb_place.place(relx=0.1, rely=0.46)

        self.label_prix_place = tk.Label(frame_recap, text="Prix par place", font=("Arial", 6, "bold"))
        self.label_prix_place.place(relx=0.1, rely=0.56)
        self.affichage_prix_place = tk.Label(frame_recap, text="---")
        self.affichage_prix_place.place(relx=0.1, rely=0.62)

        self.label_prix = tk.Label(frame_recap, text="Prix total", font=("Arial", 6, "bold"))
        self.label_prix.place(relx=0.6, rely=0.56)
        self.affichage_prix_total = tk.Label(frame_recap, text="---")
        self.affichage_prix_total.place(relx=0.6, rely=0.62)

        # Boutons

        tk.Button(self, text="RÉSERVER", command=self.reserver).place(relx=0.25, rely=0.6, relwidth=0.15)
        tk.Button(self, text="EFFACER", command=self.effacer).place(relx=0.425, rely=0.6, relwidth=0.15)
        tk.Button(self, text="QUITTER   ", command=self.destroy).place(relx=0.6, rely=0.6, relwidth=0.15)

        # frame statut
        frame_satut = tk.LabelFrame(self, text="STATUT")
        frame_satut.place(relx=0.05, rely=0.67, anchor="nw", relwidth=0.9, relheight=0.08)

        self.affichage_reservations = tk.Label(frame_satut, text="Aucune réservation")
        self.affichage_reservations.place(relx= 0.05, rely=0.1)

    def reserver(self):
        client = Reservation(self.entree_nom.get(), self.entree_courriel.get(), self.entree_activite.get(), self.entree_nb_place.get())
        self.affichage_client.config(text=f"{client.nom}")
        self.affichage_activite.config(text=f"{client.activite}")
        self.affichage_nb_place.config(text=f"{client.nb_place}")
        self.affichage_prix_place.config(text=f"{client.obtenir_prix_unitaire():.2f} $")
        self.affichage_prix_total.config(text=f"{client.calculer_prix():.2f} $")

        if int(client.nb_place) > 1:
            nb_place = "places"
        else:
            nb_place = "place"
        self.affichage_reservations.config(text=f"{client.nom} à réserver {client.nb_place} {nb_place} à {client.obtenir_prix_unitaire():.2f} $ chacune pour l'activité de {client.activite}. "
                                                f"Tout ça pour un total de {client.calculer_prix():.2f} $")
    def effacer(self):
        self.entree_nom.delete(0, tk.END)
        self.entree_courriel.delete(0, tk.END)
        self.affichage_client.config(text="---")
        self.affichage_activite.config(text="---")
        self.affichage_nb_place.config(text="---")
        self.affichage_prix_place.config(text="---")
        self.affichage_prix_total.config(text="---")

        self.affichage_reservations.config(text="Aucune réservation")


if __name__ == "__main__":
    app = Application()
    app.mainloop()