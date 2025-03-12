from bisekcja import Bisekcja
from siecznych import Siecznych
from rownania import Rownania
from rysuj import Wykres

def main():
    numer = int(input("Podaj numer funkcji (1-wielomianowa 2-trygonometryczna 3-wykładnicza 4-złożona): "))
    a = float(input("Podaj a: "))
    b = float(input("Podaj b: "))
    epsilon = float(input("Podaj dokładkość (epsilon): "))

    rownania_obj = Rownania()

    if rownania_obj.rownanie(numer, a) * rownania_obj.rownanie(numer, b) >= 0:
        print("Błąd: Funkcja nie zmienia znaku na podanym przedziale dla metody bisekcji.")
        return

    bisekcja = Bisekcja.metodaBisekcji(numer, a, b, epsilon)
    sieczne = Siecznych.siecznych(a, b, numer)

    print(f"Znalezione miejsce zerowe metodą bisekcji: {bisekcja}")
    print(f"Znalezione miejsce zerowe metodą siecznych: {sieczne}")

    Wykres.rysuj_wykres(numer, a, b, bisekcja, sieczne, epsilon)

if __name__ == "__main__":
    main()






