class Produit:
    def __init__(self, code_ref: str, libelle_brut: str, prix_initial, qte_initiale):
        self.__code = str(code_ref)          # champ privé direct
        self.libelle = libelle_brut          # ⇦ appelle le setter libelle
        self.prix = prix_initial             # ⇦ appelle le setter prix
        self.quantite = qte_initiale         # ⇦ appelle le setter quantite

    # --- propriétés ---
    @property
    def code(self) -> str:
        return self.__code

    @property
    def libelle(self) -> str:
        return self.__libelle

    @libelle.setter
    def libelle(self, valeur):
        nom = str(valeur).strip()
        if not nom:
            raise ValueError("Libellé vide.")
        self.__libelle = nom

    @property
    def prix(self) -> float:
        return self.__prix

    @prix.setter
    def prix(self, montant):
        self.__prix = max(0.0, float(montant))

    @property
    def quantite(self) -> int:
        return self.__quantite

    @quantite.setter
    def quantite(self, q):
        n = int(q)
        if n < 0:
            n = 0
        self.__quantite = n

    def __repr__(self):
        return f"Produit(code={self.__code}, libelle={self.__libelle!r}, prix={self.__prix:.2f}, qte={self.__quantite})"


# Exemple d'usage (les noms du constructeur ≠ noms des attributs/propriétés)
p = Produit(code_ref="A42", libelle_brut="  Clavier  ", prix_initial="39.9", qte_initiale=5)
print(p)  # Produit(code=A42, libelle='Clavier', prix=39.90, qte=5)
