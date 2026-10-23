import tkinter as tk
from tkinter import ttk
import messagebox

class Produit:
    def __init__(self, nom, quantite, prix):
        self.nom = nom
        self.quantite = quantite
        self.prix = prix

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, valeur):
        self.__nom = valeur

    @property
    def quantite(self):
        return self.__quantite

    @quantite.setter
    def quantite(self, valeur):
        self.__quantite = valeur

    @property
    def prix(self):
        return self.__prix

    @prix.setter
    def prix(self, valeur):
        self.__prix = valeur

class AppProduit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualisation de courbes scientifiques")
        self.geometry("800x600")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.fonction = tk.StringVar(value="Courbe linéaire")

        self.craete_widget()

    def craete_widget(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def ajouter_produit(self):
        nom = self.entry_nom.get()
        quantite = self.entry_quantite.get()
        prix = self.entry_prix.get()

        try:
            produit = Produit(nom, quantite, prix)
            self.produits.append(produit)

            self.tree.insert("", "end", values=(produit.nom, produit.quantite, produit.prix))
            self.entry_nom.delete(0, tk.END)
            self.entry_quantite.delete(0, tk.END)
            self.entry_prix.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_produit(self):
        


