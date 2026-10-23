import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
import json, csv
import re


FIELDS = ("nom", "email", "age")

class Formulaire(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formulaire")
        self.geometry("700x450")
        self.init_widgets()
        self.rows = []

    def init_widgets(self):

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header_content = tk.Frame(self)
        header_content.grid(row=0, column=0, sticky="ew")
        header_content.columnconfigure(0, weight=1)
        header_content.columnconfigure(1, weight=1)
        header_content.columnconfigure(2, weight=1)

        # labels
        self.Nom = tk.Label(header_content, text="Nom")
        self.Nom.grid(row=0, column=0, sticky="w", padx=20, pady=5)
        self.Email = tk.Label(header_content, text="Email")
        self.Email.grid(row=0, column=1, sticky="w", padx=20, pady=5)
        self.Age = tk.Label(header_content, text="Ã‚ge")
        self.Age.grid(row=0, column=2, sticky="w", padx=20, pady=5)

        # inputs
        self.Nom_Entry = tk.Entry(header_content)
        self.Nom_Entry.grid(row=1, column=0, sticky="ew", padx=(20, 5), pady=5)
        self.Email_Entry = tk.Entry(header_content, width=40)
        self.Email_Entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.Age_Entry = tk.Entry(header_content)
        self.Age_Entry.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        # buttons
        self.Btn_Ajouter = tk.Button(header_content, text="Ajouter", command=self.ajouter)
        self.Btn_Ajouter.grid(row=1, column=3, sticky="e", padx=5, pady=5)
        self.Btn_Supprimer = tk.Button(header_content, text="Supprimer sÃ©lection", command=self.supprimer)
        self.Btn_Supprimer.grid(row=1, column=4, sticky="e", padx=(5, 20), pady=5)

        main_content = tk.Frame(self)
        main_content.grid(row=1, column=0, sticky="snew")
        # Configurer les poids de la grille pour que le Treeview s'Ã©tire bien
        main_content.columnconfigure(0, weight=1)
        main_content.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(main_content, columns=("nom", "email", "age"), show="headings", selectmode="extended")

        self.tree.heading("nom", text="Nom")
        self.tree.heading("email", text="Email")
        self.tree.heading("age", text="Ã‚ge")

        self.tree.column("nom", minwidth=100, width=200)
        self.tree.column("email", minwidth=100, width=200)
        self.tree.column("age", minwidth=100, width=200)

        self.tree.grid(column=0, row=0, sticky="nsew", padx=15, pady=5)

        footer_content = tk.Frame(self)
        footer_content.grid(row=2, column=0, sticky="snew")
        footer_content.columnconfigure(1, weight=1)
        footer_content.columnconfigure(2, weight=1)
        self.Btn_Importer_Json = tk.Button(footer_content, text="Importer JSON", command=self.importerJson)
        self.Btn_Importer_Json.grid(row=0, column=0, sticky="w", padx=(20, 5), pady=5)
        self.Btn_Importer_CSV = tk.Button(footer_content, text="Importer CSV", command=self.importerCSV)
        self.Btn_Importer_CSV.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.Btn_Exporter_Json = tk.Button(footer_content, text="Exporter JSON", command=self.exporterJson)
        self.Btn_Exporter_Json.grid(row=0, column=3, sticky="e", padx=5, pady=5)
        self.Btn_Exporter_CSV = tk.Button(footer_content, text="Exporter CSV", command=self.exporterCSV)
        self.Btn_Exporter_CSV.grid(row=0, column=4, sticky="e", padx=(5, 20), pady=5)

    def ajouter(self):
        nom = self.Nom_Entry.get()
        email = self.Email_Entry.get()
        age = self.Age_Entry.get()

        if not nom:
            messagebox.showwarning("Validation", "Le nom est obligatoire")
            return

        if not email:
            messagebox.showwarning("Validation", "L'email est obligatoire")
            return

        if  not age or not age.isdigit():
            messagebox.showwarning("Validation", "L'age doit etre un entier")
            return

        self.tree.insert('', 'end', values=(nom, email, age))
        self.rows.append({"nom": nom, "email": email,"age": age})

        # Vider les champs aprÃ¨s l'insertion
        self.Nom_Entry.delete(0, tk.END)
        self.Email_Entry.delete(0, tk.END)
        self.Age_Entry.delete(0, tk.END)



    # def supprimer(self):
    #     selected_row = self.tree.selection()
    #     if selected_row:
    #         index = self.tree.index(selected_row[0])
    #         self.rows.pop(index)
    #         self.tree.delete(selected_row[0]) #*selected_rows permet de dÃ©composer le tuple en plusieurs arguments.
    #     else:
    #         messagebox.showwarning("Validation", "Aucun Ã©lÃ©ment sÃ©lectionnÃ©")

    def supprimer(self):
        selected_rows = self.tree.selection()

        if selected_rows:
            indices = []
            for row in selected_rows:
                indices.append(self.tree.index(row))

            indices.sort(reverse=True)

            for index in indices:
                self.rows.pop(index)

            self.tree.delete(*selected_rows)
        else:
            messagebox.showwarning("Validation", "Aucun Ã©lÃ©ment sÃ©lectionnÃ©")


    def importerJson(self):
        path = filedialog.askopenfilename(title="Importer JSON", filetypes=(("JSON", "*.json")
                                                                                , ("All files", "*.*")))
        if not path:
            return
        try:
            with open(path, "r", encoding ="utf-8") as f:
                data = json.load(f)
                nouvelles_lignes = []
                for r in data:
                    if isinstance(r, dict):
                        ligne = {}
                        for k in FIELDS:
                            ligne[k] = r.get(k)
                        nouvelles_lignes.append(ligne)
                self.rows = nouvelles_lignes
                self.tree.delete(*self.tree.get_children())
                for r in self.rows:
                    self.tree.insert('', 'end', values=(r["nom"], r["email"], r["age"]))
        except Exception as e:
            messagebox.showwarnings("Validation", "le fichier Ã  importer est obligatoire")




    def importerCSV(self):
        path = filedialog.askopenfilename(title="Importer CSV", filetypes=[("CSV", "*.csv")])

        if not path:
            return
        try:
            with open(path, "r", newline ="", encoding ="utf-8") as f:
                reader = csv.DictReader(f)

                nouvelles_lignes = []
                for r in reader:
                    ligne = {}
                    for k in FIELDS:
                        ligne[k] = r.get(k)
                    nouvelles_lignes.append(ligne)

            self.rows = nouvelles_lignes
            self.tree.delete(*self.tree.get_children())
            for r in self.rows:
                self.tree.insert("", "end", values=(r["nom"], r["email"], r["age"]))

        except Exception as e:
            messagebox.showerror("Erreur d'importation", str(e))

    # -------------- Export JSON / CSV --------------
    def exporterJson(self):
        if not self.rows:
            messagebox.showinfo("Export Json", "Rien Ã  exporter")
            return

        path = filedialog.asksaveasfilename(title = "Exporter Json", defaultextension=".json",
                                            filetypes=[("Json files", "*.json")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.rows, f, indent=4)
            messagebox.showinfo("Export Json", "Export terminÃ©")
        except Exception as e:
            messagebox.showerror("Echec export", str(e))


    def exporterCSV(self):
        if not self.rows:
            messagebox.showinfo("Export CSV", "Rien Ã  exporter")
            return

        path = filedialog.asksaveasfilename(title = "Export CSV", defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["nom", "email", "age"])
                writer.writeheader()
                for row in self.rows:
                    ligne = {}
                    for k in FIELDS:
                        ligne[k] = row.get(k,"")
                    writer.writerow(ligne)
            messagebox.showinfo("Export CSV", "Export terminÃ©")
        except Exception as e:
            messagebox.showerror("Echec export", str(e))




if __name__ == "__main__":
    Formulaire().mainloop()