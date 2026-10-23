class Personne:
    def __init__(self, nom, age):
        self.__nom = nom  # Attribut privé
        self._age = age
    
    @property
    def nom(self):
        return self.__nom
    
    def __str__(self):
        return f"Nom: {self.__nom}, Âge: {self._age}"

class Stagiaire(Personne):
    def __init__(self, nom, age, num_inscription):
        super().__init__(nom, age)  # Appelle le constructeur de Personne
        self.__num_inscription = num_inscription
    
    @property
    def num_inscription(self):
        return self.__num_inscription
    
    def __str__(self):  # Redéfinition de __str__
        return f"Stagiaire: {self.nom}, Âge: {self._age}, Numéro: {self.__num_inscription}"

# Test
s1 = Stagiaire("Garraoui", 21, 1122)
print(s1)  # Affiche: Stagiaire: Garraoui, Âge: 21, Numéro: 1122
print(s1.nom)  # Affiche: Garraoui (via getter hérité)
