from pc import *
import sexprs

ps = ParserStack()

new_line = pcChar('\n')

pSexpr_d = delayed(lambda: pSexpr)

line_comment = ps. \
    parser(pcChar(';')). \
    const(lambda m: m > ' '). \
    star(). \
    parser(new_line). \
    catens(4). \
    done()

sexpr_comment = ps. \
    parser(pcWord('#;')). \
    parser(pSexpr_d). \
    caten(). \
    done()

ignorable = ps. \
    parser(line_comment). \
    parser(sexpr_comment). \
    parser(pcWhite1). \
    disjs(3). \
    star(). \
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
    pack(lambda m: sexprs.Integer(m[0] + ''.join(m[2]))). \
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
    pack(lambda m: sexprs.Fraction(m[0], m[2])). \
    done()

boolean = ps. \
    parser(true). \
    parser(false). \
    disj(). \
    pack(lambda m: sexprs.Boolean(m[1].lower())). \
    done()

symbol = ps. \
    parser(symbol_chars). \
    plus(). \
    pack(lambda m: sexprs.Symbol(''.join(m))). \
    done()

meta_char_values = {'n': 10,
                    'r': 13,
                    't': 9,
                    'f': 12,
                    '\\': 93,
                    '"': 34,
                    'l': 0x03bb}

string_meta_char = ps. \
    parser(pcChar('\\')). \
    parser(pcOneOf('nrtf\\"l')). \
    caten(). \
    pack(lambda m: chr(meta_char_values[m[1]])). \
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
    pack(lambda m: sexprs.String(m[1])). \
    done()

named_chars = {'newline': 10,
               'return': 13,
               'tab': 9,
               'page': 12,
               'lambda': 0x03bb}

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
    pack(lambda m: ''.join(m)). \
    parser(hex_digits). \
    parser(hex_digits). \
    caten(). \
    maybe(). \
    pack(lambda m: ''.join(m[1]) if m[0] else ''). \
    catens(3). \
    pack(lambda m: chr(int(''.join(m[1:]), 16))). \
    done()

visible_char = const(lambda m: m > ' ')

char = ps. \
    parser(pcWord('#\\')). \
    parser(named_char). \
    parser(hex_char). \
    parser(visible_char). \
    disjs(3). \
    caten(). \
    pack(lambda m: sexprs.Char(m[1])). \
    done()

nil = ps. \
    parser(pcChar('(')). \
    parser(ignorable). \
    parser(pcChar(')')). \
    catens(3). \
    pack(lambda m: sexprs.Nil()). \
    done()

improper_list = ps. \
    parser(pcChar('(')). \
    parser(pSexpr_d). \
    plus(). \
    parser(pcChar('.')). \
    parser(pSexpr_d). \
    parser(pcChar(')')). \
    catens(5). \
    pack(lambda m: sexprs.Pair(m[1] + [m[3]])). \
    done()

proper_list = ps. \
    parser(pcChar('(')). \
    parser(pSexpr_d). \
    star(). \
    parser(pcChar(')')). \
    catens(3). \
    pack(lambda m: sexprs.Pair(m[1]) if m[1] else sexprs.Nil()). \
    done()

pair = ps. \
    parser(proper_list). \
    parser(improper_list). \
    disj(). \
    done()

vector = ps. \
    parser(pcWord('#(')). \
    parser(pSexpr_d). \
    star(). \
    parser(pcChar(')')). \
    catens(3). \
    pack(lambda m: sexprs.Vector(m[1])). \
    done()

quotes_dict = {'′': 'quote',
               '`': 'quasiquote',
               ',@': 'unquote-splicing',
               ',': "unquote"}

quote = ps. \
    parser(pcWord(',@')). \
    pack(lambda m: ''.join(m)). \
    parser(pcChar('′')). \
    parser(pcChar(',')). \
    parser(pcChar('`')). \
    disjs(4). \
    parser(pSexpr_d). \
    caten(). \
    pack(lambda m: sexprs.Pair([sexprs.Symbol(quotes_dict[m[0]]), sexprs.Pair([m[1]])])). \
    done()

pSexpr = ps. \
    parser(ignorable). \
    parser(fraction). \
    parser(integer). \
    parser(symbol). \
    parser(string). \
    parser(boolean). \
    parser(char). \
    parser(pair). \
    parser(vector). \
    parser(nil). \
    parser(quote). \
    disjs(10). \
    parser(ignorable). \
    catens(3). \
    pack(lambda m: m[1]). \
    done()


