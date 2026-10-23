import matplotlib.pyplot as plt

class Livre:
    def __init__(self, titre, auteur, isbn):
        self.__titre = titre
        self.__auteur = auteur
        self.__isbn = isbn
        self.__disponible = True

        if not isinstance(titre, str) or not titre.strip():
            raise ValueError()
        if not isinstance(auteur, str) or not auteur.strip():
            raise ValueError()
        if not isinstance(isbn, str) or not isbn.strip():
            raise ValueError()

    @property
    def titre(self):
        return self.__titre

    @property
    def auteur(self):
        return self.__auteur

    @property
    def isbn(self):
        return self.__isbn

    def emprunter(self):
        if not self.__disponible:
            raise ValueError()
        self.__disponible = False

    def retourner(self):
        self.__disponible =True

    def __str__(self):
        dispo = "disponible"
        if not self.__disponible:
            dispo = "indisponible"
        return (f"le titre du livre est {self.__titre}/n"
                f"le nom de l'auteur est {self.__auteur}/n"
                f"l'isbn du livre est {self.__isbn}"
                f"le livre est {dispo}")

class LivreNumerique(Livre):
    def __init__(self,titre, auteur, isbn, taille_fichier):
        super().__init__(titre, auteur, isbn)
        self.__taille_fichier = taille_fichier

        if not isinstance(taille_fichier, (int,float)):
            raise TypeError()
        if taille_fichier <= 0:
            raise ValueError()

    @property
    def taille_fichier(self):
        return self.__taille_fichier

    def __str__(self):
        return super().__str__() + f"la taille du fichier est {self.__taille_fichier} Mo"

class Bibliotheque:
    def __init__(self, nom):
        self.__nom = nom
        self.__livres = []
        self.__nombre_livre_empruntes = 0

    def ajouter_livre(self, livre):
        if not isinstance(livre, Livre):
            raise TypeError()
        if self.rechercher_livre(livre.isbn) is not None:
            raise ValueError()
        self.__livres.append(livre)

    def rechercher_livre(self, isbn):
        for livre in self.__livres:
            if livre.isbn == isbn:
                return livre
        return None

    def emprunter_livre(self, isbn):
        livre = self.rechercher_livre(isbn)
        if livre is None:
            raise ValueError()
        livre.emprunter()
        self.__nombre_livre_empruntes += 1

    def retourner_livre(self, isbn):
        livre = self.rechercher_livre(isbn)
        if livre is None:
            raise ValueError()
        livre.retourner()
        self.__nombre_livre_empruntes -= 1

    def afficher_livres(self):
        if len(self.__livres) == 0:
            print("pas de livre dans la biblioteques")
            return
        for livre in self.__livres:
            print(livre)

    def affiche_statistiques(self):
        labels = ["disponible", "emprunter"]
        values = [len(self.__livres), self.__nombre_livre_empruntes]

        plt.figure(figsize=(6, 6))
        plt.bar(labels, values)
        plt.title("Statistique")
        plt.xlabel("etat des livres")
        plt.ylabel("nombre de livres")
        plt.show()


livre1 = Livre("Minecraft", "Java", "676767")
livre2 = Livre("Python", "Jubz", "696969")
livre3 = Livre("Frappe", "Moi", "000000")
livre4 = LivreNumerique("Touche", "Pipi", "111111", 2)

bibliotheque = Bibliotheque("Bib moi")

bibliotheque.ajouter_livre(livre1)
bibliotheque.ajouter_livre(livre2)
bibliotheque.ajouter_livre(livre3)
bibliotheque.ajouter_livre(livre4)

bibliotheque.emprunter_livre("676767")
bibliotheque.emprunter_livre("696969")

bibliotheque.affiche_statistiques()




