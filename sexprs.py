from pc import *

ps = ParserStack()

new_line = pcChar('\n')

line_comment_d = delayed(lambda: line_comment)
pSexpr_d = delayed(lambda: pSexpr)

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
    parser(unsigned_int). \
    caten(). \
    pack(lambda m: m[1].negate() if m[0] == '-' else m[1]). \
    done()

integer = ps. \
    parser(signed_int). \
    parser(unsigned_int). \
    disj(). \
    done()

fraction = ps. \
    parser(integer). \
    parser(pcChar('/')). \
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

string_meta_char = ps. \
    parser(pcChar('\\')). \
    parser(pcOneOf('nrtf\\"l')). \
    caten(). \
    pack(lambda m: chr(0x03bb) if m[1] == 'l' else m[1]). \
    done()

string = ps. \
    parser(pcChar('"')). \
    parser(string_meta_char). \
    const(). \
    parser(pcChar('"')). \
    butNot(). \
    disj(). \
    star(). \
    parser(pcChar('"')). \
    catens(3). \
    pack(lambda m: String(m[1])). \
    done()

named_chars = {'newline': 10,
               'return': 13,
               'tab': 9,
               'page': 12,
               'lambda': 0x3bb}

named_char = ps. \
    parser(pcWord('newline')). \
    parser(pcWord('return')). \
    parser(pcWord('tab')). \
    parser(pcWord('page')). \
    parser(pcWord('lambda')). \
    disjs(5). \
    pack(lambda m: chr(named_chars[''.join(m)])). \
    done()

hex_char = ps. \
    parser(pcChar('x')). \
    parser(hex_digits). \
    parser(hex_digits). \
    caten(). \
    parser(hex_digits). \
    parser(hex_digits). \
    caten(). \
    maybe(). \
    catens(3). \
    pack(lambda m: chr(int(''.join((m[1] + m[2][1]) if m[2][0] else m[1]), 16))). \
    done()

visible_char = const(lambda m: m > ' ')

char = ps. \
    parser(pcWord('#\\')). \
    parser(named_char). \
    parser(hex_char). \
    parser(visible_char). \
    disjs(3). \
    caten(). \
    pack(lambda m: Char(m[1])). \
    done()

# TODO: add comment support inside nil
nil = ps. \
    parser(pcChar('(')). \
    parser(pcWhiteStar). \
    parser(pcChar(')')). \
    catens(3). \
    pack(lambda m: Nil()). \
    done()

improper_list = ps. \
    parser(pcChar('(')). \
    parser(pSexpr_d). \
    plus(). \
    parser(pcChar('.')). \
    parser(pSexpr_d). \
    parser(pcChar(')')). \
    catens(5). \
    pack(lambda m: Pair(m[1] + [m[3]])). \
    done()

proper_list = ps. \
    parser(pcChar('(')). \
    parser(pSexpr_d). \
    star(). \
    parser(pcChar(')')). \
    catens(3). \
    pack(lambda m: Pair(m[1])). \
    done()

pair = ps. \
    parser(proper_list). \
    parser(improper_list). \
    disj(). \
    done()

vector = ps. \
    parser(pcWord('#(')). \
    parser(pcWhiteStar). \
    parser(pSexpr_d). \
    caten(). \
    pack(lambda m: m[1]). \
    star(). \
    parser(pcWhiteStar). \
    parser(pcChar(')')). \
    catens(5). \
    pack(lambda m: Vector(m[1])). \
    done()

quotes_dict = {'′': 'quote', '`': 'quasiquote', ',@': 'unquote-splicing', ',': "unquote"}

quote = ps. \
    parser(pcWord(',@')). \
    pack(lambda m: ''.join(m)). \
    parser(pcChar('′')). \
    parser(pcChar(',')). \
    parser(pcChar('`')). \
    disjs(4). \
    parser(pSexpr_d). \
    caten(). \
    pack(lambda m: Pair([Symbol(quotes_dict[m[0]]), Pair([m[1]])])). \
    done()

pSexpr = ps. \
    parser(pcWhiteStar). \
    parser(fraction). \
    parser(integer). \
    parser(symbol). \
    parser(string). \
    parser(char). \
    parser(pair). \
    parser(vector). \
    parser(nil). \
    parser(quote). \
    disjs(9). \
    parser(pcWhiteStar). \
    catens(3). \
    pack(lambda m: m[1]). \
    done()


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
            raise NoMatch

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
            raise NoMatch('Divide by zero')

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
        self.car = items[0]
        if len(items[1:]) == 0:
            self.cdr = Nil()
        elif len(items[1:]) == 1:
            self.cdr = items[1]
        else:
            self.cdr = Pair(items[1:])

    def __str__(self):
        return '(' + str(self.car) + " . " + str(self.cdr) + ')'


class Vector(AbstractSexpr):
    def __init__(self, items):
        self.items = items

    def __str__(self):
        return '#(' + ' '.join(map(str, self.items)) + ')'


def main():
    print(AbstractSexpr.readFromString('′(#\\lambda x y z)')[0])
    print(AbstractSexpr.readFromString('`#\\lambda')[0])
    print(AbstractSexpr.readFromString(',@#\\lambda')[0])
    print(AbstractSexpr.readFromString(',#\\lambda')[0])

    print(integer.match('+0h34')[0])

    print(fraction.match('0X54/0Hf50')[0])
    print(fraction.match('-00000000000000034/0x0000000000000000000000000043')[0])

    print(symbol.match('abc!!?bcd')[0])

    print(boolean.match('#t')[0])

    print(string.match('"123\lcdd""')[0])

    print(char.match('#\\lambda')[0])
    print(char.match('#\\x30')[0])
    print(char.match('#\\☺')[0])

    print(nil.match('(   )')[0])


if __name__ == '__main__':
    main()
