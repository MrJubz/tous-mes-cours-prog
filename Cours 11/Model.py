import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Reservation:
    INFORMATIONS_CLIENTS = {"Programmation": 40, "Robotique": 55, "Intelligence artificiel": 65, "Développement web": 45}
    def __init__(self, nom, courriel, activite, nb_place):
        self.nom = nom
        self.courriel = courriel
        self.activite = activite
        self.nb_place = nb_place


    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, nv_nom):
        if not nv_nom.strip():
            raise ValueError("ne peut pas être vide")
        self.__nom = nv_nom

    @property
    def courriel(self):
        return self.__courriel

    @courriel.setter
    def courriel(self, nv_courriel):
        if not nv_courriel.strip():
            raise ValueError("ne peut pas être vide")
        if not "@" in nv_courriel:
            raise ValueError("doit contenir un @")
        self.__courriel = nv_courriel

    @property
    def activite(self):
        return self.__activite

    @activite.setter
    def activite(self, nv_activite):
        if nv_activite not in self.INFORMATIONS_CLIENTS.keys():
            raise ValueError("doit être une des 4 activités de la liste")
        self.__activite = nv_activite

    @property
    def nb_place(self):
        return self.__nb_place

    @nb_place.setter
    def nb_place(self, nv_nb_place):
        if int(nv_nb_place) <= 0:
            raise ValueError("doit être supérieur à zéro")
        self.__nb_place = nv_nb_place

    def obtenir_prix_unitaire(self):
        return self.INFORMATIONS_CLIENTS[self.activite]

    def calculer_prix(self):
        return self.obtenir_prix_unitaire() * int(self.__nb_place)

    def obtenir_resume(self):
        return f"{self.__nom} - {self.__courriel} - {self.activite} - {self.__nb_place} - {self.calculer_prix()}"

