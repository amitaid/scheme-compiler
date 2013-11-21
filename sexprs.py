from reader import pSexpr


class AbstractSexpr:
    def __str__(self):
        pass

    @staticmethod
    def readFromString(sexpr_str):
        return pSexpr.match(sexpr_str)


class Void(AbstractSexpr):
    pass


class Nil(AbstractSexpr):
    def __str__(self):
        return '()'


class Boolean(AbstractSexpr):
    def __init__(self, value):
        self.value = value == 't'

    def __str__(self):
        return str(self.value)


class Char(AbstractSexpr):
    def __init__(self, ch):
        self.ch = ch

    def __str__(self):
        return str(self.ch)


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


class Fraction(AbstractNumber):
    def __init__(self, numer, denum):
        self.numer, self.denum = numer, denum

    def __str__(self):
        return str(self.numer) + '/' + str(self.denum)

    def eval(self):
        return self.numer.eval() / self.denum.eval()


class String(AbstractSexpr):
    def __init__(self, chars):
        self.chars = chars

    def __str__(self):
        return '"' + self.chars + '"'


class Symbol(AbstractSexpr):
    def __init__(self, symbol_str):
        self.symbol = symbol_str
        self.length = len(symbol_str)

    def __str__(self):
        return self.symbol


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


class Vector(AbstractSexpr):
    def __init__(self, items):
        self.items = items

    def __str__(self):
        return '#(' + ' '.join(map(str, self.items)) + ')'

