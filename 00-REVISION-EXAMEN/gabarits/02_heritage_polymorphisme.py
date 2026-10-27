"""Gabarit : héritage simple, multi-niveaux, multiple, redéfinition et polymorphisme."""


class Personne:
    def __init__(self, nom, age):
        self.__nom = nom  # privé : les classes filles doivent passer par la property
        self._age = age   # protégé (convention) : les classes filles peuvent l'utiliser

    @property
    def nom(self):
        return self.__nom

    def se_presenter(self):
        return f"Je m'appelle {self.nom}."

    def __str__(self):
        return f"{self.nom}, {self._age} ans"


# ---------- Héritage simple + redéfinition (overriding) ----------
class Stagiaire(Personne):
    def __init__(self, nom, age, num_inscription):
        super().__init__(nom, age)  # 1re façon : super() sans self
        self.__num = num_inscription

    @property
    def num_inscription(self):
        return self.__num

    def se_presenter(self):  # même nom que dans Personne → redéfinie
        return super().se_presenter() + f" Je suis stagiaire n° {self.__num}."


# ---------- Multi-niveaux : StagiaireInternational → Stagiaire → Personne ----------
class StagiaireInternational(Stagiaire):
    def __init__(self, nom, age, num_inscription, pays):
        super().__init__(nom, age, num_inscription)
        self.__pays = pays

    def __str__(self):
        return super().__str__() + f" ({self.__pays})"


# ---------- Héritage multiple ----------
class Employe:
    def __init__(self, salaire):
        self.__salaire = salaire

    @property
    def salaire(self):
        return self.__salaire

    def travailler(self):
        return "Je travaille"


class EtudiantEmploye(Personne, Employe):
    def __init__(self, nom, age, salaire, universite):
        Personne.__init__(self, nom, age)  # 2e façon : NomClasse.__init__(self, ...) — obligatoire en multiple
        Employe.__init__(self, salaire)
        self.__universite = universite

    def __str__(self):
        # self.__age n'existe pas ici (il est privé à Personne) → on utilise les properties / _age
        return f"{self.nom}, {self._age} ans, {self.salaire} $, {self.__universite}"


# ---------- « Surcharge » en Python : paramètres par défaut ----------
class Calcul:
    def additionner(self, a, b=0, c=0):
        return a + b + c


if __name__ == "__main__":
    groupe = [
        Personne("Alice", 30),
        Stagiaire("Bob", 21, 1122),
        StagiaireInternational("Chen", 23, 3344, "Canada"),
    ]
    # Polymorphisme : même appel, comportement différent selon la classe réelle
    for p in groupe:
        print(type(p).__name__, "->", p.se_presenter(), "|", p)

    ee = EtudiantEmploye("Dana", 25, 2000, "UQAM")
    print(ee, "|", ee.travailler())

    print(isinstance(groupe[2], Personne))     # True : un StagiaireInternational EST une Personne
    print(issubclass(Stagiaire, Personne))     # True
    print(EtudiantEmploye.__mro__)             # ordre de recherche des méthodes en héritage multiple
    print(Calcul().additionner(1), Calcul().additionner(1, 2, 3))
