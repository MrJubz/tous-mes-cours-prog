import random as rnd

from matplotlib import pyplot as plt


class MonteCarlo:
    def __init__(self, nombre_points):
        self.x_in = []
        self.x_out = []
        self.y_in = []
        self.y_out = []
        self.nombre_points = nombre_points

    def generate(self):
        for _ in range(0, self.nombre_points):
            x = rnd.uniform(-1, 1)
            y = rnd.uniform(-1, 1)
            if x**2 + y**2 < 1:
                self.x_in.append(x)
                self.y_in.append(y)
            else:
                self.x_out.append(x)
                self.y_out.append(y)

    def estimer_pi(self):
        return 4 * len(self.x_in)/ self.nombre_points

    def afficher(self):
        plt.figure(figsize=(20,20))
        plt.scatter(self.x_in, self.y_in, s=1)
        plt.scatter(self.x_out, self.y_out, s=1)
        plt.show()


mc = MonteCarlo(4000000)
mc.generate()
pi = mc.estimer_pi()
mc.afficher()
print(pi)

