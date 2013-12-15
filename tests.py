import sexprs

# Zelig, this is the message
# Amitai, this is a message
import tag_parser


def parse(input):
    print(input + ' => ' + str(sexprs.AbstractSexpr.readFromString(input)[0]))


def main():

    #parse('(if 5 > 0 then 1 else 2)')
    #print(sexprs.Pair.get_car(x))
    #print(sexprs.Pair.get_cdr(x).get_car())
    #parse("'a")

    #x,y = sexprs.AbstractSexpr.readFromString('3')
    #print(tag_parser.AbstractSchemeExpr.parse('(lambda (x . y) (+ 1 1))'))
    #print(tag_parser.AbstractSchemeExpr.parse('(if 1 3 4)'))
    #print(tag_parser.AbstractSchemeExpr.parse('#(1 a z)'))
    print(tag_parser.AbstractSchemeExpr.parse("`(,x)")[0])
    #print(str(reader.list_to_pair([sexprs.Symbol('A'), sexprs.Symbol('B'),sexprs.Symbol('B'),sexprs.Symbol('B'), sexprs.Nil()])))
    #print(tag_parser.AbstractSchemeExpr.parse("(if #f 1 2)")[0])
    #parse(',@3')


if __name__ == '__main__':
    main()

