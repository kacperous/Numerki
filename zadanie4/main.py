import math
import sys

def f1(x):
  """f(x) = 1. Całka[0, inf] exp(-x)*1 dx = 1"""
  return 1.0

def f2(x):
  """f(x) = x. Całka[0, inf] exp(-x)*x dx = 1"""
  return x

def f3(x):
  """f(x) = x^2. Całka[0, inf] exp(-x)*x^2 dx = 2"""
  return x**2

def f4(x):
  """f(x) = sin(x). Całka[0, inf] exp(-x)*sin(x) dx = 0.5"""
  return math.sin(x)

FUNKCJE = {
    1: {'func': f1, 'desc': "f(x) = 1", 'latex': "1"},
    2: {'func': f2, 'desc': "f(x) = x", 'latex': "x"},
    3: {'func': f3, 'desc': "f(x) = x^2", 'latex': "x^2"},
    4: {'func': f4, 'desc': "f(x) = sin(x)", 'latex': "\\sin(x)"}
}

def segment_simpsona(g, a, b, n):
  """
    Oblicza całkę funkcji g(x) na przedziale [a, b] używając metody Simpsona
    z n podprzedziałami.
    Argumenty:
        g (callable): Funkcja do scałkowania (musi być postaci exp(-x)*f(x)).
        a (float): Dolna granica przedziału.
        b (float): Górna granica przedziału.
        n (int): Liczba podprzedziałów (MUSI być parzysta i dodatnia).
    Zwraca:
        float: Przybliżona wartość całki.
    """
  if n % 2 != 0 or n <= 0:
    raise ValueError("Liczba podprzedziałów n musi być dodatnią liczbą parzystą.")
  if a > b:
      a, b = b, a
  if a == b:
      return 0.0

  h = (b - a) / n
  calka = g(a) + g(b)

  for i in range(1, n, 2):
    try:
        calka += 4 * g(a + i * h)
    except (ValueError, OverflowError):
        print(f"Ostrzeżenie: Potencjalny problem numeryczny przy obliczaniu g({a + i * h}). Pomijanie składnika.")
        return float('nan')

  for i in range(2, n - 1, 2):
     try:
        calka += 2 * g(a + i * h)
     except (ValueError, OverflowError):
        print(f"Ostrzeżenie: Potencjalny problem numeryczny przy obliczaniu g({a + i * h}). Pomijanie składnika.")
        return float('nan')

  return (h / 3.0) * calka

def iteracyjna_metoda_simpsona(g, a, b, epsilon, max_iter_podzialu=20):
    """
    Oblicza całkę funkcji g(x) na przedziale [a, b] iteracyjnie, używając metody Simpsona,
    aż do osiągnięcia żądanej dokładności 'epsilon' pomiędzy iteracjami.
    Argumenty:
        g (callable): Funkcja do scałkowania (musi być postaci exp(-x)*f(x)).
        a (float): Dolna granica przedziału.
        b (float): Górna granica przedziału.
        epsilon (float): Żądana dokładność (różnica między kolejnymi iteracjami).
        max_iter_podzialu (int): Maksymalna liczba podwojeń podziału, aby zapobiec nieskończonym pętlom.
    Zwraca:
        float: Przybliżona wartość całki.
    """
    if epsilon <= 0:
        raise ValueError("Epsilon musi być dodatnie.")
    if a == b:
        return 0.0

    n = 2
    calka_poprzednia = segment_simpsona(g, a, b, n)
    if math.isnan(calka_poprzednia): return float('nan')

    for licznik_iter in range(max_iter_podzialu):
        n *= 2
        calka_biezaca = segment_simpsona(g, a, b, n)
        if math.isnan(calka_biezaca): return float('nan')

        if abs(calka_biezaca - calka_poprzednia) < epsilon:
            return calka_biezaca

        calka_poprzednia = calka_biezaca
    else:
        print(f"Ostrzeżenie: Iteracyjna metoda Simpsona na [{a},{b}] nie osiągnęła zbieżności w ciągu {max_iter_podzialu} podwojeń podziału (n={n}).")
        print(f"         Ostatnia różnica wynosiła {abs(calka_biezaca - calka_poprzednia)}. Zwracanie ostatniej obliczonej wartości.")
        return calka_biezaca

def simpson_granica_nieskonczona(f, epsilon, poczatkowa_gorna_granica=10.0, delta=5.0, max_iter_nieskonczona=1000):
    """
    Oblicza całkę funkcji exp(-x)*f(x) od 0 do +nieskończoności używając
    złożonej metody Simpsona z iteracyjnym rozszerzaniem granicy całkowania.
    Argumenty:
        f (callable): Oryginalna funkcja f(x).
        epsilon (float): Żądana dokładność. Proces zatrzymuje się, gdy całka
                         na ostatnim segmencie [a, a+delta] jest mniejsza od epsilon.
        poczatkowa_gorna_granica (float): Początkowa górna granica dla pierwszego segmentu [0, a].
        delta (float): Rozmiar kroku do rozszerzania górnej granicy.
        max_iter_nieskonczona (int): Maksymalna liczba iteracji rozszerzania granicy.
    Zwraca:
        float: Przybliżona wartość całki ∫[0, inf] exp(-x)*f(x) dx.
    """
    def g(x):
        try:
            if x < -700:
                return 0.0
            return math.exp(-x) * f(x)
        except (ValueError, OverflowError) as e:
             print(f"Błąd podczas obliczania exp(-{x})*f({x}): {e}")
             return float('nan')

    calka_calkowita = 0.0
    biezace_a = 0.0
    kolejne_a = poczatkowa_gorna_granica

    epsilon_segmentu = epsilon / 10.0

    print(f"\nObliczanie całki Simpsona ∫[0, ∞) e^(-x) * f(x) dx z ε = {epsilon:.2e}")
    print(f"Segment początkowy: [0, {poczatkowa_gorna_granica:.1f}], Δ = {delta:.1f}")

    print(f"Całkowanie segmentu [{biezace_a:.2f}, {kolejne_a:.2f}]...")
    calka_segmentu = iteracyjna_metoda_simpsona(g, biezace_a, kolejne_a, epsilon_segmentu)
    if math.isnan(calka_segmentu):
         print(f"Błąd: Nie udało się obliczyć całki na początkowym segmencie [{biezace_a:.2f}, {kolejne_a:.2f}]. Przerywanie.")
         return float('nan')
    print(f"Całka na segmencie [{biezace_a:.2f}, {kolejne_a:.2f}] ≈ {calka_segmentu:.6e}")
    calka_calkowita += calka_segmentu
    biezace_a = kolejne_a

    for iter_inf in range(max_iter_nieskonczona):
        kolejne_a = biezace_a + delta
        print(f"Całkowanie segmentu [{biezace_a:.2f}, {kolejne_a:.2f}]...")

        calka_segmentu = iteracyjna_metoda_simpsona(g, biezace_a, kolejne_a, epsilon_segmentu)
        if math.isnan(calka_segmentu):
            print(f"Błąd: Nie udało się obliczyć całki na segmencie [{biezace_a:.2f}, {kolejne_a:.2f}]. Przerywanie.")
            return float('nan')

        print(f"Całka na segmencie [{biezace_a:.2f}, {kolejne_a:.2f}] ≈ {calka_segmentu:.6e}")

        if abs(calka_segmentu) < epsilon:
            print(f"Zatrzymanie: |Całka na ostatnim segmencie| ({abs(calka_segmentu):.2e}) < ε ({epsilon:.2e}).")
            break

        calka_calkowita += calka_segmentu
        biezace_a = kolejne_a

    else:
        print(f"\nOstrzeżenie: Osiągnięto maksymalną liczbę iteracji ({max_iter_nieskonczona}) dla granicy nieskończonej w metodzie Simpsona.")
        print(f"         Całka może być niekompletna. Ostatni segment: [{biezace_a - delta:.2f}, {biezace_a:.2f}].")
        print(f"         Całka na ostatnim segmencie wynosiła {calka_segmentu:.6e}.")

    print(f"Końcowy wynik metody Simpsona ≈ {calka_calkowita:.8f}")
    return calka_calkowita

DANE_GAUSSA_LAGUERREA = {
    2: {
        'nodes': [0.5857864376269049, 3.414213562373095],
        'weights': [0.8535533905932737, 0.14644660940672622]
    },
    3: {
        'nodes': [0.4157745567834791, 2.294280360279042, 6.289945082937479],
        'weights': [0.7110930099291733, 0.2785177335667594, 0.01038925650397849]
    },
    4: {
        'nodes': [0.3225476896192245, 1.7457611011583466, 4.536620296921129, 9.395070912301299],
        'weights': [0.6031541043416596, 0.3574186924377997, 0.03888790851500538, 0.000539294705561327]
    },
    5: {
        'nodes': [0.2635603197181408, 1.4134030591065147, 3.596425771040722, 7.08581000585883, 12.640800844275782],
        'weights': [0.5217556105828084, 0.3986668110831759, 0.0759424496817076, 0.00361175867992204, 0.000023369972385783]
    }
}

def gauss_laguerre(f, n):
    """
    Oblicza całkę funkcji exp(-x)*f(x) od 0 do +nieskończoności używając
    kwadratury Gaussa-Laguerre'a z n węzłami.
    Argumenty:
        f (callable): Oryginalna funkcja f(x).
        n (int): Liczba węzłów (musi być 2, 3, 4 lub 5).
    Zwraca:
        float: Przybliżona wartość całki ∫[0, inf] exp(-x)*f(x) dx.
    """
    if n not in DANE_GAUSSA_LAGUERREA:
        raise ValueError("Liczba węzłów n dla kwadratury Gaussa-Laguerre'a musi wynosić 2, 3, 4 lub 5.")

    wezly = DANE_GAUSSA_LAGUERREA[n]['nodes']
    wagi = DANE_GAUSSA_LAGUERREA[n]['weights']

    calka = 0.0
    print(f"\nObliczanie kwadratury Gaussa-Laguerre'a ∫[0, ∞) e^(-x) * f(x) dx z n = {n} węzłami:")
    for i in range(n):
        try:
            f_w_wezle = f(wezly[i])
            skladnik = wagi[i] * f_w_wezle
            print(f"  Węzeł {i+1}: x = {wezly[i]:.6f}, w = {wagi[i]:.6e}, f(x) = {f_w_wezle:.6e}, składnik = {skladnik:.6e}")
            calka += skladnik
        except (ValueError, OverflowError) as e:
            print(f"Błąd podczas obliczania f({wezly[i]}) dla kwadratury Gaussa-Laguerre'a: {e}")
            return float('nan') # Sygnalizacja błędu

    print(f"Końcowy wynik kwadratury Gaussa-Laguerre'a (n={n}) ≈ {calka:.8f}")
    return calka


def main():
    print("Program do Całkowania Numerycznego")
    print("Oblicza całkę ∫[0, ∞) e^(-x) * f(x) dx używając:")
    print("1. Złożonej metody Simpsona (Iteracyjnie)")
    print("2. Kwadratury Gaussa-Laguerre'a")
    print("-" * 30)

    print("Dostępne funkcje f(x):")
    for klucz, wartosc in FUNKCJE.items():
        print(f"  {klucz}: {wartosc['desc']}")

    while True:
        try:
            wybor = int(input("Wybierz funkcję (1-4): "))
            if wybor in FUNKCJE:
                wybrana_f = FUNKCJE[wybor]['func']
                wybrany_opis = FUNKCJE[wybor]['desc']
                print(f"Wybrano funkcję: {wybrany_opis}")
                break
            else:
                print("Nieprawidłowy wybór. Proszę podać liczbę od 1 do 4.")
        except ValueError:
            print("Nieprawidłowe dane wejściowe. Proszę podać liczbę.")

    while True:
        try:
            epsilon_str = input(f"Podaj żądaną dokładność ε dla metody Simpsona (np. 1e-6): ")
            epsilon = float(epsilon_str)
            if epsilon > 0:
                break
            else:
                print("Dokładność ε musi być liczbą dodatnią.")
        except ValueError:
            print("Nieprawidłowe dane wejściowe. Proszę podać poprawną liczbę zmiennoprzecinkową (np. 0.00001 lub 1e-5).")

    while True:
        try:
            n_gauss_str = input("Podaj liczbę węzłów dla kwadratury Gaussa-Laguerre'a (2, 3, 4 lub 5): ")
            n_gauss = int(n_gauss_str)
            if n_gauss in DANE_GAUSSA_LAGUERREA:
                break
            else:
                print("Nieprawidłowy wybór. Proszę podać 2, 3, 4 lub 5.")
        except ValueError:
            print("Nieprawidłowe dane wejściowe. Proszę podać liczbę całkowitą.")

    print("-" * 30)
    print(f"Obliczanie całki dla f(x) = {wybrany_opis}")
    print("-" * 30)

    wynik_simpsona = simpson_granica_nieskonczona(wybrana_f, epsilon)
    wynik_gaussa = gauss_laguerre(wybrana_f, n_gauss)

    print("-" * 30)
    print("--- Podsumowanie Wyników ---")
    print(f"Funkcja f(x): {wybrany_opis}")
    print(f"Całka: ∫[0, ∞) e^(-x) * f(x) dx")
    print("-" * 30)
    if not math.isnan(wynik_simpsona):
        print(f"Wynik metody Simpsona (ε ≈ {epsilon:.1e}): {wynik_simpsona:.8f}")
    else:
        print(f"Wynik metody Simpsona (ε ≈ {epsilon:.1e}): Obliczenia nie powiodły się")

    if not math.isnan(wynik_gaussa):
        print(f"Wynik Gaussa-Laguerre'a (n = {n_gauss}):    {wynik_gaussa:.8f}")
    else:
         print(f"Wynik Gaussa-Laguerre'a (n = {n_gauss}):    Obliczenia nie powiodły się")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDziałanie anulowane przez użytkownika.")
        sys.exit(0)
    except Exception as e:
        print(f"\nWystąpił nieoczekiwany błąd: {e}")
        sys.exit(1)