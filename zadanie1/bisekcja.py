from rownania import Rownania
class Bisekcja:
    @staticmethod
    def metodaBisekcji(numer, a, b, epsilon, wariant='A', max_iter=100):
        rownania_obj = Rownania()
        if rownania_obj.rownanie(numer, a) * rownania_obj.rownanie(numer, b) >= 0:
            raise ValueError("Funkcja musi zmieniać znak w podanym przedziale, tzn. f(a) * f(b) < 0.")
        x_poprzednie = None
        iteracje = 0
        while abs(a - b) > epsilon:
            x1 = (a + b) / 2

            if abs(rownania_obj.rownanie(numer, x1)) < epsilon:
                return x1
            if wariant == 'A' and x_poprzednie is not None and abs(x1 - x_poprzednie) < epsilon:
                return x1
            iteracje+=1
            if wariant == 'B' and iteracje >= max_iter:
                return x1
            elif rownania_obj.rownanie(numer, x1) * rownania_obj.rownanie(numer, a) < 0:
                b = x1
            else:
                a = x1
            x_poprzednie = x1
        return x1