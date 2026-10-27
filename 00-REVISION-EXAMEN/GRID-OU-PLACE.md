# grid ou place ?

Réponse courte : **grid**, sauf si l'énoncé exige `place()`.

L'exercice du cours 11 disait mot pour mot « L'ensemble des widgets de l'interface doit être positionné à l'aide du gestionnaire place() ». Si tu lis une phrase comme ça à l'examen, tu prends `place`. Sinon, grid, toujours.

## Pourquoi grid gagne presque tout le temps

Presque toutes les interfaces du cours sont des formulaires : une colonne de libellés, une colonne de champs, un cadre de résumé, une rangée de boutons. C'est littéralement une grille. Avec grid, tu donnes un numéro de ligne et de colonne et Tkinter aligne tout seul. Avec place, tu inventes un pourcentage pour chaque widget, et si un texte s'allonge, rien ne se décale : les widgets se chevauchent sans aucun message d'erreur.

Grid redimensionne bien aussi, à condition de faire les deux choses suivantes :

```python
conteneur.columnconfigure(1, weight=1)          # 1) la colonne reçoit l'espace libre
entry.grid(row=0, column=1, sticky="ew")        # 2) le widget s'étire dans sa cellule
```

Une des deux sans l'autre ne fait rien. C'est l'erreur la plus fréquente : on met `sticky="ew"`, rien ne bouge, parce que la colonne a encore `weight=0`.

### La méthode qui marche à chaque fois

1. Découpe la capture d'écran de l'énoncé en **zones** (titre, infos client, résumé, options, boutons). Chaque zone devient un `Frame` ou un `LabelFrame` placé dans la fenêtre avec grid.
2. Dans chaque zone, recommence la numérotation à `row=0, column=0`. Les lignes et colonnes d'un frame n'ont rien à voir avec celles de la fenêtre.
3. Un widget qui traverse plusieurs colonnes (titre, barre de boutons, zone d'options) : `columnspan`.
4. Une barre de boutons de même largeur : un frame, `columnconfigure((0, 1, 2), weight=1)`, puis chaque bouton en `sticky="ew"`.
5. Valeurs collées à droite dans un résumé (« 0.00 $ ») : libellé en `sticky="w"`, valeur en `sticky="e"`, et `weight=1` sur la colonne des valeurs.

Le gabarit [gabarits/04_fenetre_grid.py](gabarits/04_fenetre_grid.py) applique exactement ces cinq règles. Les corrigés [cours09_reservation_hotel.py](exercices-corriges/cours09_reservation_hotel.py) et [cours10_centre_sportif.py](exercices-corriges/cours10_centre_sportif.py) aussi.

### Les bugs grid que tu as déjà eus

- **Deux widgets dans la même cellule.** Dans ta version de l'hôtel, `label_taxes` et `label_total` étaient tous les deux en `row=4` : le total cachait les taxes. Grid ne prévient pas, le dernier placé gagne.
- **Le parent oublié.** `tk.Entry()` sans parent atterrit dans la fenêtre principale. Dans tes cours 12 et 13 ça passait parce que les champs étaient justement dans la fenêtre, mais dès qu'ils doivent aller dans un frame, ils apparaissent au mauvais endroit. Écris toujours le parent en premier argument.
- **Des `rowconfigure(i, weight=1)` partout.** Dans le centre sportif, toutes les lignes s'étiraient, donc les cadres flottaient au milieu d'espaces vides quand on agrandissait. Mets `weight=1` seulement sur la ligne qui doit grandir (souvent celle du tableau ou de la Listbox).

## Quand tu dois utiliser place

Tout est relatif au **parent** et entre 0 et 1 :

```python
widget.place(relx=0.05, rely=0.15, relwidth=0.42, relheight=0.5)   # position + taille en %
titre.place(relx=0.5, rely=0.02, anchor="n")                       # centré horizontalement
bouton.place(relx=0.5, rely=0.5, anchor="center")                   # centré au milieu
```

Pour ne pas improviser les chiffres, planifie la largeur avant de coder. Deux cadres côte à côte : `5 % marge | 42 % | 6 % espace | 42 % | 5 % marge`, donc `relx=0.05` et `relx=0.53`, les deux avec `relwidth=0.42`. Dans un cadre, un libellé au-dessus d'un champ : le champ va à `rely` du libellé + 0.09.

`anchor` dit quel point du widget est posé sur la coordonnée. Par défaut c'est `"nw"` (coin haut-gauche). Sans `anchor="n"`, un titre à `relx=0.5` commence au milieu au lieu d'être centré.

`x=` et `y=` (en pixels) existent aussi, mais la position reste fixe quand on agrandit la fenêtre. Évite-les sauf si on te les demande.

Exemple complet : [gabarits/05_fenetre_place.py](gabarits/05_fenetre_place.py) et le corrigé [cours11_reservation_place/view.py](exercices-corriges/cours11_reservation_place/view.py).

## Et pack ?

Tu peux l'oublier, avec une seule règle à retenir : **ne mélange jamais pack et grid dans le même conteneur**. Tkinter plante avec `cannot use geometry manager grid inside . which already has slaves managed by pack`. Des frames différents peuvent utiliser des gestionnaires différents.

C'est pour ça que la barre d'outils Matplotlib (`NavigationToolbar2Tk`), qui utilise pack en interne, va dans son propre frame dans [gabarits/10_matplotlib_dans_tkinter.py](gabarits/10_matplotlib_dans_tkinter.py).

## Traduction pack → grid → place

| Ce que tu veux | pack | grid | place |
|---|---|---|---|
| Prendre toute la largeur | `fill="x"` | `sticky="ew"` + `weight=1` sur la colonne | `relwidth=1` |
| Remplir tout l'espace | `fill="both", expand=True` | `sticky="nsew"` + `weight=1` ligne et colonne | `relwidth=1, relheight=1` |
| Mettre côte à côte | `side="left"` | `column=0`, `column=1`, ... | `relx` différents |
| Marge extérieure | `padx=, pady=` | `padx=, pady=` | (calculer dans relx/rely) |
| Marge intérieure | `ipadx=, ipady=` | `ipadx=, ipady=` | (n/a) |
| Cacher puis réafficher | `pack_forget()` | `grid_remove()` puis `grid()` | `place_forget()` |
| Lire les options | `pack_info()` | `grid_info()` | `place_info()` |
