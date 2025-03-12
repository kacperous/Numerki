from rownania import Rownania

class Siecznych:
    @staticmethod
    def siecznych(x1, x2, numer, tol=1e-5, max_iter=100):
        iteracja=0
        Xpoprzednie = x1
        X = x2

        rownania_obj = Rownania()
        while(iteracja<max_iter):
          wartosc1 = rownania_obj.rownanie(numer, Xpoprzednie)
          wartosc2 = rownania_obj.rownanie(numer, X)

          if wartosc1 == wartosc2:
              return None

          nachylenie = (wartosc2 - wartosc1) / (X - Xpoprzednie)

          nowyX= X - wartosc2/nachylenie
          if abs(nowyX-X) < tol or abs(wartosc2) < tol:
              return nowyX
          Xpoprzednie=X
          X=nowyX
          iteracja += 1

        return None