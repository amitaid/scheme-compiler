import sexprs
import tag_parser

# Zelig, this is the message
# Amitai, this is a message


def parse(input):
    print(input + ' => ' + str(sexprs.AbstractSexpr.readFromString(input)[0]))


def main():
    print(tag_parser.AbstractSchemeExpr.parse(
        "(LAMBDA X"
        "    (LAMBDA (Y X)"
        "        (LIST"
        "        (IF Y X (IF Z T 2))"
        "        (OR (LAMBDA (X)"
        "                (X Y))"
        "        X Y)"
        "        22"
        "        (D X (+ X Y))"
        "        (LAMBDA C"
        "            (LAMBDA (A B . C)"
        "                (LAMBDA (E F G)"
        "                    (LAMBDA (H I J)"
        "                        (IF (OR A B C) (D E F G) (D H (+ I J))))))))))")[0].semantic_analysis())

    print(tag_parser.AbstractSchemeExpr.parse("(lambda (x y . z) (x y z))")[0].semantic_analysis())
    # parse("(a b c)")
    #print(AbstractSchemeExpr.parse("(a b . c)")[0])
    #print(AbstractSchemeExpr.parse('(lambda (x) (if 1 (lambda (x) (+ x 1)) (lambda () x)))')[0].debruijn().annotateTC())
    # for test in testlist[-1:]:
    #     print(sexprs.AbstractSexpr.readFromString(test)[0])
    # print(sexprs.AbstractSexpr.readFromString('(x y z . 5/5)')[0].cdr.cdr)
    # x, y = AbstractSchemeExpr.parse("(+ x (lambda (x) (if "
        #                                 "    1 "
        #                                 "(lambda (x) ( + 1 x))"
        #                                 "(lambda () (+ x x))"
        #                                 ")))")
        # print(x)
        # print(x.debruijn().annotateTC())
        #print(x.annotateTC())
        #parse(',@3')

if __name__ == '__main__':
    main()

