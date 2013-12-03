from pc import *
import sexprs

ps = ParserStack()

pSexpr_d = delayed(lambda: pSexpr)

######### Comment ###########

# TODO Fix line comments
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
    parser(line_comment). \
    parser(sexpr_comment). \
    parser(pcWhitePlus). \
    disjs(3). \
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
    pack(lambda m: sexprs.Integer(m)). \
    done()

fraction = ps. \
    parser(integer). \
    parser(pcChar('/')). \
    parser(unsigned_int_nz). \
    pack(lambda m: sexprs.Integer(m)). \
    catens(3). \
    pack(lambda m: sexprs.Fraction(m[0], m[2])). \
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
    pack(lambda m: sexprs.Boolean(m[1].lower())). \
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
    pack(lambda m: chr(named_chars_dict[''.join(m).lower()])). \
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

pSexpr_wrapped = ps. \
    parser(ignorable). \
    star(). \
    parser(pSexpr_d). \
    parser(ignorable). \
    star(). \
    catens(3). \
    pack(lambda m: m[1]). \
    done()

improper_list = ps. \
    parser(pcChar('(')). \
    parser(pSexpr_wrapped). \
    plus(). \
    parser(pcWord('. ')). \
    parser(pSexpr_wrapped). \
    parser(pcChar(')')). \
    catens(5). \
    pack(lambda m: sexprs.Pair(m[1][0], m[1][1:] + [m[3]])). \
    done()

proper_list = ps. \
    parser(pcChar('(')). \
    parser(pSexpr_wrapped). \
    plus(). \
    parser(pcChar(')')). \
    catens(3). \
    pack(lambda m: sexprs.Pair(m[1][0], m[1][1:] + [sexprs.Nil()])). \
    done()

pair = ps. \
    parser(improper_list). \
    parser(proper_list). \
    disj(). \
    done()

######### Vector #########

vector = ps. \
    parser(pcWord('#(')). \
    parser(pSexpr_wrapped). \
    star(). \
    parser(pcChar(')')). \
    catens(3). \
    pack(lambda m: sexprs.Vector(m[1])). \
    done()

######### Quote ##########

quotes_dict = {'′': 'quote',
               '`': 'quasiquote',
               ',@': 'unquote-splicing',
               ',': 'unquote'}

quote = ps. \
    parser(pcWord(',@')). \
    pack(lambda m: ''.join(m)). \
    parser(pcChar('′')). \
    parser(pcChar(',')). \
    parser(pcChar('`')). \
    disjs(4). \
    parser(pSexpr_d). \
    caten(). \
    pack(lambda m: sexprs.Pair(sexprs.Symbol(quotes_dict[m[0]]), [sexprs.Pair(m[1], [sexprs.Nil()])])). \
    done()

###### S-Expression ########

pSexpr = ps. \
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
    done()