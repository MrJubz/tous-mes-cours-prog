class Personne:
    def __init__(self, nom, age):
        self.__nom = nom
        self.__age = age
        
    @property
    def nom(self):
        return self.__nom

    @property
    def age(self):
        return self.__age

    
    def __str__(self):
        return f"Nom: {self.nom}, Âge: {self.age}"

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
        Personne.__init__(self, nom, age)  # Appelle explicitement le constructeur de Personne
        Employe.__init__(self, salaire)   # Appelle explicitement le constructeur de Employe
        self.__universite = universite
    
    def __str__(self):
        return f"Etudiant-Employé: {self.nom}, Âge: {self.age}, Salaire: {self.salaire}, Université: {self.__universite}"

# Test
e1 = EtudiantEmploye("GARRAOUI", 25, 2000, "Université de Québec")
print(e1)  # Affiche: Etudiant-Employé: GARRAOUI, Âge: 25, Salaire: 2000, Université: Université de Québec
print(e1.travailler())  # Affiche: Je travaille

