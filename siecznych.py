import rownanie from rownania

def siecznych(x1, x2, tol=1e-6, max_iter=100):
    iteracja=0
    Xpoprzednie = x1
    X = x2
    while(iteracja<max_iter):
      wartosc1 = rownanie(numer,Xpoprzednie)
      wartosc2 = rownanie(numer,X)

      nachylenie = (wartosc1 - wartosc2)/(wartosc1 - wartosc2)
      nowyX=x2-wartosc1/nachylenie
      if(nowyX- X)< tol or abs(wartosc2)<tol:
          return nowyX
      Xpoprzednie=X
      X=nowyX
    return None