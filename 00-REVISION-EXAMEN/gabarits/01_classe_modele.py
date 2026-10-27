"""Gabarit : classe « modèle » (encapsulation + validation + méthodes magiques)."""


class Etudiant:
    PROGRAMMES = {"Informatique": 420, "Sciences": 200, "Arts": 500}  # constante de classe
    nb_crees = 0  # attribut de classe : partagé par tous les objets

    def __init__(self, nom, age, programme, moyenne=None):
        # Toujours passer par les setters dans __init__ → la validation s'applique dès la création
        self.nom = nom
        self.age = age
        self.programme = programme
        self.moyenne = moyenne  # paramètre facultatif (None par défaut)
        Etudiant.nb_crees += 1

    # ---------- nom : texte non vide ----------
    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        self.__nom = valeur.strip()

    # ---------- age : entier dans une plage (accepte aussi le texte d'un Entry) ----------
    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, valeur):
        try:
            valeur = int(valeur)
        except (ValueError, TypeError):
            raise ValueError("L'âge doit être un entier.")
        if not 0 < valeur < 120:
            raise ValueError("L'âge doit être entre 1 et 119.")
        self.__age = valeur

    # ---------- programme : doit exister dans le dictionnaire ----------
    @property
    def programme(self):
        return self.__programme

    @programme.setter
    def programme(self, valeur):
        if valeur not in self.PROGRAMMES:
            raise ValueError(f"Programme inconnu. Choix : {', '.join(self.PROGRAMMES)}")
        self.__programme = valeur

    # ---------- moyenne : float facultatif ----------
    @property
    def moyenne(self):
        return self.__moyenne

    @moyenne.setter
    def moyenne(self, valeur):
        if valeur is None or valeur == "":
            self.__moyenne = None
            return
        try:
            valeur = float(valeur)
        except (ValueError, TypeError):
            raise ValueError("La moyenne doit être un nombre.")
        if not 0 <= valeur <= 100:
            raise ValueError("La moyenne doit être entre 0 et 100.")
        self.__moyenne = valeur

    # ---------- lecture seule (pas de setter) ----------
    @property
    def code_programme(self):
        return self.PROGRAMMES[self.programme]

    # ---------- méthodes « métier » ----------
    def est_en_reussite(self):
        return self.moyenne is not None and self.moyenne >= 60

    # ---------- méthodes magiques ----------
    def __str__(self):  # print(objet), str(objet), f"{objet}"
        moy = f"{self.moyenne:.1f}" if self.moyenne is not None else "—"
        return f"{self.nom} ({self.age} ans) - {self.programme} - moyenne {moy}"

    def __repr__(self):  # affichage dans une liste, console
        return f"Etudiant({self.nom!r}, {self.age}, {self.programme!r}, {self.moyenne})"

    def __eq__(self, other):  # ==
        return isinstance(other, Etudiant) and self.nom == other.nom and self.age == other.age

    def __lt__(self, other):  # <  (permet aussi sorted() et min()/max())
        if not isinstance(other, Etudiant):
            raise TypeError("On ne compare qu'avec un Etudiant.")
        return self.age < other.age

    # ---------- conversion pour JSON / CSV ----------
    def to_dict(self):
        return {"nom": self.nom, "age": self.age, "programme": self.programme, "moyenne": self.moyenne}

    @classmethod
    def from_dict(cls, d):
        return cls(d["nom"], d["age"], d["programme"], d.get("moyenne"))


class PersonneGetSet:
    """Variante « Java » demandée au cours 1 : get_/set_ au lieu de @property."""

    def __init__(self, nom, age):
        self.__nom = nom
        self.set_age(age)

    def get_nom(self):
        return self.__nom

    def get_age(self):
        return self.__age

    def set_age(self, valeur):
        if valeur < 0:
            raise ValueError("L'âge ne peut pas être négatif.")
        self.__age = valeur


if __name__ == "__main__":
    a = Etudiant("Alice", "20", "Informatique", "85.5")  # les textes sont convertis par les setters
    b = Etudiant("Bob", 18, "Arts")
    print(a)
    print(repr(b))
    print("a < b ?", a < b)
    print("Trié par âge :", sorted([a, b]))
    print("Dict :", a.to_dict())
    print("Recréé :", Etudiant.from_dict(a.to_dict()))
    print("Objets créés :", Etudiant.nb_crees)

    try:
        Etudiant("", 20, "Arts")
    except ValueError as e:
        print("Erreur attendue :", e)

    try:
        a.age = -5
    except ValueError as e:
        print("Erreur attendue :", e)

    # name mangling : __age devient _Etudiant__age (accès possible mais à ne pas faire)
    print(a._Etudiant__age)
