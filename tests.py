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

#    parse('(if 5 > 0 then 1 else 2)')
    x,y = sexprs.AbstractSexpr.readFromString('(if #t 1)')
    print(x)
    print(tag_parser.IfThenElse.is_if_then_else(x))
    print(tag_parser.syntacticSugar.is_if_then(x))
  #  print(sexprs.Pair.get_car(x))
  #  print(sexprs.Pair.get_cdr(x).get_car())
  #  x2,y2 = tag_parser.AbstractSchemeExpr.get_token('IF',x)
  #  print(x2)
  #  print(y2)
  #  x3,y3 = tag_parser.AbstractSchemeExpr.get_token('THEN',x)
  #  print(x3)
  #  print(y3)
  #  x4,y4 = tag_parser.AbstractSchemeExpr.get_token('ELSE',x)
  #  print(x4)
  #  print(y4)
  #  x5,y5 = tag_parser.AbstractSchemeExpr.get_token('1',x)
  #  print(x5)
  #  print(y5)
  #  x6,y6 = tag_parser.AbstractSchemeExpr.get_token('2',x)
  #  print(x6)
  #  print(y6)
if __name__ == '__main__':
    main()

