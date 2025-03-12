import math
from bisekcja import Bisekcja




def f(x):
    return x ** 3 - x - 2

def main():
    bisekcja = Bisekcja.metodaBisekcji(f, a=1, b=2, epsilon=1e-5)
    print(f"Znalezione miejsce zerowe: {bisekcja}")


if __name__ == "__main__":
    main()






