import numpy as np

def wybierz_macierz():
    # Definiowanie macierzy
    macierze = {
        "a": (np.array([[3, 3, 1],
                        [2, 5, 7],
                        [1, 2, 1]], dtype=float),
              np.array([[12], [33], [8]], dtype=float)),

        "b": (np.array([[3, 3, 1],
                        [3, 5, 7],
                        [3, 7, 14]], dtype=float),
              np.array([[12], [20], [-40]], dtype=float)),

        "c": (np.array([[3, 3, 1],
                        [3, 5, 7],
                        [-4, -10, -14]], dtype=float),
              np.array([[12], [20], [45]], dtype=float)),

        "d": (np.array([[3, 3, 1],
                        [3, 5, 7],
                        [3, 7, 14]], dtype=float),
              np.array([[12], [20], [-20]], dtype=float)),

        "e": (np.array([[3, 2, -1],
                        [5, -1, 2],
                        [7, 8, -1]], dtype=float),
              np.array([[0], [2], [-7]], dtype=float)),

        "f": (np.array([[3, -1, 2, -1],
                        [3, -1, 1, 1],
                        [-1, -1, -2, 3]], dtype=float),
              np.array([[-13], [1], [-5]], dtype=float)),

        "g": (np.array([[0, 0, 1],
                        [1, 0, 0],
                        [0, 1, 0]], dtype=float),
              np.array([[3], [7], [5]], dtype=float)),

        "h": (np.array([[10, -5, 1],
                        [4, -7, 2],
                        [5, -2, 7]], dtype=float),
              np.array([[3], [-4], [19]], dtype=float)),

        "i": (np.array([[6, -4, 0],
                        [3, 0.9, 3.6],
                        [0, 0.9, 3.6]], dtype=float),
              np.array([[4], [11], [5]], dtype=float)),

        "j": (np.array([[1, 0.2, 0.3],
                        [0.1, -0.3, 0.2],
                        [-0.1, -0.2, 1]], dtype=float),
              np.array([[1.5], [0.8], [0.7]], dtype=float))
    }

    # Wybór macierzy
    wybor = input(f"Wybierz macierz ({', '.join(macierze.keys())}): ").strip().lower()

    if wybor in macierze:
        A, b = macierze[wybor]
        return A, b
    else:
        print("Nieprawidłowy wybór! Spróbuj ponownie.")
        return wybierz_macierz()
