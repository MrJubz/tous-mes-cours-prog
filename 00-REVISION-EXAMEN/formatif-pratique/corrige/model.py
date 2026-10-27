"""Modèle : aucune ligne de tkinter ici. Toute la validation est dans les setters."""
import numpy as np


class MatriculeDejaUtilise(ValueError):
    # Hérite de ValueError : un seul « except ValueError » dans la vue attrape aussi celle-ci
    pass


class Etudiant:
    PROGRAMMES = ("Informatique", "Sciences de la nature", "Sciences humaines")
    PONDERATIONS = {"tp1": 0.25, "tp2": 0.25, "examen": 0.50}
    SEUIL = 60

    def __init__(self, matricule, nom, programme, tp1, tp2, examen):
        matricule = str(matricule).strip()
        if len(matricule) != 7 or not matricule.isdigit():
            raise ValueError(f"Le matricule doit contenir exactement 7 chiffres (reçu « {matricule} »).")
        self.__matricule = matricule  # pas de setter : lecture seule
        self.nom = nom
        self.programme = programme
        self.tp1 = tp1
        self.tp2 = tp2
        self.examen = examen

    @staticmethod
    def _valider_note(valeur, champ):
        # Un seul « _ » : la classe fille peut l'appeler (avec « __ » le name mangling la cacherait)
        try:
            valeur = float(str(valeur).replace(",", "."))
        except ValueError:
            raise ValueError(f"{champ} doit être un nombre.")
        if not 0 <= valeur <= 100:
            raise ValueError(f"{champ} doit être entre 0 et 100 (reçu {valeur:g}).")
        return valeur

    @property
    def matricule(self):
        return self.__matricule

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
    def programme(self):
        return self.__programme

    @programme.setter
    def programme(self, valeur):
        if valeur not in self.PROGRAMMES:
            raise ValueError(f"Programme inconnu : « {valeur} ».")
        self.__programme = valeur

    @property
    def tp1(self):
        return self.__tp1

    @tp1.setter
    def tp1(self, valeur):
        self.__tp1 = self._valider_note(valeur, "TP1")

    @property
    def tp2(self):
        return self.__tp2

    @tp2.setter
    def tp2(self, valeur):
        self.__tp2 = self._valider_note(valeur, "TP2")

    @property
    def examen(self):
        return self.__examen

    @examen.setter
    def examen(self, valeur):
        self.__examen = self._valider_note(valeur, "Examen")

    def note_examen_retenue(self):
        return self.examen

    def moyenne(self):
        p = self.PONDERATIONS
        return self.tp1 * p["tp1"] + self.tp2 * p["tp2"] + self.note_examen_retenue() * p["examen"]

    def statut(self):
        return "Réussite" if self.moyenne() >= self.SEUIL else "Échec"

    def to_dict(self):
        return {"type": "regulier", "matricule": self.matricule, "nom": self.nom, "programme": self.programme,
                "tp1": self.tp1, "tp2": self.tp2, "examen": self.examen}

    def __str__(self):
        return f"{self.matricule} {self.nom} ({self.programme}) : {self.moyenne():.1f} %"

    def __repr__(self):
        return f"{type(self).__name__}({self.matricule!r}, {self.nom!r})"

    def __eq__(self, autre):
        return isinstance(autre, Etudiant) and self.matricule == autre.matricule

    def __lt__(self, autre):
        return self.moyenne() < autre.moyenne()


class EtudiantReprise(Etudiant):
    def __init__(self, matricule, nom, programme, tp1, tp2, examen, ancien_examen):
        super().__init__(matricule, nom, programme, tp1, tp2, examen)
        self.ancien_examen = ancien_examen

    @property
    def ancien_examen(self):
        return self.__ancien_examen

    @ancien_examen.setter
    def ancien_examen(self, valeur):
        self.__ancien_examen = self._valider_note(valeur, "Ancien examen")

    def note_examen_retenue(self):
        return max(self.examen, self.ancien_examen)

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "reprise"
        d["ancien_examen"] = self.ancien_examen
        return d

    def __str__(self):
        return super().__str__() + " [reprise]"


def etudiant_depuis_dict(d):
    """Recrée le bon type d'objet à partir d'une ligne JSON ou CSV. Lève ValueError si la ligne est invalide."""
    if not isinstance(d, dict):
        raise ValueError("la ligne n'est pas un objet.")
    try:
        args = (d["matricule"], d["nom"], d["programme"], d["tp1"], d["tp2"], d["examen"])
        type_etudiant = d.get("type") or "regulier"
        if type_etudiant == "regulier":
            return Etudiant(*args)
        if type_etudiant == "reprise":
            return EtudiantReprise(*args, d["ancien_examen"])
    except KeyError as e:
        raise ValueError(f"champ manquant : {e.args[0]}.")
    raise ValueError(f"type inconnu : « {type_etudiant} ».")


class Groupe:
    def __init__(self):
        self.__etudiants = []

    @property
    def etudiants(self):
        return list(self.__etudiants)

    def __len__(self):
        return len(self.__etudiants)

    def trouver(self, matricule):
        for e in self.__etudiants:
            if e.matricule == matricule:
                return e
        return None

    def ajouter(self, etudiant):
        if not isinstance(etudiant, Etudiant):
            raise TypeError("On ne peut ajouter qu'un Etudiant.")
        if etudiant in self.__etudiants:  # « in » utilise __eq__ : compare les matricules
            raise MatriculeDejaUtilise(f"Le matricule {etudiant.matricule} existe déjà.")
        self.__etudiants.append(etudiant)

    def supprimer(self, matricule):
        etudiant = self.trouver(matricule)
        if etudiant is None:
            raise ValueError(f"Aucun étudiant avec le matricule {matricule}.")
        self.__etudiants.remove(etudiant)

    def remplacer(self, matricule, nouvel_etudiant):
        for i, e in enumerate(self.__etudiants):
            if e.matricule == matricule:
                self.__etudiants[i] = nouvel_etudiant
                return
        raise ValueError(f"Aucun étudiant avec le matricule {matricule}.")

    def vider(self):
        self.__etudiants.clear()

    def rechercher(self, texte):
        texte = texte.strip().lower()
        return [e for e in self.__etudiants if texte in e.nom.lower() or texte in e.matricule]

    def statistiques(self):
        if not self.__etudiants:
            return None
        m = np.array([e.moyenne() for e in self.__etudiants])
        return {"n": m.size, "moyenne": m.mean(), "mediane": np.median(m), "ecart_type": m.std(),
                "min": m.min(), "max": m.max(), "reussite": np.mean(m >= Etudiant.SEUIL) * 100}

    def moyennes_par_programme(self):
        resultat = {}
        for programme in Etudiant.PROGRAMMES:
            m = [e.moyenne() for e in self.__etudiants if e.programme == programme]
            if m:
                resultat[programme] = float(np.mean(m))
        return resultat
