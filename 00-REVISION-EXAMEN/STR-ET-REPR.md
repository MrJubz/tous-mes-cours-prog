# `__str__`, `__repr__` et le `!r`

Les exemples viennent du modèle du [formatif de pratique](formatif-pratique/corrige/model.py).

## Deux textes pour deux lecteurs

Les deux méthodes transforment l'objet en texte, mais pas pour la même personne.

| | `__str__` | `__repr__` |
|---|---|---|
| Pour qui | l'**utilisateur** | le **programmeur** (toi qui débogues) |
| Appelée par | `print(e)`, `str(e)`, `f"{e}"` | `repr(e)`, la console, **les éléments d'une liste** |
| Dans le formatif | `2412034 Léa Tremblay (Informatique) : 87.5 %` | `Etudiant('2412034', 'Léa Tremblay')` |

Règle pour `__repr__` : le texte doit ressembler au code qui recrée l'objet. On voit tout de suite la classe et les valeurs.

### Sans `__repr__`

```python
>>> print([e1, e2])
[<model.Etudiant object at 0x0000021F3A8C1D90>, <model.Etudiant object at 0x0000021F3A8C1E50>]
```

`print` d'une **liste** utilise le `__repr__` de chaque élément, pas le `__str__`. Ton `__str__` peut être parfait, `print(groupe.etudiants)` affiche quand même ce charabia tant qu'il n'y a pas de `__repr__`.

Avec le `__repr__` du formatif :

```python
>>> print(groupe.etudiants)
[Etudiant('2412034', 'Léa Tremblay'), EtudiantReprise('2311902', 'Noah Roy')]
```

S'il n'y a pas de `__str__`, `print` se rabat sur `__repr__`. L'inverse n'est pas vrai.

## Le `!r` dans un f-string

`{x!r}` veut dire « mets `repr(x)` ici au lieu de `str(x)` ». Pour une chaîne, ça ajoute **les guillemets** :

```python
nom = "Léa Tremblay"
f"{nom}"      # Léa Tremblay
f"{nom!r}"    # 'Léa Tremblay'
```

Le `__repr__` du formatif :

```python
def __repr__(self):
    return f"{type(self).__name__}({self.matricule!r}, {self.nom!r})"
```

| Avec `!r` | Sans `!r` |
|---|---|
| `Etudiant('2412034', 'Léa Tremblay')` | `Etudiant(2412034, Léa Tremblay)` |

Sans `!r` :

1. `2412034` a l'air d'un **int**, alors que c'est une chaîne. Les guillemets montrent le vrai type, et c'est ce qu'on cherche quand on débogue.
2. `Léa Tremblay` sans guillemets n'est pas du Python valide. On ne voit plus où finit un argument et où commence le suivant.

### Pourquoi ne pas écrire les guillemets à la main ?

```python
f"Etudiant('{self.matricule}', '{self.nom}')"
```

Ça marche jusqu'au premier nom avec une apostrophe : `D'Amour` donne `Etudiant('2412034', 'D'Amour')`, qui est cassé. `!r` choisit les bons guillemets tout seul : `repr("D'Amour")` donne `"D'Amour"`.

Pour les nombres, `!r` ne change rien (`repr(87.5)` donne `87.5`, comme `str`). C'est surtout utile pour les chaînes.

## `type(self).__name__`

Au lieu d'écrire `"Etudiant"` en dur, on demande le nom de la vraie classe de l'objet. `EtudiantReprise` hérite donc du `__repr__` sans le redéfinir et affiche quand même `EtudiantReprise('2311902', 'Noah Roy')`.

## Les erreurs classiques

- **`print` au lieu de `return`.** Python lève `TypeError: __repr__ returned non-string (type NoneType)`. `__str__` et `__repr__` doivent **retourner** une chaîne.
- **Retourner un nombre**, comme `return self.moyenne()` : même erreur. Écris `return f"{self.moyenne():.1f}"`.
- **Mettre l'affichage utilisateur dans `__repr__`.** Ça ne plante pas, mais si l'énoncé demande les deux méthodes, le prof s'attend à deux textes différents.

En une phrase : `__str__` est joli pour l'utilisateur, `__repr__` est précis pour toi, et `!r` met les guillemets qui montrent que c'est une chaîne.
