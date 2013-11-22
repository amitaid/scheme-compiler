from reader import pSexpr


class AbstractSexpr:
    def get_value(self):
        pass

    @staticmethod
    def readFromString(sexpr_str):
        return pSexpr.match(sexpr_str)


class Void(AbstractSexpr):
    pass


class Nil(AbstractSexpr):
    def __str__(self):
        return '()'

    def get_value(self):
        return None


class Boolean(AbstractSexpr):
    def __init__(self, value):
        self.value = value == 't'

    def __str__(self):
        return str(self.value)

    def get_value(self):
        return self.value


class Char(AbstractSexpr):
    def __init__(self, ch):
        self.value = ch

    def __str__(self):
        return str(self.value)

    def get_value(self):
        return self.value


class AbstractNumber(AbstractSexpr):
    def eval(self):
        pass


class Integer(AbstractNumber):
    def __init__(self, value):
        self.value = int(value, 0)

    def __str__(self):
        return str(self.value)

    def eval(self):
        return self.value

    def get_value(self):
        return self.eval()


class Fraction(AbstractNumber):
    def __init__(self, numer, denum):
        self.numer, self.denum = numer, denum

    def __str__(self):
        return str(self.numer) + '/' + str(self.denum)

    def eval(self):
        return self.numer.eval() / self.denum.eval()

    def get_value(self):
        return self.eval()


class String(AbstractSexpr):
    def __init__(self, chars):
        self.value = chars

    def __str__(self):
        return '"' + self.value + '"'

    def get_value(self):
        return self.value


class Symbol(AbstractSexpr):
    def __init__(self, symbol_str):
        self.value = symbol_str
        self.length = len(symbol_str)

    def __str__(self):
        return self.value

    def get_value(self):
        return self.value


class Pair(AbstractSexpr):
    def __init__(self, car, cdr):
        self.car = car
        if len(cdr) == 1:
            self.cdr = cdr[0]
        else:
            self.cdr = Pair(cdr[0], cdr[1:])

    def __str__(self):
        return '(' + self._inner_str() + ')'

    def _inner_str(self):
        res = str(self.car)
        if isinstance(self.cdr, Nil):
            pass
        elif isinstance(self.cdr, Pair):
            res += ' ' + self.cdr._inner_str()
        else:
            res += ' . ' + str(self.cdr)
        return res

    def get_value(self):
        return (self.car, self.cdr)

    def get_car(self):
        return self.car

    def get_cdr(self):
        return self.cdr


class Vector(AbstractSexpr):
    def __init__(self, items):
        self.value = items

    def __str__(self):
        return '#(' + ' '.join(map(str, self.value)) + ')'

    def get_value(self):
        return self.value