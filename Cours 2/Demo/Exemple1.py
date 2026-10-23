class Personne:
    def __init__(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom

    def se_presenter(self):
        return f"Je m'appelle {self.prenom} {self.nom}."

    def parler(self, message):
        return f"{self.prenom} dit : '{message}'"

class Directeur(Personne):
    def __init__(self, nom, prenom, departement):
        super().__init__(nom, prenom)
        self.departement = departement

    def diriger(self):
        return f"{self.prenom} {self.nom} dirige le département {self.departement}."

    def se_presenter(self):
        return f"Je suis le directeur {self.prenom} {self.nom}, responsable du département {self.departement}."


class Employe(Personne):
    def __init__(self, nom, prenom, poste):
        super().__init__(nom, prenom)
        self.poste = poste

    def travailler(self):
        return f"{self.prenom} travaille en tant que {self.poste}."

    def se_presenter(self):
        return f"Je suis {self.prenom} {self.nom}, employé au poste de {self.poste}."

class Client(Personne):
    def __init__(self, nom, prenom, numero_client):
        super().__init__(nom, prenom)
        self.numero_client = numero_client

    def acheter(self):
        return f"Le client {self.prenom} {self.nom} (n°{self.numero_client}) effectue un achat."

    def se_presenter(self):
        return f"Je suis {self.prenom} {self.nom}, client n°{self.numero_client}."

if __name__ == "__main__":
    p = Personne("Martin", "Alice")
    d = Directeur("Durand", "Paul", "Informatique")
    e = Employe("Lefevre", "Sophie", "Développeuse")
    c = Client("Bernard", "Luc", 1023)

    print(p.se_presenter())
    print(d.se_presenter())
    print(e.travailler())
    print(c.acheter())
