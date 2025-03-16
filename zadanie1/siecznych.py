from zadanie1.rownania import Rownania

class Siecznych:
    @staticmethod
    def siecznych(x1, x2, numer, epsilon, wariant = 'A', max_iter=100):
        iteracja=0
        Xpoprzednie = x1
        X = x2

        rownania_obj = Rownania()
        while True:
            if wariant == 'B' and iteracja >= max_iter:
                return X

            wartosc1 = rownania_obj.rownanie(numer, Xpoprzednie)
            wartosc2 = rownania_obj.rownanie(numer, X)

            if wartosc1 == wartosc2:
                return None

            nachylenie = (wartosc2 - wartosc1) / (X - Xpoprzednie)
            nowyX = X - wartosc2 / nachylenie

            if wariant == 'A' and abs(nowyX - X) < epsilon:
                return nowyX

            Xpoprzednie = X
            X = nowyX
            iteracja += 1

            if wariant == 'A' and iteracja >= 1000:
                return None