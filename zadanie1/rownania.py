import math
class Rownania:
    def rownanie(self,numer,x):
        if numer == 1:
            return 2 * x ** 3 + 3 * x ** 2 + 1
        elif numer == 2:
            return math.cos(x)
        elif numer == 3:
            return 2 ** x - 2
        elif numer == 4:
            return (x**2 + 3*x + 2) * math.sin(x)
        else:
            return None
