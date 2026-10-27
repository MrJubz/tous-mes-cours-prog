# Ce qui clochait dans tes exercices

Tes fichiers d'origine dans `Cours X/` n'ont pas été touchés (sauf `Cours 15/corrige.py`, voir plus bas). Les versions corrigées sont dans [exercices-corriges/](exercices-corriges/). Classé du plus grave au plus léger.

## Les vrais bugs (le programme plante ou donne un mauvais résultat)

### Cours 5, bibliothèque de documents ([corrigé](exercices-corriges/cours05_bibliotheque_documents.py))

Le plus gros. `AdherentPremium.limite_emprunts()` faisait `len(self.__emprunt)`. À cause du name mangling, dans la classe `AdherentPremium` ça devient `self._AdherentPremium__emprunt`, qui n'existe pas : **tout emprunt par un adhérent premium plantait** avec `AttributeError`. La correction : la classe fille redéfinit seulement `return 5`, et c'est la classe mère qui compare avec `len(...)`.

Il manquait aussi des morceaux de l'énoncé :
- la règle « pas plus d'un Magazine à la fois pour un adhérent standard » ;
- `borrowing`, `log` et `documents` devaient retourner une **copie** (`list(...)`), pas la vraie liste ;
- la recherche par titre devait ignorer les majuscules (`.lower()` des deux côtés) ;
- `titre` n'était pas `strip()`, `DVD` validait `duree_min` après l'avoir assignée et n'avait pas de property ;
- `rendre()` d'un document jamais emprunté par cet adhérent faisait planter `remove()` ;
- pas de tests à la fin, alors que l'énoncé en demandait (4 documents, 2 adhérents, plusieurs cas).

### Cours 12, to-do avec validation ([corrigé](exercices-corriges/cours12_todo_validation.py))

- Le champ **durée** était branché sur `textvariable=self.tache_var` et le champ **tâche** n'avait aucune variable. Résultat : taper un titre ne réactivait jamais le bouton.
- `"Professionel"` (un seul n) dans `affichage()` alors que la valeur du bouton radio est `"Professionnel"` : tout s'affichait `[Pers]`.
- `[P]` était écrit en dur : toutes les tâches apparaissaient prioritaires.
- L'énoncé voulait le bouton actif seulement si le titre est non vide **et** la durée entre 1 et 480. Ta version vérifiait seulement que les champs n'étaient pas vides.
- Le message disait « entier (positif ou négatif) » alors que c'était 1 à 480, et la couleur rouge restait 5 secondes en plus d'un messagebox. L'énoncé demandait un retour discret : `bell()` + rouge pendant 0,5 s.

### Cours 4, bibliothèque de livres ([corrigé](exercices-corriges/cours04_bibliotheque_livres.py))

- L'énoncé demande un graphique **circulaire** (`plt.pie`), tu avais `plt.bar`.
- La barre « disponible » affichait `len(self.__livres)`, donc le nombre **total** de livres.
- `retourner_livre` sur un livre jamais emprunté faisait quand même `-= 1` : le compteur pouvait devenir négatif. Le corrigé compte directement les livres disponibles au lieu de tenir un compteur.
- `"/n"` au lieu de `"\n"` dans `__str__` (le même bug est au cours 5).
- La validation se faisait après l'assignation des attributs, et il n'y avait pas de setters.

### Cours 9, réservation d'hôtel ([corrigé](exercices-corriges/cours09_reservation_hotel.py))

`label_taxes` et `label_total` étaient tous les deux en `row=4` : le total cachait les taxes. Taper « abc » dans le nombre de nuits faisait planter `int()`. Le calcul lui-même était bon (390 $ / 58,4 $ / 448,4 $ comme dans l'énoncé).

### Cours 11, réservation avec place ([corrigé](exercices-corriges/cours11_reservation_place/))

- Aucun `try/except` dans `reserver()` : un nom vide ou « abc » places fermait l'application au lieu d'afficher le message du setter.
- `nb_place` était validé avec `int()` mais stocké en chaîne (`"3"`), donc il fallait refaire `int()` partout ailleurs. Le corrigé stocke l'entier converti.
- Le dictionnaire s'appelait `INFORMATIONS_CLIENTS` au lieu de `PRIX_ACTIVITES` (nom de l'énoncé), avec « Intelligence artificiel » et « Développement web » mal écrits.
- `effacer()` ne remettait ni l'activité ni le nombre de places.

### Cours 15, gestion de produits ([corrigé](exercices-corriges/cours15_gestion_produits.py))

Ton `Manager.py` était commencé seulement (`import messagebox` au lieu de `from tkinter import messagebox`, pas d'interface). Le corrigé du prof fonctionne, mais :
- `supprimer_produit` retire des éléments de la liste **pendant** qu'il la parcourt, en comparant le texte affiché. Avec trois produits identiques, il en retire deux de la liste mais une seule ligne du tableau : la liste et l'affichage ne correspondent plus. Le corrigé utilise l'index de la ligne (`tree.index`).
- `modifier_produit` supprime le produit et remet ses valeurs dans les champs : si on ne reclique pas sur Ajouter, le produit est perdu. Le corrigé remplit les champs quand on sélectionne une ligne (`<<TreeviewSelect>>`) et « Modifier » remplace sur place.

Le `Cours 15/corrige.py` du repo était une ancienne copie où `sauvegarder_csv` et `sauvegarder_json` étaient vides (`pass`). Il a été remplacé par la version complète que tu m'as donnée.

## Exercices pas finis ou jamais faits

| Exercice | État dans ton repo | Corrigé |
|---|---|---|
| Satisfaction clients (cours 4, Exercice3 du PowerPoint) | absent | [cours04_satisfaction_clients.py](exercices-corriges/cours04_satisfaction_clients.py) |
| Interface 2 Formulaire, Interface 3 PanedWindow (cours 7) | absents | [cours07_formulaire_et_panedwindow.py](exercices-corriges/cours07_formulaire_et_panedwindow.py) |
| Interface 5 Simulateur de compte (cours 7) | absent | [cours07_simulateur_compte.py](exercices-corriges/cours07_simulateur_compte.py) |
| Centre sportif (cours 10) | `calculer`, `inscrire`, `reinitialiser` = `pass` ; les boutons Activité étaient liés à `self.niveau` | [cours10_centre_sportif.py](exercices-corriges/cours10_centre_sportif.py) (ta version finie est dans `Cours 11/20260926015302_Sport.py` et elle marche) |
| Formulaire JSON/CSV (cours 13) | `main.py` abandonné (méthodes vides, références à des champs qui n'existent pas) ; `table.py` est la bonne version | [cours13_formulaire_json_csv.py](exercices-corriges/cours13_formulaire_json_csv.py) |
| Cours 9 `main.py` | début abandonné (deux frames en `row=0, column=1`) | remplacé par l'hôtel |

## Les petites choses

- **Calculatrice (cours 7)** : `calculator.py` est une version cassée (le test `type(value) == int` n'est jamais vrai) ; `20260921230856_calculatrice.py` fonctionne. Le corrigé la refait en grid avec une seule boucle pour les 18 boutons.
- **To-do (cours 7)** : `messagebox.showwarning("veuillez saisir une tache")` n'a qu'un argument (il faut titre + message). L'affichage donnait `[P],Personnel,titre` au lieu de `[P][Pers] titre`. `f"{task["titre"]}"` (mêmes guillemets dedans et dehors) ne marche qu'à partir de Python 3.12 : mets `task['titre']` pour être tranquille sur les ordis du cégep.
- **Compte bancaire (cours 1)** : `if not nouveau_solde or ...` refuse un solde de **0**, parce que `not 0` vaut `True`. Pareil pour `0 < taux < 20` qui refuse un taux de 0.
- **Cours 13 `table.py`** : `messagebox.showwarnings` (avec un s) plante si l'import JSON échoue ; les accents s'affichent « Ã‚ge » parce que le fichier a été réenregistré dans le mauvais encodage ; `json.dump` sans `ensure_ascii=False` écrit `\u00e9` au lieu de « é ».
- **Cours 14 `main.py`** : l'énoncé demande de « mettre à jour le graphique automatiquement selon la sélection », il manquait `combo.bind("<<ComboboxSelected>>", ...)`. Le diagramme en barres avait la légende « sin(x) ». `plt.subplots` dans Tkinter fonctionne, mais `Figure()` (comme dans le PowerPoint) évite qu'une fenêtre Matplotlib séparée reste ouverte.
- **Cours 11 `main.py`** : c'est le fichier exemple de PyCharm, rien à voir avec le cours.
