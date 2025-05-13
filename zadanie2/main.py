from matrix import wybierz_macierz
from GaussSeidel import gauss_seidel
import numpy as np

def main():
    A, b = wybierz_macierz()

    print("\nWybrana macierz A:")
    print(A)
    print("\nWektor wyrazów wolnych b:")
    print(b)

    print("\nWybierz warunek stopu:")
    print("1. Dokładność (epsilon)")
    print("2. Liczba iteracji")

    try:
        wybor_stopu = int(input("Twój wybór (1 lub 2): "))

        epsilon = None
        max_iteracji = None

        if wybor_stopu == 1:
            epsilon = float(input("Podaj dokładność (np. 0.0001): "))
        elif wybor_stopu == 2:
            max_iteracji = int(input("Podaj maksymalną liczbę iteracji: "))
        else:
            print("Nieprawidłowy wybór. Wybrano domyślnie dokładność 0.0001.")
            epsilon = 0.0001

        x, iteracje, zbieznosc = gauss_seidel(A, b, epsilon, max_iteracji)

        print("\nWyniki:")
        print(f"Wykonano {iteracje} iteracji.")

        det_A = np.linalg.det(A)
        if abs(det_A) < 1e-10:
            ranga_A = np.linalg.matrix_rank(A)
            ranga_Ab = np.linalg.matrix_rank(np.column_stack((A, b)))

            if ranga_A != ranga_Ab:
                print("Układ równań jest sprzeczny.")
            else:
                print("Układ równań jest nieoznaczony.")
        else:
            if zbieznosc:
                print("Metoda zbiegła do rozwiązania.")
            else:
                print("Metoda nie zbiegła do żądanej dokładności.")

            print("\nRozwiązanie:")
            for i, xi in enumerate(x):
                print(f"x{i+1} = {xi:.8f}")

    except ValueError:
        print("Błąd: Wprowadzono nieprawidłowe dane.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    main()