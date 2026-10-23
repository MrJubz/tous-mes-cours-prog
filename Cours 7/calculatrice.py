import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interface Simple")
        self.geometry("400x600")

        # nombre 1
        tk.Label(self, text="Nombre 1 :").pack(pady=(10,4))

        self.e1 = tk.Entry(self, width=20)
        self.e1.pack(pady=(0, 4))

        # nombre 2
        tk.Label(self, text="Nombre 2 :").pack(pady=(2, 4))

        self.e2 = tk.Entry(self, width=20)
        self.e2.pack(pady=(0, 4))

        #calcule
        tk.Button(self, text="Calculer", command=self.calculer_nombre, state="normal").pack(pady=(0, 4))

    def calculer_nombre(self):
        try:
            num1 = float(self.e1.get())
            num2 = float(self.e2.get())
            somme = num1 + num2

            messagebox.showinfo(title="Info", message=f"la somme est {somme}")

            self.e1.delete(0, "end")
            self.e2.delete(0, "end")
        except ValueError:
            messagebox.showerror(title="Erreur", message="Veuillez entrer deux nombres valides")

            self.e1.delete(0, "end")
            self.e2.delete(0, "end")

if __name__ == "__main__":
    app = App()
    app.mainloop()
