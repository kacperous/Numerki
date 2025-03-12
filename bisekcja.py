class Bisekcja:
    @staticmethod
    def metodaBisekcji(f, a, b, epsilon):
        if f(a) * f(b) >= 0:
            raise ValueError("Funkcja musi zmieniać znak w podanym przedziale, tzn. f(a) * f(b) < 0.")
        x_poprzednie = a
        while abs(a - b) > epsilon:
            x1 = (a + b) / 2

            if abs(x1-x_poprzednie) < epsilon:
                return x1
            elif f(x1) * f(a) < 0:
                b = x1
            else:
                a = x1
            x_poprzednie = x1
        return (a + b) / 2