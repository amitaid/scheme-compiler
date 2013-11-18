from pc import *

ps = ParserStack()

new_line = pcChar('\n')

d_line_comment = delayed(lambda: line_comment)

line_comment = ps. \
    parser(pcWhiteStar). \
    parser(pcChar(';')). \
    const(lambda m: m > ' '). \
    star(). \
    parser(new_line). \
    catens(4). \
    done()

zero = pcChar('0')
hex_digits = pcOneOfCI('0123456789abcdef')
true = pcWordCI('#T')
false = pcWordCI('#F')
symbol_chars = ps. \
    parser(pcRangeCI('a', 'z')). \
    parser(pcRange('0', '9')). \
    parser(pcOneOf('!$^*-_=+<>/?')). \
    disjs(3). \
    done()

unsigned_int = ps. \
    parser(pcWordCI('0x')). \
    parser(pcWordCI('0h')). \
    disj(). \
    maybe(). \
    pack(lambda m: '0x' if m[0] else ''). \
    parser(zero). \
    star(). \
    parser(hex_digits). \
    plus(). \
    catens(3). \
    pack(lambda m: Integer(m[0] + ''.join(m[2]))). \
    done()

signed_int = ps. \
    parser(pcChar('+')). \
    parser(pcChar('-')). \
    disj(). \
    maybe(). \
    pack(lambda m: m[1] if m[0] and m[1] == '-' else ''). \
    parser(unsigned_int). \
    caten(). \
    pack(lambda m: Integer(m[0] + str(m[1]))). \
    done()

fraction = ps. \
    parser(signed_int). \
    const(lambda m: m == '/'). \
    parser(unsigned_int). \
    catens(3). \
    pack(lambda m: Fraction(m[0], m[2])). \
    done()

boolean = ps. \
    parser(true). \
    parser(false). \
    disj(). \
    pack(lambda m: Boolean(m[1].lower())). \
    done()

symbol = ps. \
    parser(symbol_chars). \
    plus(). \
    pack(lambda m: Symbol(''.join(m))). \
    done()

pSexpr = None


class AbstractSexpr:
    pass


class Void(AbstractSexpr):
    pass


class Nil(AbstractSexpr):
    pass


class Boolean(AbstractSexpr):
    def __init__(self, value):
        self.value = value == 't'

    def __str__(self):
        return str(self.value)


class Char(AbstractSexpr):
    pass


class AbstractNumber(AbstractSexpr):
    def evaluate(self):
        pass


class Integer(AbstractNumber):
    def __init__(self, value):
        try:
            self.value = int(value, 0)
        except ValueError:
            raise NoMatch

    def __str__(self):
        return str(self.value)

    def evaluate(self):
        return self.value


class Fraction(AbstractNumber):
    def __init__(self, numer, denum):
        self.numer, self.denum = numer.evaluate(), denum.evaluate()
        if self.denum == 0:
            raise NoMatch('Divide by zero')

    def __str__(self):
        return str(self.numer) + '/' + str(self.denum)

    def evaluate(self):
        return self.numer.evaluate() / self.denum.evaluate()


class String(AbstractSexpr):
    pass


class Symbol(AbstractSexpr):
    def __init__(self, symbol_str):
        self.symbol = symbol_str
        self.length = len(symbol_str)

    def __str__(self):
        return self.symbol


class Pair(AbstractSexpr):
    pass


class Vector(AbstractSexpr):
    pass


def main():
    print(signed_int.match('34')[0])
    print(signed_int.match('+0h34')[0])
    print(fraction.match('0X54/0Hf50')[0])
    print(fraction.match('-00000000000000034/0x0000000000000000000000000043')[0])

    print(symbol.match('abc!!?bcd')[0].length)

    print(boolean.match('#t')[0])


if __name__ == '__main__':
    main()
