import numpy as np

def calculate(A, b):
    matrixA = A.copy()
    matrixB = b.copy()
    n = len(matrixA)

    print("-------------------")
    print("Macierz początkowa:")
    print(matrixA)
    print("Wektor początkowy:")
    print(matrixB)

    numer = 0
    value = 0
    multiplier = []

    for i in range(n - 1):
        for k in range(i + 1, n):
            print(matrixA[i][i], matrixA[k][i])
            if matrixA[k][i] != 0:
                value = matrixA[k][i] / matrixA[i][i]
                multiplier.append(float(value))
                print(f"Appending {value:.4f} to multiplier")

                for j in range(i, n):
                    matrixA[k][j] -= value * matrixA[i][j]

                matrixB[k][0] -= value * matrixB[i][0]

        print("Macierz po kroku eliminacji:")
        print(matrixA)
        print("Wektor b po kroku eliminacji:")
        print(matrixB)
        print("-------------------")

    print("Lista mnożników:")
    print(multiplier)

    x = np.zeros((n, 1))
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += matrixA[i][j] * x[j][0]
        x[i][0] = (matrixB[i][0] - suma) / matrixA[i][i]

    print("Rozwiązania:")
    print(x)
    return x
