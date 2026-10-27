"""Gabarit : random, NumPy et Matplotlib (hors Tkinter). Chaque bloc est indépendant."""
import random
import numpy as np
import matplotlib.pyplot as plt

# ---------- random ----------
random.seed(1)                     # mêmes résultats à chaque exécution
de = random.randint(1, 6)          # entier dans [1, 6] (6 inclus)
x = random.uniform(-1, 1)          # float dans [-1, 1[
choix = random.choice(["a", "b"])  # un élément au hasard
print(de, round(x, 3), choix)

# ---------- NumPy : créer des tableaux ----------
a = np.arange(0, 11, 2)            # [0 2 4 6 8 10] : fin EXCLUE, on donne le PAS
b = np.linspace(0, 2, 5)           # [0. 0.5 1. 1.5 2.] : fin INCLUSE, on donne le NOMBRE de valeurs
c = np.array([3, 7, 1, 9])
mixte = np.array([1, "texte", 2.5], dtype=object)  # tableau hétérogène (rare)

# ---------- NumPy : calculs vectorisés (pas de boucle) ----------
print(c * 2, c + 10, c ** 2)
print(c.sum(), c.mean(), c.max(), c.min(), c.std())
print(np.sin(np.pi / 2), np.cos(0), np.sqrt(16), np.exp(1))  # trigonométrie en RADIANS
print(np.round(np.degrees(np.pi), 1), np.radians(180))

# ---------- NumPy : slicing et masques ----------
M = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(M[:2, 1:3])        # 2 premières lignes, colonnes 1 et 2 → [[2 3] [5 6]]
print(M[:, 0])           # toute la colonne 0
print(c[c > 2])          # masque booléen : garde les valeurs > 2
print(np.clip(c, 2, 8))  # borne les valeurs entre 2 et 8

# ---------- Distribution normale (exercice satisfaction) ----------
notes = 80 + 12 * np.random.standard_normal(size=25)
notes = np.clip(notes, 0, 100)

# ---------- Matplotlib : plusieurs graphiques dans une figure ----------
fig, axes = plt.subplots(2, 3, figsize=(13, 7))

x = np.linspace(0, 2 * np.pi, 100)
axes[0, 0].plot(x, np.sin(x), "b-", label="sin")   # "b-" = bleu, ligne continue
axes[0, 0].plot(x, np.cos(x), "r--", label="cos")  # "r--" = rouge, pointillés
axes[0, 0].set_title("plot (courbes)")
axes[0, 0].legend()
axes[0, 0].grid(True)

axes[0, 1].scatter(np.random.rand(30), np.random.rand(30), c="green", marker="o", s=20)
axes[0, 1].set_title("scatter (nuage)")

axes[0, 2].bar(["A", "B", "C"], [5, 9, 3], color="orange")
axes[0, 2].set_title("bar (barres)")

axes[1, 0].hist(notes, bins=10, edgecolor="black")
axes[1, 0].set_title("hist (distribution)")

axes[1, 1].pie([60, 30, 10], labels=["Dispo", "Empruntés", "Perdus"], autopct="%1.0f%%")
axes[1, 1].set_title("pie (circulaire)")

axes[1, 2].fill([0, 2, 1], [0, 0, 2], color="skyblue", edgecolor="black", linestyle="--")
axes[1, 2].set_title("fill (polygone)")
axes[1, 2].set_axisbelow(True)
axes[1, 2].grid(True)

for ax in axes.flat:
    ax.set_xlabel("x")
    ax.set_ylabel("y")

plt.tight_layout()
plt.show()

# Version « une seule figure » la plus simple :
# plt.figure(figsize=(6, 4))
# plt.plot([1, 2, 3], [4, 1, 6], ".b-")
# plt.title("Titre"); plt.xlabel("x"); plt.ylabel("y"); plt.grid(True)
# plt.show()
