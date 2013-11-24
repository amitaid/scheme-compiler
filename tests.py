import sexprs
import reader

# Zelig, this is the message
# Amitai, this is a message
import tag_parser


def parse(input):
    print(input + ' => ' + str(sexprs.AbstractSexpr.readFromString(input)[0]))


def main():
    #print(sexprs.AbstractSexpr.readFromString(
    #    r'(-0H432 +0123/0x52 ab53$$ "bla bla \n \l bla" #\pAge #\tAb #\xFDFA #\M () #(1 2 3 #(1 2 3)) 72 . 5)')[0])

    #print(reader.ignorable.match('#;(a b c)'))

    #parse(r';     \n(a)')


    #print(AbstractSexpr.readFromString('′(#\\x03bb x y z)')[0])
    #print(AbstractSexpr.readFromString('`#\\lambda')[0])
    #print(AbstractSexpr.readFromString(',@#\\lambda')[0])
    #print(AbstractSexpr.readFromString(',#\\lambda')[0])

    #print(AbstractSexpr.readFromString('#\pAge')[0])

    #print(proper_list.match('(a v)')[0])
    #
    #print(fraction.match('5/0xa')[0])
    #
    #print(AbstractSexpr.readFromString('#t')[0])
    #
    #print(AbstractSexpr.readFromString('"123\lcdd""')[0])
    #
    #print(AbstractSexpr.readFromString('#\\lambda')[0])
    #print(AbstractSexpr.readFromString('#\\x30')[0])
    #print(AbstractSexpr.readFromString('#\\☺')[0])

    #parse('(if 5 > 0 then 1 else 2)')
    #print(sexprs.Pair.get_car(x))
    #print(sexprs.Pair.get_cdr(x).get_car())
    #parse("'a")

    #x = tag_parser.AbstractSchemeExpr.parse('(if #t #\\y)')
    #x = tag_parser.AbstractSchemeExpr.parse('"abc"')
    #print(x)

    #print(sexprs.AbstractSexpr.readFromString('′a'))
    #x = tag_parser.AbstractSchemeExpr.parse('a')
    x = tag_parser.AbstractSchemeExpr.parse('(define x 3)')
    #x,y = sexprs.AbstractSexpr.readFromString('(define x 3)')
    print(x)
    #x = tag_parser.Def(x)
    print(str(x))
    #print(b)


if __name__ == '__main__':
    main()

