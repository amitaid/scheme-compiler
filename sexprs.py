import pc
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
        try:
            self.value = int(value, 0)
        except ValueError:
            raise pc.NoMatch

    def __str__(self):
        return str(self.value)

    def eval(self):
        return self.value

    def negate(self):
        self.value = -self.value
        return self


class Fraction(AbstractNumber):
    def __init__(self, numer, denum):
        self.numer, self.denum = numer.eval(), denum.eval()
        if self.denum == 0:
            raise pc.NoMatch('Divide by zero')

    def __str__(self):
        return str(self.numer) + '/' + str(self.denum)

    def eval(self):
        return self.numer.eval() / self.denum.eval()


class String(AbstractSexpr):
    def __init__(self, chars):
        self.chars = chars

    def __str__(self):
        return '"' + ''.join(self.chars) + '"'


class Symbol(AbstractSexpr):
    def __init__(self, symbol_str):
        self.symbol = symbol_str
        self.length = len(symbol_str)

    def __str__(self):
        return self.symbol


class Pair(AbstractSexpr):
    def __init__(self, items):
        self.str_form = '(' + ' '.join(map(str, items)) + ')'
        self.car = items[0]
        if len(items[1:]) == 0:
            self.cdr = Nil()
        elif len(items[1:]) == 1:
            self.cdr = items[1]
        else:
            self.cdr = Pair(items[1:])

    def __str__(self):
        return self.str_form
        #res = '('
        #next = self.cdr
        #while next:
        #    if next.cdr == None:
        #        res += ' . ' + next.car
        #    elif isinstance(next.cdr, Nil):
        #        res += ' ' + next.car +
        #
        #return '(' + str(self.car) + " " + str(self.cdr) + ')'


class Vector(AbstractSexpr):
    def __init__(self, items):
        self.items = items

    def __str__(self):
        return '#(' + ' '.join(map(str, self.items)) + ')'

