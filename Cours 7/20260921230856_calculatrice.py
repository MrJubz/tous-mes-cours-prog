import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x400")
        self.num1 = ""
        self.num2 = ""
        self.operation = ""
        self.resultat = 0
        self.create_widget()

    def create_widget(self):
        ctn_nombre = tk.LabelFrame(self, borderwidth=8, relief="groove", width=350, height=50, bg="white")
        ctn_nombre.pack(fill="x", padx=10, pady=(10,5))

        self.affichage = tk.Label(ctn_nombre, text="0", font=("Arial", 20, "bold"),
                                          bg="white", anchor="e")
        self.affichage.pack(fill="x")

        row_1 = tk.Frame(self)
        row_1.pack(fill="x", pady=1)

        clear = tk.Button(row_1, text="C", font=("Arial", 15, "bold"), command=lambda: self.on_click("C"))
        clear.pack(side="left",fill="x", expand=True)
        slash = tk.Button(row_1, text="/", font=("Arial", 15, "bold"), command=lambda: self.on_click("/"))
        slash.pack(side="left",fill="x", expand=True)
        star = tk.Button(row_1, text="*", font=("Arial", 15, "bold"), command=lambda: self.on_click("*"))
        star.pack(side="left",fill="x", expand=True)

        row_2 = tk.Frame(self)
        row_2.pack(fill="x", pady=1)

        sept = tk.Button(row_2, text="7", font=("Arial", 15, "bold"), command=lambda: self.on_click("7"))
        sept.pack(side="left", fill="x", expand=True)
        huit = tk.Button(row_2, text="8", font=("Arial", 15, "bold"), command=lambda: self.on_click("8"))
        huit.pack(side="left", fill="x", expand=True)
        neuf = tk.Button(row_2, text="9", font=("Arial", 15, "bold"), command=lambda: self.on_click("9"))
        neuf.pack(side="left", fill="x", expand=True)
        moins = tk.Button(row_2, text="-", font=("Arial", 15, "bold"), command=lambda: self.on_click("-"))
        moins.pack(side="left", fill="x", expand=True)

        row_3 = tk.Frame(self)
        row_3.pack(fill="x", pady=1)

        quatre = tk.Button(row_3, text="4", font=("Arial", 15, "bold"), command=lambda: self.on_click("4"))
        quatre.pack(side="left", fill="x", expand=True)
        cinq = tk.Button(row_3, text="5", font=("Arial", 15, "bold"), command=lambda: self.on_click("5"))
        cinq.pack(side="left", fill="x", expand=True)
        six = tk.Button(row_3, text="6", font=("Arial", 15, "bold"), command=lambda: self.on_click("6"))
        six.pack(side="left", fill="x", expand=True)
        plus = tk.Button(row_3, text="+", font=("Arial", 15, "bold"), command=lambda: self.on_click("+"))
        plus.pack(side="left", fill="x", expand=True)

        row_4 = tk.Frame(self)
        row_4.pack(fill="x", pady=1)

        un = tk.Button(row_4, text="1", font=("Arial", 15, "bold"), command=lambda: self.on_click("1"))
        un.pack(side="left", fill="x", expand=True)
        deux = tk.Button(row_4, text="2", font=("Arial", 15, "bold"), command=lambda: self.on_click("2"))
        deux.pack(side="left", fill="x", expand=True)
        trois = tk.Button(row_4, text="3", font=("Arial", 15, "bold"), command=lambda: self.on_click("3"))
        trois.pack(side="left", fill="x", expand=True)
        egal = tk.Button(row_4, text="=", font=("Arial", 15, "bold"), command=lambda: self.on_click("="))
        egal.pack(side="left", fill="x", expand=True)

        row_5 = tk.Frame(self)
        row_5.pack(fill="x", pady=1)

        zero = tk.Button(row_5, text="0", font=("Arial", 15, "bold"), command=lambda: self.on_click("0"))
        zero.pack(side="left", fill="x", expand=True)
        point = tk.Button(row_5, text=".", font=("Arial", 15, "bold"), command=lambda: self.on_click("."))
        point.pack(side="left", fill="x", expand=True)

    def on_click(self, value):
        if value.isdigit() or value == ".":
            if self.operation == "":
                self.num1 += value
            else:
                self.num2 += value
        elif value == "C":
            self.erase()
        elif value == "=":
            self.egal()
        else:
            if self.num1 != "":
                self.operation = value
        self.rafraichir()

    def rafraichir(self):
        texte = self.num1 + self.operation + self.num2
        self.affichage.config(text=texte if texte != "" else "0")

    def erase(self):
        self.num1 = ""
        self.num2 = ""
        self.operation = ""
        self.resultat = 0

    def egal(self):
        if self.num1 == "" or self.num2 == "" or self.operation == "":
            messagebox.showerror("Erreur", "vous devez rentrer deux chiffre et un operateur")
            return
        if self.operation == "+":
            self.additionner()
        elif self.operation == "-":
            self.soustraire()
        elif self.operation == "*":
            self.multiplier()
        elif self.operation == "/":
            if float(self.num2) == 0:
                messagebox.showerror("Erreur", "division par zero impossible")
                return
            self.diviser()

        self.num1 = str(self.resultat)
        self.num2 = ""
        self.operation = ""

    def additionner(self):
        self.resultat = float(self.num1) + float(self.num2)

    def soustraire(self):
        self.resultat = float(self.num1) - float(self.num2)

    def multiplier(self):
        self.resultat = float(self.num1) * float(self.num2)

    def diviser(self):
        self.resultat =  float(self.num1) / float(self.num2)

if __name__ == "__main__":
    app = App()
    app.mainloop()