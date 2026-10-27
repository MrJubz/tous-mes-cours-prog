class Reservation:
    PRIX_ACTIVITES = {
        "Programmation": 40,
        "Robotique": 55,
        "Intelligence artificielle": 65,
        "Développement Web": 45,
    }

    def __init__(self, nom, courriel, activite, nb_places):
        self.nom = nom
        self.courriel = courriel
        self.activite = activite
        self.nb_places = nb_places

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, valeur):
        if not str(valeur).strip():
            raise ValueError("Le nom ne peut pas être vide.")
        self.__nom = str(valeur).strip()

    @property
    def courriel(self):
        return self.__courriel

    @courriel.setter
    def courriel(self, valeur):
        valeur = str(valeur).strip()
        if not valeur:
            raise ValueError("Le courriel ne peut pas être vide.")
        if "@" not in valeur:
            raise ValueError("Le courriel doit contenir un @.")
        self.__courriel = valeur

    @property
    def activite(self):
        return self.__activite

    @activite.setter
    def activite(self, valeur):
        if valeur not in self.PRIX_ACTIVITES:
            raise ValueError(f"L'activité doit être une de : {', '.join(self.PRIX_ACTIVITES)}.")
        self.__activite = valeur

    @property
    def nb_places(self):
        return self.__nb_places

    @nb_places.setter
    def nb_places(self, valeur):
        # On convertit ici : la vue peut envoyer directement le texte de l'Entry
        try:
            valeur = int(valeur)
        except (ValueError, TypeError):
            raise ValueError("Le nombre de places doit être un entier.")
        if valeur <= 0:
            raise ValueError("Le nombre de places doit être supérieur à 0.")
        self.__nb_places = valeur

    def obtenir_prix_unitaire(self):
        return self.PRIX_ACTIVITES[self.activite]

    def calculer_prix(self):
        return self.obtenir_prix_unitaire() * self.nb_places

    def obtenir_resume(self):
        mot = "places" if self.nb_places > 1 else "place"
        return (f"{self.nom} a réservé {self.nb_places} {mot} en {self.activite} "
                f"pour un total de {self.calculer_prix():.2f} $")
