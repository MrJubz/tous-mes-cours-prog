# Révision examen, 420-SF3-RE

Mes notes, mes gabarits et mes exercices corrigés, à ouvrir et copier pendant l'examen. Chaque `.py` se lance tel quel.

## Pendant l'examen

1. Lis l'énoncé et cherche s'il impose un gestionnaire de placement. Pas de consigne → grid. « place() » écrit dans l'énoncé → place. Le détail est dans [GRID-OU-PLACE.md](GRID-OU-PLACE.md).
2. Copie le point de départ le plus proche :
   - une classe avec validation, sans interface : [gabarits/01_classe_modele.py](gabarits/01_classe_modele.py)
   - un formulaire qui calcule un prix : [gabarits/04_fenetre_grid.py](gabarits/04_fenetre_grid.py) (ou [05_fenetre_place.py](gabarits/05_fenetre_place.py))
   - un tableau avec ajouter / modifier / supprimer / JSON / CSV : [gabarits/11_app_complete/](gabarits/11_app_complete/) (modèle et vue séparés)
   - un graphique dans la fenêtre : [gabarits/10_matplotlib_dans_tkinter.py](gabarits/10_matplotlib_dans_tkinter.py)
3. Écris d'abord la classe modèle (setters qui lèvent `ValueError`), ensuite l'interface, ensuite les boutons. Dans chaque bouton, entoure l'appel au modèle d'un `try / except ValueError` qui affiche `messagebox.showerror`. C'est ce qui empêche l'application de fermer quand on tape « abc ».
4. Une syntaxe oubliée : [AIDE-MEMOIRE.md](AIDE-MEMOIRE.md). Le tableau « Erreurs qui reviennent » à la fin est fait pour quand ça plante et que tu ne comprends pas pourquoi.

## Ce qu'il y a dans le dossier

```
00-REVISION-EXAMEN/
├── README.md               ← ce fichier
├── GRID-OU-PLACE.md        ← lequel choisir, comment bien s'en servir
├── AIDE-MEMOIRE.md         ← toute la syntaxe, cours 1 à 15
├── CORRECTIONS.md          ← ce qui clochait dans tes exercices
├── gabarits/               ← points de départ génériques, à copier
│   ├── 01_classe_modele.py           @property, validation, __str__, __lt__, to_dict
│   ├── 02_heritage_polymorphisme.py  super(), multi-niveaux, multiple, redéfinition
│   ├── 03_numpy_matplotlib.py        random, arange/linspace, masques, 6 types de graphiques
│   ├── 04_fenetre_grid.py            formulaire complet en grid
│   ├── 05_fenetre_place.py           même chose en place
│   ├── 06_widgets_et_methodes.py     Entry, Text, Listbox, Treeview, Combobox, Spinbox...
│   ├── 07_evenements.py              command, lambda, bind, bind_all, bind_class, <<virtuels>>
│   ├── 08_validation_erreurs.py      %P, invalidcommand, trace_add, try/except/else/finally
│   ├── 09_json_csv.py                lire/écrire + filedialog
│   ├── 10_matplotlib_dans_tkinter.py Figure + FigureCanvasTkAgg + mise à jour + CSV
│   └── 11_app_complete/              model.py + app.py : tout ensemble
├── exercices-corriges/     ← chaque exercice des cours, corrigé et complet
└── formatif-pratique/      ← un formatif plus gros que celui du prof, pour t'entraîner
    ├── ENONCE.pdf / ENONCE.md        l'énoncé avec l'image de la fenêtre attendue
    ├── donnees/                      un JSON valide et un CSV plein d'erreurs pour tester l'import
    └── corrige/                      model.py + app.py
```

Pour t'entraîner avant l'examen, fais le [formatif de pratique](formatif-pratique/ENONCE.md) sans regarder le corrigé. Il reprend le formatif du cours 15 et ajoute l'héritage, les méthodes magiques, NumPy, la validation au clavier, la recherche, le tri et un graphique.

Les commentaires dans le code sont courts et placés seulement là où une ligne n'est pas évidente. Les explications longues sont dans les `.md`.

`numpy` et `matplotlib` doivent être installés pour les fichiers des cours 4 et 14 et les gabarits 03, 10 et 11 (`pip install numpy matplotlib`). Le reste n'a besoin que de Python.

## Les exercices, cours par cours

Les numéros des PowerPoint ne suivent pas toujours ceux de tes dossiers. Le fichier `Cours__06_...widgets.pptx` porte le titre « Cours #7 » à l'intérieur et correspond à ton dossier `Cours 7`, et `Cours__07_Evenements` correspond à `Cours 8`.

| Dossier | Matière (PowerPoint) | Exercices donnés | Tes fichiers | Corrigé |
|---|---|---|---|---|
| Cours 1 | POO : classe, encapsulation, getters/setters | 1 (refaire avec get_/set_ puis avec @property) | `main.py` (CompteBanquaire) | [cours01_compte_bancaire.py](exercices-corriges/cours01_compte_bancaire.py), [gabarit 01](gabarits/01_classe_modele.py) (`PersonneGetSet`) |
| Cours 2 | Héritage, super(), polymorphisme | 1 (faire marcher le code des diapos 6-8, 2 solutions) | `Demo/` | Les deux solutions sont déjà dans tes démos : `_age` protégé (HeritageSimple) ou properties (HeritageMultiNiveau). [gabarit 02](gabarits/02_heritage_polymorphisme.py) |
| Cours 3 | Méthodes magiques, `__lt__`, `__str__`/`__repr__` | 0 dans le PowerPoint | `main.py` (Monte Carlo, c'est de la matière du cours 4) | [gabarit 01](gabarits/01_classe_modele.py) couvre `__str__`, `__repr__`, `__eq__`, `__lt__` |
| Cours 4 | random, NumPy, Matplotlib | 2 (bibliothèque de livres, satisfaction clients) | `Exercise Gestion d'une bibliothèque/main.py` | [cours04_bibliotheque_livres.py](exercices-corriges/cours04_bibliotheque_livres.py), [cours04_satisfaction_clients.py](exercices-corriges/cours04_satisfaction_clients.py) |
| Cours 5 | (pas de PowerPoint) | 1 (bibliothèque de documents, `Exercice_1.pdf`) | `Gestion bibliothèque.py` | [cours05_bibliotheque_documents.py](exercices-corriges/cours05_bibliotheque_documents.py) |
| Cours 7 | Tkinter : widgets, pack | 8 (5 interfaces dans `Exercices.pdf` + somme, calculatrice, to-do dans `Exercices (1).pdf`) | `calculatrice.py`, `20260921230856_calculatrice.py`, `todo.py`, `Interface 4.py` | [calculatrice](exercices-corriges/cours07_calculatrice_grid.py), [to-do](exercices-corriges/cours07_todo_list.py), [formulaire + panedwindow](exercices-corriges/cours07_formulaire_et_panedwindow.py), [simulateur de compte](exercices-corriges/cours07_simulateur_compte.py). Somme et messagebox : tes versions sont bonnes. |
| Cours 8 | Événements, méthodes des widgets | démos seulement | `Demos/1` à `10` | [gabarit 06](gabarits/06_widgets_et_methodes.py), [gabarit 07](gabarits/07_evenements.py) |
| Cours 9 | grid | 3 (`Exercices (2).pdf` : to-do, hôtel, centre sportif) + « refaire les exercices en grid » | `Exercises/reservation.py`, `Exercises/main.py` | [cours09_reservation_hotel.py](exercices-corriges/cours09_reservation_hotel.py) ; la to-do en grid est dans le corrigé du cours 12 |
| Cours 10 | (suite grid) | le centre sportif | `Centre Sportif Exo/Centre Sport.py` (pas fini) | [cours10_centre_sportif.py](exercices-corriges/cours10_centre_sportif.py) |
| Cours 11 | place | 1 (modèle/vue Réservation, `Exercice (1).pdf`) | `Model.py`, `View.py`, `20260926015302_Sport.py` | [cours11_reservation_place/](exercices-corriges/cours11_reservation_place/) |
| Cours 12 | Validation, gestion d'erreurs | 1 (to-do : durée 1-480 à la frappe + bouton désactivé) | `main.py` | [cours12_todo_validation.py](exercices-corriges/cours12_todo_validation.py) |
| Cours 13 | JSON, CSV, filedialog | 1 (formulaire + Treeview + Ajouter/Supprimer + import/export) | `table.py` (bon), `main.py` (abandonné) | [cours13_formulaire_json_csv.py](exercices-corriges/cours13_formulaire_json_csv.py) |
| Cours 14 | Matplotlib dans Tkinter | 1 (courbe, nuage, barres selon un Combobox) | `main.py`, `demo.py` (démo du prof) | [cours14_graphiques_tkinter.py](exercices-corriges/cours14_graphiques_tkinter.py) |
| Cours 15 | (pas de PowerPoint) | gestion de produits (corrigé du prof) | `Manager.py` (commencé), `corrige.py` | [cours15_gestion_produits.py](exercices-corriges/cours15_gestion_produits.py) |

Au total : 21 exercices, plus les démos. Ce qui était faux ou incomplet dans chacun est expliqué dans [CORRECTIONS.md](CORRECTIONS.md).

## Vérifié

Chaque corrigé et chaque gabarit a été lancé et piloté par un script de test (remplir les champs, cliquer, vérifier les résultats affichés, exporter puis réimporter en JSON et CSV). Exemples de valeurs vérifiées : l'hôtel donne bien 390 $ / 58,4 $ / 448,4 $ comme dans l'énoncé, et la to-do du cours 12 refuse les lettres et les durées au-dessus de 480 pendant la frappe.
