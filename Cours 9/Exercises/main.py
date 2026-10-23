import tkinter as tk

class Reserve(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Reservation d'hotel")
        self.geometry("600x600")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        content = tk.Frame(self, padx=10, pady=10)
        content.grid(row=0, column=0, sticky="nsew")

        ctn_1 = tk.Frame(content, padx=10, pady=10)
        ctn_1.grid(row=0, column=0, sticky="nsew")
        ctn_1.columnconfigure(0, weight=1)
        ctn_1.rowconfigure(0, weight=1)

        ctn_2 = tk.Frame(content, padx=10, pady=10)
        ctn_2.grid(row=0, column=1, sticky="nsew")
        ctn_2.columnconfigure(0, weight=1)
        ctn_2.columnconfigure(1, weight=1)
        ctn_2.rowconfigure(0, weight=2)
        ctn_2.rowconfigure(1, weight=1)

        ctn2_1  = tk.LabelFrame(content,text="Info client", padx=10, pady=10)
        ctn2_1.grid(row=0, column=1, sticky="nsew")

        tk.Label(ctn_1, text="Reservation", bg="blue", fg="white").grid(row=0, column=0, sticky="ew")



if __name__ == "__main__":
    App = Reserve()
    App.mainloop()


