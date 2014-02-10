from fractions import gcd

from pc import *
import sexprs


ps = ParserStack()

pSexpr_d = delayed(lambda: sexpr)

######### Comment ###########

line_comment = ps. \
    parser(pcChar(';')). \
    const(). \
    parser(pcChar('\n')). \
    butNot(). \
    star(). \
    parser(pcChar('\n')). \
    catens(3). \
    done()

sexpr_comment = ps. \
    parser(pcWord('#;')). \
    parser(pSexpr_d). \
    caten(). \
    done()

ignorable = ps. \
    parser(pcWhite1). \
    parser(line_comment). \
    parser(sexpr_comment). \
    disjs(3). \
    done()

ignore_star = ps. \
    parser(ignorable). \
    star(). \
    done()

ignore_plus = ps. \
    parser(ignorable). \
    plus(). \
    done()

######### Number ##########

zero = pcChar('0')
dec_digit = pcRange('0', '9')
hex_digit = pcOneOf('0123456789abcdefABCDEF')

hex_prefix = ps. \
    parser(pcWordCI('0x')). \
    parser(pcWordCI('0h')). \
    disj(). \
    done()

unsigned_int = ps. \
    parser(hex_prefix). \
    parser(zero). \
    star(). \
    parser(hex_digit). \
    plus(). \
    catens(3). \
    pack(lambda m: '0x' + ''.join(m[2])). \
    parser(zero). \
    star(). \
    parser(dec_digit). \
    plus(). \
    caten(). \
    pack(lambda m: ''.join(m[1])). \
    disj(). \
    done()

unsigned_int_nz = ps. \
    parser(hex_prefix). \
    parser(zero). \
    star(). \
    parser(hex_digit). \
    parser(zero). \
    butNot(). \
    parser(hex_digit). \
    star(). \
    catens(4). \
    pack(lambda m: '0x' + ''.join(m[1] + [m[2]] + m[3])). \
    parser(zero). \
    star(). \
    parser(dec_digit). \
    parser(zero). \
    butNot(). \
    parser(dec_digit). \
    star(). \
    catens(3). \
    pack(lambda m: m[1] + ''.join(m[2])). \
    disj(). \
    done()

signed_int = ps. \
    parser(pcChar('+')). \
    parser(pcChar('-')). \
    disj(). \
    parser(unsigned_int). \
    caten(). \
    pack(lambda m: m[0] + m[1]). \
    done()

integer = ps. \
    parser(signed_int). \
    parser(unsigned_int). \
    disj(). \
    pack(lambda m: sexprs.Integer(int(m, 0))). \
    done()

fraction = ps. \
    parser(signed_int). \
    parser(unsigned_int). \
    disj(). \
    parser(pcChar('/')). \
    parser(unsigned_int_nz). \
    catens(3). \
    pack(lambda m: (int(m[0], 0), int(m[2], 0))). \
    pack(lambda m: (m[0], m[1], gcd(m[0], m[1]))). \
    pack(lambda m: (int(m[0] / m[2]), int(m[1] / m[2]))). \
    pack(
    lambda m: sexprs.Fraction(sexprs.Integer(m[0]), sexprs.Integer(m[1])) if not m[1] == 1 else sexprs.Integer(m[0])). \
    done()

######### Symbol ##########

symbol_chars = ps. \
    parser(pcRangeCI('a', 'z')). \
    parser(dec_digit). \
    parser(pcOneOf('!$^*-_=+<>/?')). \
    disjs(3). \
    done()

symbol = ps. \
    parser(symbol_chars). \
    plus(). \
    pack(lambda m: sexprs.Symbol(''.join(m).upper())). \
    done()

########## Boolean ###########

true = pcWordCI('#T')
false = pcWordCI('#F')

boolean = ps. \
    parser(true). \
    parser(false). \
    disj(). \
    pack(lambda m: sexprs.Boolean(''.join(m).lower())). \
    done()

######### String #########

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
    pack(lambda m: sexprs.String(''.join(m[1]))). \
    done()

######### Char ##########

named_chars_dict = {
    'newline': 10,
    'return': 13,
    'tab': 9,
    'page': 12,
    'lambda': 0x03bb}

named_char = ps. \
    parser(pcWordCI('newline')). \
    parser(pcWordCI('return')). \
    parser(pcWordCI('tab')). \
    parser(pcWordCI('page')). \
    parser(pcWordCI('lambda')). \
    disjs(5). \
    pack(lambda m: ''.join(m).lower()). \
    done()

hex_char = ps. \
    parser(pcChar('x')). \
    parser(hex_digit). \
    parser(hex_digit). \
    caten(). \
    pack(lambda m: ''.join(m)). \
    parser(hex_digit). \
    parser(hex_digit). \
    caten(). \
    maybe(). \
    pack(lambda m: ''.join(m[1]) if m[0] else ''). \
    catens(3). \
    pack(lambda m: ''.join(m[1:])). \
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

######### Nil ##########

nil = ps. \
    parser(pcChar('(')). \
    parser(ignorable). \
    star(). \
    parser(pcChar(')')). \
    catens(3). \
    pack(lambda m: sexprs.Nil()). \
    done()

######## Pair ##########

def list_to_pair(l):
    if len(l) == 1:
        return l[0]
    else:
        return sexprs.Pair(l[0], list_to_pair(l[1:]))


pair = ps. \
    parser(pcChar('(')). \
    parser(ignore_star). \
    parser(pSexpr_d). \
    parser(ignore_plus). \
    parser(pSexpr_d). \
    caten(). \
    pack(lambda m: m[1]). \
    star(). \
    parser(ignore_plus). \
    parser(pcChar('.')). \
    parser(ignore_plus). \
    parser(pSexpr_d). \
    catens(4). \
    pack(lambda m: m[3]). \
    maybe(). \
    parser(ignore_star). \
    parser(pcChar(')')). \
    catens(7). \
    pack(lambda m: list_to_pair([m[2]] + m[3] + ([m[4][1]] if m[4][0] else [sexprs.Nil()]))). \
    done()

# Old, inefficient version
# pSexpr_wrapped = ps. \
#     parser(ignorable). \
#     star(). \
#     parser(pSexpr_d). \
#     parser(ignorable). \
#     star(). \
#     catens(3). \
#     pack(lambda m: m[1]). \
#     done()
#
# improper_list = ps. \
#     parser(pcChar('(')). \
#     parser(pSexpr_wrapped). \
#     plus(). \
#     parser(pcWord('.')). \
#     parser(pSexpr_wrapped). \
#     parser(pcChar(')')). \
#     catens(5). \
#     pack(lambda m: list_to_pair(m[1] + [m[3]])). \
#     done()
#
# proper_list = ps. \
#     parser(pcChar('(')). \
#     parser(pSexpr_wrapped). \
#     plus(). \
#     parser(pcChar(')')). \
#     catens(3). \
#     pack(lambda m: list_to_pair(m[1] + [sexprs.Nil()])). \
#     done()
#
# pair = ps. \
#     parser(proper_list). \
#     parser(improper_list). \
#     disj(). \
#     done()

######### Vector #########

vector = ps. \
    parser(pcWord('#(')). \
    parser(ignore_star). \
    parser(pSexpr_d). \
    caten(). \
    pack(lambda m: m[1]). \
    star(). \
    parser(ignore_star). \
    parser(pcChar(')')). \
    catens(4). \
    pack(lambda m: sexprs.Vector(m[1])). \
    done()

######### Quote ##########

quotes_dict = {'′': 'quote',
               "'": 'quote',
               '`': 'quasiquote',
               ',@': 'unquote-splicing',
               ',': 'unquote'}

quote = ps. \
    parser(pcWord(',@')). \
    pack(lambda m: ''.join(m)). \
    parser(pcChar('′')). \
    parser(pcChar("'")). \
    parser(pcChar(',')). \
    parser(pcChar('`')). \
    disjs(5). \
    parser(pSexpr_d). \
    caten(). \
    pack(lambda m: sexprs.Pair(sexprs.Symbol(quotes_dict[m[0]]), sexprs.Pair(m[1], sexprs.Nil()))). \
    done()

###### S-Expression ########

sexpr = ps. \
    parser(pair). \
    parser(fraction). \
    parser(integer). \
    parser(symbol). \
    parser(string). \
    parser(boolean). \
    parser(char). \
    parser(vector). \
    parser(nil). \
    parser(quote). \
    disjs(10). \
    done()

pSexpr = ps. \
    parser(ignore_star). \
    parser(sexpr). \
    parser(ignore_star). \
    catens(3). \
    pack(lambda m: m[1]). \
    done()