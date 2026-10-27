import numpy as np
import matplotlib.pyplot as plt

NB_CLIENTS = 25
MOYENNE = 80
ECART_TYPE = 12
NIVEAUX = ["Très satisfait", "Satisfait", "Neutre", "Insatisfait", "Très insatisfait"]


def niveau_satisfaction(note):
    if note > 90:
        return "Très satisfait"
    elif note > 80:
        return "Satisfait"
    elif note > 70:
        return "Neutre"
    elif note > 60:
        return "Insatisfait"
    return "Très insatisfait"


np.random.seed(42)  # mêmes notes à chaque exécution (pratique pour vérifier)
notes = MOYENNE + ECART_TYPE * np.random.standard_normal(size=NB_CLIENTS)
notes = np.clip(notes, 0, 100)  # aucune note au-dessus de 100 (ni sous 0)

compte = {niveau: 0 for niveau in NIVEAUX}
for note in notes:
    compte[niveau_satisfaction(note)] += 1

print("Notes :", np.round(notes, 1))
for niveau, nb in compte.items():
    print(f"{niveau:<18} {nb}")

fig, (ax_hist, ax_table) = plt.subplots(1, 2, figsize=(11, 5))

ax_hist.hist(notes, bins=[0, 60, 70, 80, 90, 100], edgecolor="black", color="skyblue")
ax_hist.set_title("Distribution des notes")
ax_hist.set_xlabel("Note")
ax_hist.set_ylabel("Nombre de clients")
ax_hist.grid(True, alpha=0.3)

ax_table.axis("off")
ax_table.table(cellText=[[niveau, nb] for niveau, nb in compte.items()],
               colLabels=["Niveau", "Nombre"], loc="center", cellLoc="center")
ax_table.set_title("Niveaux de satisfaction")

plt.tight_layout()
plt.show()
