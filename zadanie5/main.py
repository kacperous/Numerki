import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite

# ========= SCHEMAT HORNERA ========
def horner(coeffs, x):
    res = np.zeros_like(x, dtype=float)
    if np.isscalar(x):
        x_arr = np.array([x])
        res_arr = np.zeros_like(x_arr, dtype=float)
        temp = coeffs[0]
        for c_idx in range(1, len(coeffs)):
            temp = temp * x_arr[0] + coeffs[c_idx]
        res_arr[0] = temp
        return res_arr[0]
    else:
        x_arr = np.array(x)
        res = np.zeros_like(x_arr, dtype=float)
        for i_val, val in enumerate(x_arr):
            temp = coeffs[0]
            for c_coeff in coeffs[1:]:
                temp = temp * val + c_coeff
            res[i_val] = temp
        return res


# ----------- FUNKCJE DO WYBORU -----------------
def f_linear(x): return x


def f_abs(x): return np.abs(x)


def f_polynomial(x, coeffs_poly): return horner(coeffs_poly, x)


def f_trig(x, a_param, b_param, c_param): return a_param * np.sin(b_param * x + c_param)


def f_composite(x): return np.abs(x) * np.cos(x)


# --------- METODA CAŁKOWANIA SIMPSONA (ZASTĘPUJE TRAPEZOWĄ) ----------
def integrate_simpson(func_to_integrate, interval_a, interval_b, num_subintervals):
    if num_subintervals % 2 != 0 or num_subintervals <= 0:
        raise ValueError("Liczba podprzedziałów dla Simpsona musi być dodatnią liczbą parzystą.")

    if interval_a == interval_b:
        return 0.0

    actual_a = interval_a
    actual_b = interval_b
    sign = 1.0
    if interval_a > interval_b:
        actual_a = interval_b
        actual_b = interval_a
        sign = -1.0

    h = (actual_b - actual_a) / num_subintervals
    integral_val = func_to_integrate(actual_a) + func_to_integrate(actual_b)

    for i in range(1, num_subintervals, 2):
        try:
            integral_val += 4 * func_to_integrate(actual_a + i * h)
        except (ValueError, OverflowError) as e:
            print(
                f"Ostrzeżenie (Simpson): Problem numeryczny przy func_to_integrate({actual_a + i * h:.4f}). {e}. Zwracam NaN.")
            return float('nan')

    for i in range(2, num_subintervals - 1, 2):
        try:
            integral_val += 2 * func_to_integrate(actual_a + i * h)
        except (ValueError, OverflowError) as e:
            print(
                f"Ostrzeżenie (Simpson): Problem numeryczny przy func_to_integrate({actual_a + i * h:.4f}). {e}. Zwracam NaN.")
            return float('nan')

    return sign * (h / 3.0) * integral_val


# --------- OBLICZANIE HERMITE'A POPRZEZ HORNERA ----------
def hermite_basis_horner(degree):
    basis = []
    for n_deg in range(degree + 1):
        h_poly = hermite(n_deg)
        coeffs_h = h_poly.c

        def phi(x, cs=coeffs_h): return horner(cs, x)

        basis.append(phi)
    return basis


# --------- WSPÓŁCZYNNIKI APROKSYMOWANEJ FUNKCJI (ITERACYJNIE) ----------
def compute_hermite_coeffs(f_orig, basis_funcs, a_interval, b_interval, n_simpson_subintervals=250):
    coeffs_approx = []
    for phi_k in basis_funcs:
        def numf(x):
            return f_orig(x) * phi_k(x) * np.exp(-x ** 2)

        def denomf(x):
            return phi_k(x) ** 2 * np.exp(-x ** 2)

        num = integrate_simpson(numf, a_interval, b_interval, n_simpson_subintervals)
        denom = integrate_simpson(denomf, a_interval, b_interval, n_simpson_subintervals)

        if np.isnan(num) or np.isnan(denom):
            print(f"Błąd: Całkowanie dla współczynnika alpha_{len(coeffs_approx)} zwróciło NaN. Ustawiam na 0.")
            coeffs_approx.append(0.0)
            continue

        coeffs_approx.append(num / denom if denom != 0 else 0.0)
    return coeffs_approx


def hermite_approx_function(x_vals, coeffs_alpha, basis_funcs):
    res_approx = np.zeros_like(x_vals, dtype=float)
    for alpha_k, phi_k in zip(coeffs_alpha, basis_funcs):
        res_approx += alpha_k * phi_k(x_vals)
    return res_approx


def approx_error(f_orig, f_approx_func, a_interval, b_interval, n_error_pts=1000):
    x_pts = np.linspace(a_interval, b_interval, n_error_pts)
    err_sq = (f_orig(x_pts) - f_approx_func(x_pts)) ** 2
    if a_interval == b_interval or len(x_pts) < 2: return 0.0
    return np.sqrt(np.trapezoid(err_sq, x_pts) / (b_interval - a_interval))


def choose_function():
    print("Wybierz funkcję do aproksymacji:")
    functions = [
        ("Liniowa        f(x) = x", lambda x_val: f_linear(x_val)),
        ("Wartość bezwzględna f(x) = |x|", lambda x_val: f_abs(x_val)),
        ("Wielomian      f(x) = ax^2 + bx + c", "polynomial_input"),  # Zachowano oryginalny opis
        ("Trygonometryczna f(x) = a*sin(bx+c)", "trigonometric_input"),
        ("Złożona        f(x) = |x|*cos(x)", lambda x_val: f_composite(x_val))
    ]
    for i, (desc, _) in enumerate(functions):
        print(f"{i}. {desc}")

    idx = -1
    while True:
        try:
            idx = int(input(f"Twój wybór [0-{len(functions) - 1}]: "))
            if 0 <= idx < len(functions):
                break
            else:
                print("Niepoprawny wybór, spróbuj ponownie.")
        except ValueError:
            print("Proszę podać liczbę.")

    selected_option = functions[idx][1]
    f_selected = None

    if selected_option == "polynomial_input":
        print("Podaj współczynniki wielomianu f(x) = a*x^2 + b*x + c:")
        a_poly = float(input("a: "))
        b_poly = float(input("b: "))
        c_poly = float(input("c: "))
        f_selected = lambda x_val: f_polynomial(x_val, [a_poly, b_poly, c_poly])
    elif selected_option == "trigonometric_input":
        print("Podaj parametry f(x) = a*sin(bx + c):")
        a_trig = float(input("a: "))
        b_trig = float(input("b: "))
        c_trig = float(input("c: "))
        f_selected = lambda x_val: f_trig(x_val, a_trig, b_trig, c_trig)
    else:
        f_selected = selected_option
    return f_selected


def main():
    print("--- Aproksymacja Hermite'a (z całkowaniem Simpsona) ---")
    f_to_approx = choose_function()

    a_main = float(input("Przedział aproksymacji: poczatek: "))
    b_main = float(input("Przedział aproksymacji: koniec: "))
    if a_main == b_main:
        print("Błąd: Przedział aproksymacji nie może mieć zerowej długości.")
        return

    n_simpson_subintervals = 0
    while True:
        try:
            n_simpson_subintervals = int(
                input("Liczba podprzedziałów do całkowania Simpsona (parzysta, np. 100-400): "))
            if n_simpson_subintervals > 0 and n_simpson_subintervals % 2 == 0:
                break
            else:
                print("Liczba podprzedziałów musi być dodatnia i parzysta. Spróbuj ponownie.")
        except ValueError:
            print("Niepoprawna wartość, proszę podać liczbę całkowitą.")

    auto_mode = input("Tryb automatycznego doboru stopnia? (t/n): ").strip().lower() == 't'

    final_coeffs = None
    final_approx_func = None
    final_degree = 0

    if auto_mode:
        eps = float(input("Podaj żądany błąd aproksymacji: "))
        max_degree = int(input("Maksymalny testowany stopień (np. 20): "))
        achieved_target_error = False
        last_error = float('inf')

        for deg in range(1, max_degree + 1):
            print(f"\nTestowanie stopnia {deg}...")
            basis = hermite_basis_horner(deg)
            current_coeffs = compute_hermite_coeffs(f_to_approx, basis, a_main, b_main, n_simpson_subintervals)

            if any(np.isnan(c) for c in current_coeffs):
                print(f"Błąd całkowania przy stopniu {deg}. Przerywam tryb automatyczny.")
                break

            current_f_approx = lambda x_val: hermite_approx_function(x_val, current_coeffs, basis)
            error = approx_error(f_to_approx, current_f_approx, a_main, b_main)
            print(f"Stopień: {deg}, błąd: {error:.6e}")

            final_coeffs = current_coeffs
            final_approx_func = current_f_approx
            final_degree = deg
            last_error = error

            if error < eps:
                print(f"Osiągnięto żądany błąd ({error:.3g}) dla stopnia {deg}")
                achieved_target_error = True
                break
        if not achieved_target_error and final_approx_func:
            print(
                f"Nie osiągnięto żądanego błędu do stopnia {max_degree}. Używam ostatniego: stopień {final_degree}, błąd {last_error:.3g}")
        elif not final_approx_func:
            print("Nie udało się wygenerować aproksymacji w trybie automatycznym z powodu błędów całkowania.")
            return


    else:
        deg_manual = int(input("Podaj stopień wielomianu aproksymującego: "))
        final_degree = deg_manual
        basis = hermite_basis_horner(deg_manual)
        final_coeffs = compute_hermite_coeffs(f_to_approx, basis, a_main, b_main, n_simpson_subintervals)

        if any(np.isnan(c) for c in final_coeffs):
            print("Błąd całkowania przy obliczaniu współczynników. Nie można kontynuować.")
            return

        final_approx_func = lambda x_val: hermite_approx_function(x_val, final_coeffs, basis)
        error = approx_error(f_to_approx, final_approx_func, a_main, b_main)
        print(f"Błąd aproksymacji (średniokwadratowy): {error:.6e}")

    if final_approx_func is None:
        print("Nie udało się wyznaczyć funkcji aproksymującej.")
        return

    # ---- Wykresy ----
    xvals = np.linspace(a_main, b_main, 1000)
    plt.plot(xvals, f_to_approx(xvals), label="Funkcja oryginalna")
    plt.plot(xvals, final_approx_func(xvals), label="Aproksymacja Hermite'a")
    plt.title("Aproksymacja funkcji wielomianami Hermite'a")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid()
    plt.show()

    # ---- Współczynniki ----
    print("Współczynniki wielomianu aproksymacyjnego (alfa_k):")
    for i, c in enumerate(final_coeffs):
        print(f"a_{i} = {c:.6g}")


if __name__ == "__main__":
    main()
