class Personne:
    def __init__(self, nom, age):
        self._nom = nom
        self._age = age
    
    def __str__(self):
        return f"Nom: {self._nom}, Âge: {self._age}"

class Employe:
    def __init__(self, salaire):
        self._salaire = salaire
    
    
    def travailler(self):
        return "Je travaille"

class EtudiantEmploye(Personne, Employe):
    def __init__(self, nom, age, salaire, universite):
        Personne.__init__(self, nom, age)  # Appelle explicitement le constructeur de Personne
        Employe.__init__(self, salaire)   # Appelle explicitement le constructeur de Employe
        self._universite = universite
    
    def __str__(self):
        return f"Etudiant-Employé: {self._nom}, Âge: {self._age}, Salaire: {self._salaire}, Université: {self._universite}"

# Test
e1 = EtudiantEmploye("Garraoui", 25, 2000, "Université de Québec")
print(e1)  # Affiche: Etudiant-Employé: Garraoui, Âge: 25, Salaire: 2000, Université: Université de Québec
print(e1.travailler())  # Affiche: Je travaille

