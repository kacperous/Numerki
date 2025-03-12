from zadanie1.rownania import Rownania
import numpy as np
import matplotlib.pyplot as plt

class Wykres:
    def rysuj_wykres(numer, a, b, bisekcja_x, siecznych_x, epsilon):
        rownania_obj = Rownania()

        x = np.linspace(a - 1, b + 1, 400)
        y = [rownania_obj.rownanie(numer, val) for val in x]

        plt.figure(figsize=(8, 5))
        plt.plot(x, y, label=f'Funkcja {numer}')
        plt.axhline(0, color='black', linewidth=1, linestyle='--')

        if bisekcja_x is not None:
            plt.scatter(bisekcja_x, 0, color='red', label=f'Bisekcja: {bisekcja_x:.5f}', zorder=3)
        if siecznych_x is not None:
            plt.scatter(siecznych_x, 0, color='blue', label=f'Siecznych: {siecznych_x:.5f}', zorder=3)

        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title(f"Metody numeryczne - funkcja {numer} dla a={a}, b={b}, epsilon={epsilon}")
        plt.legend()
        plt.grid()
        plt.show()