import math
import app


class InvalidPermissions(Exception):
    pass


class Calculator:
    
    def add(self, x, y):
        self.check_types(x, y)
        return x + y

    def substract(self, x, y):
        try:
            self.check_types(x, y)
            return x - y
        except TypeError:
            return TypeError

    def multiply(self, x, y):
        try:
            self.check_types(x, y)
            return x * y
        except TypeError:
            return TypeError

    def divide(self, x, y):
        self.check_types(x, y)
        if y == 0:
            raise TypeError("No se puede dividir para cero")
        return x / y

    def power(self, x, y):
        try:
            self.check_types(x, y)
            return x ** y
        except TypeError:
                return TypeError
    
    def sqrt(self, a):
        try:
            self.check_types(a)
            if a < 0:
                return TypeError
            return a ** 0.5
        except TypeError:
            return TypeError
    
    def log10(self, a):
        try:
            self.check_types(a)
            import math
            return math.log10(a)
        except TypeError:
            return TypeError

    def check_types(self, *args):
        for value in args:
            if not isinstance(value, (int, float)):
                raise TypeError("Los parametros deben ser numeros")


if __name__ == "__main__":  # pragma: no cover
    calc = Calculator()
    result = calc.add(2, 2)
    print(result)
