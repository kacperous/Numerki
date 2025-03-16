from zadanie1.bisekcja import Bisekcja
from siecznych import Siecznych
from rysuj import Wykres

def main():
    numer = int(input("Podaj numer funkcji (1-wielomianowa 2-trygonometryczna 3-wykładnicza 4-złożona): "))
    a = float(input("Podaj a: "))
    b = float(input("Podaj b: "))
    epsilon = float(input("Podaj dokładkość (epsilon): "))

    print("\nWybierz wariant stopu dla metody bisekcji:")
    print("A - Warunek stopu: |x_n - x_{n-1}| < epsilon")
    print("B - Warunek stopu: maksymalna liczba iteracji")
    wariant = input("Twój wybór (A/B): ").upper()

    max_iter = 100
    if wariant == 'B':
        max_iter = int(input("Podaj maksymalną liczbę iteracji: "))

    bisekcja = Bisekcja.metodaBisekcji(numer, a, b, epsilon, wariant, max_iter)
    sieczne = Siecznych.siecznych(a, b, numer, epsilon, wariant, max_iter)

    print(f"Znalezione miejsce zerowe metodą bisekcji: {bisekcja}")
    print(f"Znalezione miejsce zerowe metodą siecznych: {sieczne}")

    Wykres.rysuj_wykres(numer, a, b, bisekcja, sieczne, epsilon)

if __name__ == "__main__":
    main()






