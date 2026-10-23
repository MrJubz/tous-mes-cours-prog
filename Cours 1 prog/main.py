class CompteBanquaire:
    def __init__(self, numero, titulaire, solde, taux_interet):
        self.numero = numero
        self.titulaire = titulaire
        self.solde = solde
        self.taux_interet = taux_interet

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, nouveau_numero):
        if not nouveau_numero or nouveau_numero < 0:
            raise ValueError("numero ne peut pas etre vide")
        self.__numero = nouveau_numero

    @property
    def titulaire(self):
        return self.__titulaire


    @titulaire.setter
    def titulaire(self, nouveau_titulaire):
        if not nouveau_titulaire:
            raise ValueError("titulaire ne peut pas etre vide")
        self.__titulaire = nouveau_titulaire

    @property
    def solde(self):
        return self.__solde

    @solde.setter
    def solde(self, nouveau_solde):
        if not nouveau_solde or nouveau_solde < 0:
            raise ValueError("solde ne peut pas etre plus petit que 0")
        self.__solde = nouveau_solde

    @property
    def taux_interet(self):
        return self.__taux_interet

    @taux_interet.setter
    def taux_interet(self, nouveau_taux_interet):
        if not 0 < nouveau_taux_interet < 20:
            raise ValueError("taux d`interet doit être compris entre 0 et 20")
        self.__taux_interet = nouveau_taux_interet

    def deposer(self, montant):
        if montant < 0: raise ValueError("montant doit etre positif")
        self.__solde += montant

    def retirer(self, montant):
        if montant < 0: raise ValueError("montant doit etre positif")
        if self.__solde - montant < 0: raise ValueError("Vous n'avez pas assez pour ce retrait")
        self.__solde -= montant

    def calculer_interet(self):
        return self.__solde * (self.__taux_interet / 100)

    def afficher_info(self):
        print(f"le compte de {self.__titulaire} avec le numero de compte {self.__numero} a un solde de {self.__solde} et possede un taux dinteret de {self.__taux_interet}")


if __name__ == '__main__':
    test = CompteBanquaire(100, "Alice", 1500, 2.5)
    test.afficher_info()

