from reader import *


class AbstractSexpr:
    def get_value(self):
        pass

    @staticmethod
    def readFromString(sexpr_str):
        return pSexpr.match(sexpr_str)


class Void(AbstractSexpr):
    def __str__(self):
        return 'Void()'

    def __eq__(self, other):
        return isinstance(other, Void)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('%Void')


class Nil(AbstractSexpr):
    def __str__(self):
        return '()'

    def __eq__(self, other):
        return isinstance(other, Nil)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('%Nil')

    def get_value(self):
        return None


class Boolean(AbstractSexpr):
    def __init__(self, value):
        self.value = value != '#f' and value != '#F'

    def __str__(self):
        if self.value:
            return '#t'
        else:
            return '#f'

    def __eq__(self, other):
        return isinstance(other, Boolean) and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('%Boolean')

    def get_value(self):
        return self.value


class Char(AbstractSexpr):
    def __init__(self, ch):
        self.value = ch

    def __str__(self):
        return '#\\' + str(self.value)

    def __eq__(self, other):
        return isinstance(other, Char) and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('%Char' + str(self.value))

    def get_value(self):
        return self.value


class AbstractNumber(AbstractSexpr):
    def __eq__(self, other):
        return isinstance(other, AbstractNumber) and self.eval() == other.eval()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('%Number' + str(self.eval()))

    def eval(self):
        pass


class Integer(AbstractNumber):
    def __init__(self, value):
        self.value = int(value)

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

    def __eq__(self, other):
        return isinstance(other, String) and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('%String' + self.value)

    def get_value(self):
        return self.value


class Symbol(AbstractSexpr):
    def __init__(self, symbol_str):
        self.value = symbol_str
        self.length = len(symbol_str)

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('%Symbol' + self.value)

    def get_value(self):
        return self.value


class Pair(AbstractSexpr):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        return '(' + self.inner_str() + ')'

    def __eq__(self, other):
        return isinstance(other, Pair) and \
               self.car == other.car and \
               self.cdr == other.cdr

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(hash(self.car) + hash(self.cdr))

    def inner_str(self):
        res = str(self.car)
        if isinstance(self.cdr, Nil):
            pass
        elif isinstance(self.cdr, Pair):
            res += ' ' + self.cdr.inner_str()
        else:
            res += ' . ' + str(self.cdr)
        return res

    def get_value(self):
        return (self.car, self.cdr)


class Vector(AbstractSexpr):
    def __init__(self, items):
        self.value = items

    def __str__(self):
        return '#(' + ' '.join(map(str, self.value)) + ')'

    def __eq__(self, other):
        return isinstance(other, Vector) and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(sum(hash(x) * i for (i, x) in enumerate(self.value)))

    def get_value(self):
        return self.value