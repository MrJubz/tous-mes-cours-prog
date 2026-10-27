import matplotlib.pyplot as plt


class Livre:
    def __init__(self, titre, auteur, isbn):
        # Le constructeur passe par les setters : la validation est faite une seule fois, au bon endroit
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.__disponible = True

    @property
    def titre(self):
        return self.__titre

    @titre.setter
    def titre(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le titre ne peut pas être vide.")
        self.__titre = valeur.strip()

    @property
    def auteur(self):
        return self.__auteur

    @auteur.setter
    def auteur(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("L'auteur ne peut pas être vide.")
        self.__auteur = valeur.strip()

    @property
    def isbn(self):
        return self.__isbn

    @isbn.setter
    def isbn(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("L'ISBN ne peut pas être vide.")
        self.__isbn = valeur.strip()

    @property
    def disponible(self):
        return self.__disponible

    def emprunter(self):
        if not self.__disponible:
            raise ValueError(f"« {self.titre} » est déjà emprunté.")
        self.__disponible = False

    def retourner(self):
        if self.__disponible:
            raise ValueError(f"« {self.titre} » n'était pas emprunté.")
        self.__disponible = True

    def __str__(self):
        etat = "disponible" if self.__disponible else "emprunté"
        return f"{self.titre} — {self.auteur} (ISBN {self.isbn}) : {etat}"


class LivreNumerique(Livre):
    def __init__(self, titre, auteur, isbn, taille_fichier):
        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier

    @property
    def taille_fichier(self):
        return self.__taille_fichier

    @taille_fichier.setter
    def taille_fichier(self, valeur):
        if not isinstance(valeur, (int, float)) or valeur <= 0:
            raise ValueError("La taille du fichier doit être un nombre strictement positif.")
        self.__taille_fichier = valeur

    def __str__(self):
        # On réutilise l'affichage de la classe parente et on ajoute seulement ce qui est nouveau
        return super().__str__() + f" [{self.taille_fichier} Mo]"


class Bibliotheque:
    def __init__(self, nom):
        self.__nom = nom
        self.__livres = []

    @property
    def nom(self):
        return self.__nom

    def ajouter_livre(self, livre):
        if not isinstance(livre, Livre):
            raise TypeError("On ne peut ajouter que des objets Livre.")
        if self.rechercher_livre(livre.isbn) is not None:
            raise ValueError(f"Un livre avec l'ISBN {livre.isbn} existe déjà.")
        self.__livres.append(livre)

    def rechercher_livre(self, isbn):
        for livre in self.__livres:
            if livre.isbn == isbn:
                return livre
        return None

    def emprunter_livre(self, isbn):
        livre = self.rechercher_livre(isbn)
        if livre is None:
            raise ValueError(f"Aucun livre avec l'ISBN {isbn}.")
        livre.emprunter()

    def retourner_livre(self, isbn):
        livre = self.rechercher_livre(isbn)
        if livre is None:
            raise ValueError(f"Aucun livre avec l'ISBN {isbn}.")
        livre.retourner()

    def afficher_livres(self):
        if not self.__livres:
            print("Aucun livre dans la bibliothèque.")
            return
        for livre in self.__livres:
            print(livre)

    def afficher_statistiques(self):
        # On compte à partir de l'état réel des livres : pas de compteur à tenir à jour à la main
        nb_disponibles = sum(1 for livre in self.__livres if livre.disponible)
        nb_empruntes = len(self.__livres) - nb_disponibles

        plt.figure(figsize=(6, 6))
        plt.pie([nb_disponibles, nb_empruntes], labels=["Disponibles", "Empruntés"],
                autopct="%1.0f%%", colors=["tab:green", "tab:red"])
        plt.title(f"Statistiques — {self.nom}")
        plt.show()


if __name__ == "__main__":
    bibliotheque = Bibliotheque("Bibliothèque du cégep")
    bibliotheque.ajouter_livre(Livre("Python pour les nuls", "John Paul Mueller", "111"))
    bibliotheque.ajouter_livre(Livre("Le Petit Prince", "Saint-Exupéry", "222"))
    bibliotheque.ajouter_livre(Livre("1984", "George Orwell", "333"))
    bibliotheque.ajouter_livre(LivreNumerique("Apprendre Tkinter", "Moi", "444", 2.5))

    try:
        bibliotheque.ajouter_livre(Livre("Doublon", "X", "111"))
    except ValueError as e:
        print("Erreur attendue :", e)

    bibliotheque.emprunter_livre("111")
    bibliotheque.emprunter_livre("444")

    try:
        bibliotheque.emprunter_livre("111")
    except ValueError as e:
        print("Erreur attendue :", e)

    bibliotheque.afficher_livres()
    bibliotheque.afficher_statistiques()
