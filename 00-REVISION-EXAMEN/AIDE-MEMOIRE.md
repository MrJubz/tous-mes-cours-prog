# Aide-mémoire

Toute la syntaxe des cours 1 à 15, sans les explications longues. Pour un exemple qui tourne, le fichier indiqué à côté de chaque section.

## POO (cours 1 à 3) · [01_classe_modele.py](gabarits/01_classe_modele.py) · [02_heritage_polymorphisme.py](gabarits/02_heritage_polymorphisme.py)

```python
class Produit:
    TAXES = {"A": 0.05}                 # constante de classe (MAJUSCULES)

    def __init__(self, nom, prix=None): # paramètre facultatif = None
        self.nom = nom                  # passe par le setter → validation dès la création
        self.prix = prix

    @property
    def nom(self):
        return self.__nom               # __ = privé (devient _Produit__nom)

    @nom.setter
    def nom(self, valeur):
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Nom vide.")
        self.__nom = valeur.strip()
```

| Préfixe | Visibilité | Accès depuis une classe fille |
|---|---|---|
| `nom` | public | oui |
| `_nom` | protégé (convention) | oui |
| `__nom` | privé (name mangling) | **non**, passer par la property |

Nommage : classes en `CamelCase`, méthodes et variables en `snake_case`, constantes en `MAJUSCULES`, pas d'accents dans les noms.

Héritage :

```python
class Fille(Mere):
    def __init__(self, a, b, c):
        super().__init__(a, b)          # ou Mere.__init__(self, a, b)  (obligatoire en héritage multiple)
        self.__c = c

    def methode(self):                  # redéfinition (overriding)
        return super().methode() + " et plus"
```

Méthodes magiques :

| Méthode | Déclenchée par |
|---|---|
| `__init__(self, ...)` | `Classe(...)` |
| `__str__(self)` | `print(obj)`, `str(obj)`, f-string |
| `__repr__(self)` | console, affichage dans une liste ; sert aussi de repli si `__str__` n'existe pas. Le `!r` : [STR-ET-REPR.md](STR-ET-REPR.md) |
| `__lt__(self, other)` | `a < b`, et donc `sorted()`, `min()`, `max()` |
| `__gt__`, `__le__`, `__ge__`, `__eq__` | `>`, `<=`, `>=`, `==` |
| `__add__(self, other)`, `__mul__` | `a + b`, `a * b` |
| `__len__(self)` | `len(obj)` |

Python n'a pas de vraie surcharge (overloading) : on utilise des paramètres par défaut (`def f(a, b=0)`).

## random, NumPy, Matplotlib (cours 4) · [03_numpy_matplotlib.py](gabarits/03_numpy_matplotlib.py)

```python
random.randint(1, 6)        # entier, 6 INCLUS
random.uniform(a, b)        # float
random.seed(42)             # résultats reproductibles

np.arange(0, 11, 2)         # début, fin EXCLUE, PAS     → [0 2 4 6 8 10]
np.linspace(0, 2, 5)        # début, fin INCLUSE, NOMBRE → [0. 0.5 1. 1.5 2.]
moy + ecart * np.random.standard_normal(size=n)   # distribution normale
np.clip(t, 0, 100)          # borner
t[t > 50]                   # masque booléen
M[:2, 1:3]                  # slicing 2D : lignes 0-1, colonnes 1-2
np.sin(x)                   # en RADIANS ; np.radians(180), np.degrees(np.pi)
```

```python
plt.figure(figsize=(8, 4))
plt.plot(x, y, "b-", label="sin")       # "ro" rouge cercles, "g--" vert pointillés, ".b-"
plt.scatter(x, y)    plt.bar(noms, valeurs)    plt.hist(data, bins=10)
plt.pie(valeurs, labels=noms, autopct="%1.0f%%")    plt.fill(xs, ys, color="c", ec="k")
plt.title("..."); plt.xlabel("..."); plt.ylabel("..."); plt.legend(); plt.grid(True)
plt.show()
```

## Fenêtre Tkinter (cours 6-7)

```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Titre")
        self.geometry("600x400")
        self.create_widgets()

if __name__ == "__main__":
    App().mainloop()
```

Options communes : `text`, `font=("Arial", 12, "bold")`, `fg`, `bg`, `width`, `height`, `relief` (`flat`, `groove`, `sunken`, `raised`, `ridge`), `state` (`normal`, `disabled`, `readonly`), `anchor`, `justify`, `wraplength`.

## Widgets et méthodes · [06_widgets_et_methodes.py](gabarits/06_widgets_et_methodes.py)

| Widget | Créer | Lire | Écrire / modifier | Effacer |
|---|---|---|---|---|
| Entry | `tk.Entry(p, show="*")` | `e.get()` | `e.insert(0, "x")` | `e.delete(0, tk.END)` |
| Text | `tk.Text(p, wrap="word", undo=True)` | `t.get("1.0", "end-1c")` | `t.insert("end", "x")` | `t.delete("1.0", "end")` |
| Listbox | `tk.Listbox(p, selectmode="extended")` | `lb.get(i)`, `lb.curselection()` | `lb.insert("end", "a", "b")` | `lb.delete(i)` |
| Combobox | `ttk.Combobox(p, values=[...], state="readonly")` | `c.get()` | `c.current(0)`, `c.set("x")` | |
| Spinbox | `tk.Spinbox(p, from_=0, to=10, increment=1)` | `s.get()` | `s.insert(0, "3")` | `s.delete(0, "end")` |
| Checkbutton | `tk.Checkbutton(p, variable=tk.BooleanVar())` | `var.get()` | `var.set(True)` | |
| Radiobutton | même `StringVar` pour tout le groupe, `value=` différente | `var.get()` | `var.set("A")` | |
| Label | `tk.Label(p, text="...")` | `l.cget("text")` | `l.config(text="...")` | |
| Treeview | `ttk.Treeview(p, columns=cols, show="headings")` | `tree.item(i, "values")`, `tree.selection()`, `tree.index(i)` | `tree.insert("", "end", values=(...))` | `tree.delete(*tree.get_children())` |

Index du Text : `"ligne.colonne"`, ligne à partir de 1, colonne à partir de 0. `"2.end+1c"` = fin de la ligne 2 plus le saut de ligne.

Tous les widgets : `config(option=val)` (= `configure`), `cget("option")`, `destroy()`, `focus_set()`.

Messagebox : `showinfo(titre, msg)`, `showwarning`, `showerror`, `askyesno` (retourne True/False).

Conteneurs : `Frame` (invisible), `LabelFrame(p, text="Titre")` (bordure + titre), `PanedWindow(p, orient="horizontal")` puis `.add(enfant)`.

Scrollbar (deux lignes qui vont ensemble) :

```python
sb = ttk.Scrollbar(p, orient="vertical", command=widget.yview)
widget.configure(yscrollcommand=sb.set)
```

## Événements (cours 7-8) · [07_evenements.py](gabarits/07_evenements.py)

```python
tk.Button(p, text="OK", command=self.ok)                   # pas d'event reçu
tk.Button(p, text="7", command=lambda: self.clic("7"))     # avec argument → lambda
for t in "789":                                            # dans une boucle → t=t !
    tk.Button(p, text=t, command=lambda t=t: self.clic(t))

widget.bind("<Return>", self.methode)     # def methode(self, event): ...
self.bind_all("<Control-s>", ...)         # raccourci global
self.bind_class("TButton", "<Enter>", ...)# tous les ttk.Button
self.event_generate("<<MonEvenement>>")   # déclencher un événement virtuel perso
```

`<Button-1>` clic gauche · `<Button-3>` clic droit · `<Double-Button-1>` · `<Key>` · `<KeyRelease>` · `<Return>` · `<Escape>` · `<Enter>` / `<Leave>` survol · `<FocusIn>` / `<FocusOut>` · `<Configure>` redimension · `<<ComboboxSelected>>` · `<<ListboxSelect>>` · `<<TreeviewSelect>>`

Dans le gestionnaire : `event.widget`, `event.char`, `event.keysym`, `event.x`, `event.y`.

## grid et place (cours 9 et 11) · [GRID-OU-PLACE.md](GRID-OU-PLACE.md)

```python
w.grid(row=0, column=1, columnspan=2, rowspan=1, sticky="nsew", padx=5, pady=5)
conteneur.columnconfigure(1, weight=1)      # ou columnconfigure((0, 1, 2), weight=1)
conteneur.rowconfigure(2, weight=1)

w.place(relx=0.5, rely=0.1, anchor="n", relwidth=0.4, relheight=0.3)
w.place(x=100, y=50, width=150, height=40)  # pixels, fixe
```

## Validation et erreurs (cours 12) · [08_validation_erreurs.py](gabarits/08_validation_erreurs.py)

```python
# À la frappe : %P = contenu APRÈS la frappe ; retourner True / False
vcmd = (self.register(self.verif), "%P")
invcmd = (self.register(self.refus),)
tk.Entry(p, validate="key", validatecommand=vcmd, invalidcommand=invcmd)

def verif(self, valeur):
    return valeur == "" or (valeur.isdigit() and 1 <= int(valeur) <= 480)

# Bouton actif seulement si le formulaire est valide
self.var = tk.StringVar()
self.var.trace_add("write", self.maj_bouton)      # def maj_bouton(self, *args)
self.btn.config(state="normal" if ok else "disabled")

# Au clic
try:
    n = int(self.entry.get())
except ValueError:
    messagebox.showerror("Saisie invalide", "Entier attendu.")
else:
    ...          # seulement si aucune erreur
finally:
    ...          # toujours
```

`"12".isdigit()` → True, mais `"-3"` et `"2.5"` → False. Pour un float : `try: float(x)`.

Signal discret : `self.bell()`, couleur temporaire avec `self.after(500, fonction)`.

## JSON et CSV (cours 13) · [09_json_csv.py](gabarits/09_json_csv.py)

```python
with open(chemin, "w", encoding="utf-8") as f:
    json.dump(liste_de_dicts, f, indent=4, ensure_ascii=False)
with open(chemin, "r", encoding="utf-8") as f:
    data = json.load(f)
# chaînes : json.dumps(obj) / json.loads(texte)

with open(chemin, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["nom", "age"]); w.writeheader(); w.writerows(lignes)
with open(chemin, "r", newline="", encoding="utf-8") as f:
    lignes = list(csv.DictReader(f))        # toutes les valeurs sont du TEXTE

chemin = filedialog.askopenfilename(title="Ouvrir", filetypes=[("CSV", "*.csv"), ("Tous", "*.*")])
chemin = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
if not chemin: return                       # Annuler → chaîne vide
```

## Matplotlib dans Tkinter (cours 14) · [10_matplotlib_dans_tkinter.py](gabarits/10_matplotlib_dans_tkinter.py)

```python
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

self.fig = Figure(figsize=(8, 4))
self.ax = self.fig.add_subplot(111)
self.canvas = FigureCanvasTkAgg(self.fig, master=self)
self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

def tracer(self):
    self.ax.clear()
    self.ax.plot(x, y)
    self.ax.set_title("..."); self.ax.set_xlabel("..."); self.ax.legend(); self.ax.grid(True)
    self.canvas.draw()                       # sans draw(), rien ne change
```

Avec `ax` on écrit `set_title`, `set_xlabel`, `set_ylabel` (avec `plt` c'est `title`, `xlabel`, `ylabel`).

## Erreurs qui reviennent

| Symptôme | Cause |
|---|---|
| `AttributeError: '...' object has no attribute '_Fille__x'` | `self.__x` utilisé dans une classe fille : utiliser la property ou `_x` |
| `AttributeError: ... has no attribute 'taches'` dès l'ouverture | `create_widgets()` utilise un attribut que `__init__` crée seulement **après** l'appel : crée les données d'abord |
| Tous les boutons d'une boucle font la même chose | `lambda: f(t)` au lieu de `lambda t=t: f(t)` |
| `cannot use geometry manager grid inside ...` | pack et grid dans le même conteneur |
| `sticky="ew"` ne fait rien | oublié `columnconfigure(col, weight=1)` |
| Un widget disparaît | deux widgets dans la même cellule de grid |
| `ValueError: invalid literal for int()` qui ferme tout | `int(entry.get())` sans `try/except` |
| `messagebox.showwarning("texte")` n'affiche rien d'utile | il faut **deux** arguments : titre, message |
| Fichier JSON plein de `\u00e9` | `ensure_ascii=False` |
| Lignes vides entre chaque ligne du CSV (Windows) | `newline=""` dans `open()` |
| « Ã© » à la place de « é » | fichier lu/écrit sans `encoding="utf-8"` |
| La sélection de la Listbox disparaît quand on clique ailleurs | `tk.Listbox(..., exportselection=False)` |
