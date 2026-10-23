

class Document:
    def __init__(self, id, titre, annee):
        self.__id = id
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
    def titre(self, nv_titre):
        if not isinstance(nv_titre, str) or not nv_titre.strip():
            raise ValueError("le titre ne peut pas etre vide")
        self.__titre = nv_titre

    @property
    def annee(self):
        return self.__annee

    @annee.setter
    def annee(self, nv_annee):
        if not isinstance(nv_annee, int):
            raise TypeError("L'annee doit etre un entier")

        if nv_annee < 0:
            raise ValueError("L'annee ne peut pas etre negatif.")
        self.__annee = nv_annee

    @property
    def disponible(self):
        return self.__disponible

    def emprunter(self):
        if not self.__disponible:
            raise ValueError("Le livre est deja emprunter")
        self.__disponible = False

    def rendre(self):
        if self.__disponible:
            raise ValueError("Le livre est deja rendu")
        self.__disponible = True

    def __str__(self):
        dispo = "disponible"
        if not self.__disponible:
            dispo = "indisponible"
        return (f"le titre du document est {self.__titre}/n"
                f"l'annee du livre est {self.__annee}/n"
                f"l'id du livre est {self.__id}/n"
                f"le livre est {dispo}")


class Livre(Document):
    def __init__(self, id, titre, annee, auteur, nb_page):
        super().__init__(id, titre, annee)
        self.auteur = auteur
        self.nb_page = nb_page

    @property
    def auteur(self):
        return self.__auteur

    @auteur.setter
    def auteur(self, nv_auteur):
        if not isinstance(nv_auteur, str) or not nv_auteur.strip():
            raise ValueError("L'auteur ne doit pas etre vide")
        self.__auteur = nv_auteur

    @property
    def nb_page(self):
        return self.__nb_page

    @nb_page.setter
    def nb_page(self, nv_nb_page):
        if not isinstance(nv_nb_page, int):
            raise TypeError("Le nombre de page doit etre un entier")

        if nv_nb_page < 1:
            raise ValueError("Le nombre de page ne peut pas etre plus petit que 1.")
        self.__nb_page = nv_nb_page


class Magazine(Document):
    def __init__(self, id, titre, annee, numero):
        super().__init__(id, titre, annee)
        self.numero = numero

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, nv_numero):
        if not isinstance(nv_numero, int):
            raise TypeError("Le numero doit etre un entier")

        if nv_numero < 1:
            raise ValueError("Le numero ne peut pas etre plus petit que 1.")
        self.__numero = nv_numero


class DVD(Document):
    def __init__(self, id, titre, annee, duree_min):
        super().__init__(id, titre, annee)
        self.__duree_min = duree_min

        if not isinstance(duree_min, (int, float)):
            raise TypeError("La duree doit etre un entier.")
        if duree_min < 1:
            raise ValueError("La duree ne peut pas etre plus petite que 1.")


class Adherent:
    def __init__(self, id, nom):
        self.__id = id
        self.nom = nom
        self.__emprunt = []
        self.__journal = []

    @property
    def id(self):
        return self.__id

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, nv_nom):
        if not isinstance(nv_nom, str) or not nv_nom.strip():
            raise ValueError("le nom ne peut pas etre vide")
        self.__nom = nv_nom

    @property
    def borrowing(self):
        return self.__emprunt

    @property
    def log(self):
        return self.__journal

    def limite_emprunts(self, nb_max=3):
        nb_emprunt = len(self.__emprunt)
        if nb_emprunt >= nb_max:
            return 0
        return nb_max - nb_emprunt

    def emprunter(self, doc: Document):
        if not isinstance(doc, Document):
            raise TypeError()
        if not doc.disponible:
            raise ValueError("Ce document est indisponible")
        if self.limite_emprunts() < 1:
            raise ValueError("Vous avez ateint votre max d'emprunt")
        doc.emprunter()
        self.__emprunt.append(doc)
        self.__journal.append(f"le doc {doc} a ete emprunter")

    def rendre(self, doc: Document):
        if doc.disponible:
            raise ValueError("Ce document est deja rendu")
        doc.rendre()
        self.__emprunt.remove(doc)
        self.__journal.append(f"le doc {doc} a ete rendu")

    def __str__(self):
        nombre_emprunts = len(self.__emprunt)
        return (f"voici les activites de la bibliotheque: {self.__journal}/n"
                f"Le nombre d'emprunt est de {nombre_emprunts}")


class AdherentPremium(Adherent):
    def limite_emprunts(self, nb_max=5):
        nb_emprunt = len(self.__emprunt)
        if nb_emprunt >= nb_max:
            return 0
        return nb_max - nb_emprunt


class Bibliotheque:
    def __init__(self):
        self.__documents = []

    @property
    def documents(self):
        return self.__documents

    def ajouter_document(self, doc: Document):
        if not isinstance(doc, Document):
            raise TypeError()
        self.__documents.append(doc)

    def rechercher_par_titre(self, mot: str):
        doc_trouver = []
        for doc in self.__documents:
            if mot in doc.titre:
                doc_trouver.append(doc)
        return doc_trouver