from matrix import wybierz_macierz
from GaussSeidel import calculate

A, b = wybierz_macierz()
print("\nMacierz współczynników A:")
print(A)
print("\nWektor b:")
print(b)
calculate(A, b)

