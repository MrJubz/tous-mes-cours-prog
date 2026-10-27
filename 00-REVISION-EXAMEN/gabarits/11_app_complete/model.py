"""Modèle : aucune ligne de tkinter ici. Toute la validation est dans les setters."""


class Article:
    CATEGORIES = {"Alimentation": 0.0, "Électronique": 0.14975, "Vêtements": 0.14975}  # catégorie → taux de taxe

    def __init__(self, nom, categorie, quantite, prix):
        self.nom = nom
        self.categorie = categorie
        self.quantite = quantite
        self.prix = prix

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, valeur):
        valeur = str(valeur).strip()
        if not valeur:
            raise ValueError("Le nom est obligatoire.")
        self.__nom = valeur

    @property
    def categorie(self):
        return self.__categorie

    @categorie.setter
    def categorie(self, valeur):
        if valeur not in self.CATEGORIES:
            raise ValueError(f"Catégorie invalide : {valeur}.")
        self.__categorie = valeur

    @property
    def quantite(self):
        return self.__quantite

    @quantite.setter
    def quantite(self, valeur):
        try:
            valeur = int(valeur)
        except (ValueError, TypeError):
            raise ValueError("La quantité doit être un entier.")
        if valeur < 0:
            raise ValueError("La quantité ne peut pas être négative.")
        self.__quantite = valeur

    @property
    def prix(self):
        return self.__prix

    @prix.setter
    def prix(self, valeur):
        try:
            valeur = float(str(valeur).replace(",", "."))  # accepte « 2,50 »
        except (ValueError, TypeError):
            raise ValueError("Le prix doit être un nombre.")
        if valeur < 0:
            raise ValueError("Le prix ne peut pas être négatif.")
        self.__prix = valeur

    def total(self):
        return self.quantite * self.prix * (1 + self.CATEGORIES[self.categorie])

    def to_dict(self):
        return {"nom": self.nom, "categorie": self.categorie, "quantite": self.quantite, "prix": self.prix}

    @classmethod
    def from_dict(cls, d):
        return cls(d["nom"], d["categorie"], d["quantite"], d["prix"])

    def __str__(self):
        return f"{self.nom} ({self.categorie}) × {self.quantite} à {self.prix:.2f} $"


class Inventaire:
    def __init__(self):
        self.__articles = []

    @property
    def articles(self):
        return list(self.__articles)

    def ajouter(self, article):
        if not isinstance(article, Article):
            raise TypeError("On ne peut ajouter qu'un Article.")
        if self.rechercher(article.nom) is not None:
            raise ValueError(f"« {article.nom} » existe déjà.")
        self.__articles.append(article)

    def remplacer(self, index, article):
        self.__articles[index] = article

    def supprimer(self, index):
        del self.__articles[index]

    def rechercher(self, nom):
        for a in self.__articles:
            if a.nom.lower() == nom.lower():
                return a
        return None

    def vider(self):
        self.__articles.clear()

    def total_par_categorie(self):
        totaux = {c: 0.0 for c in Article.CATEGORIES}
        for a in self.__articles:
            totaux[a.categorie] += a.total()
        return totaux

    def valeur_totale(self):
        return sum(a.total() for a in self.__articles)
