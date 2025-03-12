from rownania import Rownania
class Bisekcja:
    @staticmethod
    def metodaBisekcji(numer, a, b, epsilon):
        rownania_obj = Rownania()
        if rownania_obj.rownanie(numer, a) * rownania_obj.rownanie(numer, b) >= 0:
            raise ValueError("Funkcja musi zmieniać znak w podanym przedziale, tzn. f(a) * f(b) < 0.")
        x_poprzednie = None
        while abs(a - b) > epsilon:
            x1 = (a + b) / 2

            if x_poprzednie is not None and abs(x1-x_poprzednie) < epsilon:
                return x1
            elif rownania_obj.rownanie(numer, x1) * rownania_obj.rownanie(numer, a) < 0:
                b = x1
            else:
                a = x1
            x_poprzednie = x1
        return x1