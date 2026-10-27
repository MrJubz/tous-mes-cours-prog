class CompteBancaire:
    def __init__(self, numero, titulaire, solde=0.0, taux_interet=1.0):
        self.numero = numero
        self.titulaire = titulaire
        self.solde = solde
        self.taux_interet = taux_interet

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, valeur):
        if not isinstance(valeur, int) or valeur <= 0:
            raise ValueError("Le numéro doit être un entier positif.")
        self.__numero = valeur

    @property
    def titulaire(self):
        return self.__titulaire

    @titulaire.setter
    def titulaire(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le titulaire ne peut pas être vide.")
        self.__titulaire = valeur.strip()

    @property
    def solde(self):
        return self.__solde

    @solde.setter
    def solde(self, valeur):
        # Attention : « if not valeur » refuserait 0, alors qu'un solde de 0 $ est valide
        if not isinstance(valeur, (int, float)) or valeur < 0:
            raise ValueError("Le solde doit être un nombre ≥ 0.")
        self.__solde = float(valeur)

    @property
    def taux_interet(self):
        return self.__taux_interet

    @taux_interet.setter
    def taux_interet(self, valeur):
        if not isinstance(valeur, (int, float)) or not 0 <= valeur <= 20:
            raise ValueError("Le taux d'intérêt doit être entre 0 et 20 %.")
        self.__taux_interet = float(valeur)

    def deposer(self, montant):
        if montant <= 0:
            raise ValueError("Le montant doit être positif.")
        self.__solde += montant

    def retirer(self, montant):
        if montant <= 0:
            raise ValueError("Le montant doit être positif.")
        if montant > self.__solde:
            raise ValueError("Solde insuffisant pour ce retrait.")
        self.__solde -= montant

    def calculer_interet(self):
        return self.__solde * self.__taux_interet / 100

    def __str__(self):
        return (f"Compte {self.numero} de {self.titulaire} : {self.solde:.2f} $ "
                f"(taux {self.taux_interet} %)")


if __name__ == "__main__":
    compte = CompteBancaire(100, "Alice", 1500, 2.5)
    compte.deposer(200)
    compte.retirer(50)
    print(compte)
    print("Intérêts :", compte.calculer_interet())

    vide = CompteBancaire(101, "Bob")  # solde 0 accepté
    print(vide)

    try:
        vide.retirer(10)
    except ValueError as e:
        print("Erreur attendue :", e)
