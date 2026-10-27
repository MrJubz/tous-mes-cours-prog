class Document:
    def __init__(self, id, titre, annee):
        self.__id = str(id)
        self.titre = titre
        self.annee = annee
        self.__disponible = True

    @property
    def id(self):
        return self.__id

    @property
    def titre(self):
        return self.__titre

    @titre.setter
    def titre(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le titre ne peut pas être vide.")
        self.__titre = valeur.strip()

    @property
    def annee(self):
        return self.__annee

    @annee.setter
    def annee(self, valeur):
        if not isinstance(valeur, int) or valeur <= 0:
            raise ValueError("L'année doit être un entier positif.")
        self.__annee = valeur

    @property
    def disponible(self):
        return self.__disponible

    def emprunter(self):
        if not self.__disponible:
            raise ValueError(f"« {self.titre} » est déjà emprunté.")
        self.__disponible = False

    def rendre(self):
        if self.__disponible:
            raise ValueError(f"« {self.titre} » est déjà disponible.")
        self.__disponible = True

    def __str__(self):
        etat = "disponible" if self.__disponible else "emprunté"
        # type(self).__name__ donne "Livre", "Magazine" ou "DVD" selon l'objet réel
        return f"[{type(self).__name__} {self.id}] {self.titre} ({self.annee}) - {etat}"


class Livre(Document):
    def __init__(self, id, titre, annee, auteur, nb_pages):
        super().__init__(id, titre, annee)
        self.auteur = auteur
        self.nb_pages = nb_pages

    @property
    def auteur(self):
        return self.__auteur

    @auteur.setter
    def auteur(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("L'auteur ne peut pas être vide.")
        self.__auteur = valeur.strip()

    @property
    def nb_pages(self):
        return self.__nb_pages

    @nb_pages.setter
    def nb_pages(self, valeur):
        if not isinstance(valeur, int) or valeur < 1:
            raise ValueError("Le nombre de pages doit être un entier ≥ 1.")
        self.__nb_pages = valeur

    def __str__(self):
        return super().__str__() + f" | {self.auteur}, {self.nb_pages} p."


class Magazine(Document):
    def __init__(self, id, titre, annee, numero):
        super().__init__(id, titre, annee)
        self.numero = numero

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, valeur):
        if not isinstance(valeur, int) or valeur < 1:
            raise ValueError("Le numéro doit être un entier ≥ 1.")
        self.__numero = valeur

    def __str__(self):
        return super().__str__() + f" | n° {self.numero}"


class DVD(Document):
    def __init__(self, id, titre, annee, duree_min):
        super().__init__(id, titre, annee)
        self.duree_min = duree_min

    @property
    def duree_min(self):
        return self.__duree_min

    @duree_min.setter
    def duree_min(self, valeur):
        if not isinstance(valeur, int) or valeur <= 0:
            raise ValueError("La durée doit être un entier > 0.")
        self.__duree_min = valeur

    def __str__(self):
        return super().__str__() + f" | {self.duree_min} min"


class Adherent:
    def __init__(self, id, nom):
        self.__id = str(id)
        self.nom = nom
        self.__emprunts = []
        self.__journal = []

    @property
    def id(self):
        return self.__id

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        self.__nom = valeur.strip()

    @property
    def borrowing(self):
        return list(self.__emprunts)  # une copie : modifier la copie ne touche pas la vraie liste

    @property
    def log(self):
        return list(self.__journal)

    def limite_emprunts(self):
        return 3

    def peut_emprunter_magazine(self):
        for doc in self.__emprunts:
            if isinstance(doc, Magazine):
                return False
        return True

    def emprunter(self, doc):
        if not isinstance(doc, Document):
            raise TypeError("On ne peut emprunter qu'un Document.")
        if not doc.disponible:
            raise ValueError(f"« {doc.titre} » n'est pas disponible.")
        if len(self.__emprunts) >= self.limite_emprunts():
            raise ValueError(f"{self.nom} a atteint sa limite de {self.limite_emprunts()} emprunts.")
        if isinstance(doc, Magazine) and not self.peut_emprunter_magazine():
            raise ValueError(f"{self.nom} ne peut pas emprunter plus d'un magazine à la fois.")
        doc.emprunter()
        self.__emprunts.append(doc)
        self.__journal.append(f"Emprunt : {doc.titre}")

    def rendre(self, doc):
        if doc not in self.__emprunts:
            raise ValueError(f"{self.nom} n'a pas emprunté « {doc.titre} ».")
        doc.rendre()
        self.__emprunts.remove(doc)
        self.__journal.append(f"Retour : {doc.titre}")

    def __str__(self):
        return f"{type(self).__name__} {self.nom} ({self.id}) - {len(self.__emprunts)} emprunt(s)"


class AdherentPremium(Adherent):
    # Seules les règles qui changent sont redéfinies ; tout le reste est hérité.
    # (Ne pas utiliser self.__emprunts ici : le name mangling chercherait _AdherentPremium__emprunts)
    def limite_emprunts(self):
        return 5

    def peut_emprunter_magazine(self):
        return True


class Bibliotheque:
    def __init__(self):
        self.__documents = []

    @property
    def documents(self):
        return list(self.__documents)

    def ajouter_document(self, doc):
        if not isinstance(doc, Document):
            raise TypeError("On ne peut ajouter que des objets Document.")
        self.__documents.append(doc)

    def rechercher_par_titre(self, mot):
        mot = mot.lower()
        return [doc for doc in self.__documents if mot in doc.titre.lower()]


def essayer(action, *args):
    try:
        action(*args)
        print("  OK")
    except (ValueError, TypeError) as e:
        print("  Refusé :", e)


if __name__ == "__main__":
    livre = Livre("L1", "Python avancé", 2022, "Guido", 350)
    mag1 = Magazine("M1", "Science & Vie", 2025, 1290)
    mag2 = Magazine("M2", "Québec Science", 2025, 45)
    dvd = DVD("D1", "Le Python sacré", 2019, 95)

    biblio = Bibliotheque()
    for doc in (livre, mag1, mag2, dvd):
        biblio.ajouter_document(doc)

    alice = Adherent("A1", "Alice")
    bob = AdherentPremium("A2", "Bob")

    print("Alice emprunte un livre :")
    essayer(alice.emprunter, livre)
    print("Alice emprunte un 1er magazine :")
    essayer(alice.emprunter, mag1)
    print("Alice emprunte un 2e magazine (interdit pour un standard) :")
    essayer(alice.emprunter, mag2)
    print("Bob (premium) emprunte le livre déjà pris par Alice :")
    essayer(bob.emprunter, livre)
    print("Bob emprunte 1 magazine + 1 DVD :")
    essayer(bob.emprunter, mag2)
    essayer(bob.emprunter, dvd)
    print("Alice rend le livre :")
    essayer(alice.rendre, livre)
    print("Alice rend encore le livre :")
    essayer(alice.rendre, livre)

    print()
    print(alice, alice.log)
    print(bob, [d.titre for d in bob.borrowing])
    print("Recherche 'python' :")
    for doc in biblio.rechercher_par_titre("python"):
        print("  ", doc)
