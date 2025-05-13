import numpy as np

def gauss_seidel(A, b, epsilon=None, max_iteracji=None):
    n = len(A)
    x = np.zeros(n)

    diag_dominacja = True
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            diag_dominacja = False
            break

    if not diag_dominacja:
        print("Ostrzeżenie: Macierz może nie spełniać warunku zbieżności metody Gaussa-Seidla.")

    iteracje = 0
    zbieznosc = False

    while True:
        x_poprzednie = x.copy()

        for i in range(n):
            suma1 = sum(A[i, j] * x[j] for j in range(i))
            suma2 = sum(A[i, j] * x_poprzednie[j] for j in range(i+1, n))

            if A[i, i] == 0:
                print("Błąd: Element na przekątnej jest równy zero.")
                return x, iteracje, False

            x[i] = (b[i] - suma1 - suma2) / A[i, i]

        iteracje += 1

        blad = np.linalg.norm(x - x_poprzednie)

        if epsilon is not None and blad < epsilon:
            zbieznosc = True
            break

        if max_iteracji is not None and iteracje >= max_iteracji:
            break

        if np.isnan(blad) or np.isinf(blad):
            print("Błąd: Metoda nie zbiega.")
            return x, iteracje, False

    return x, iteracje, zbieznosc