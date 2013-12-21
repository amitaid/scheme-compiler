import sexprs

# Zelig, this is the message
# Amitai, this is a message
from tag_parser import *


def parse(input):
    print(input + ' => ' + str(sexprs.AbstractSexpr.readFromString(input)[0]))


def main():
    testlist = ['(LAMBDA (X) (LAMBDA (Y Z) ((LAMBDA (X V) (F Z X)) (+ V Z X))))',
                '(LAMBDA X (LAMBDA (Y X) (LIST (IF Y X (IF Z T 2)) (OR (LAMBDA (X) (X Y)) X Y) 22 (D X (+ X Y)) (LAMBDA C (LAMBDA (A B . C) (LAMBDA (E F G) (LAMBDA (H I J) (IF (OR A B C) (D E F G) (D H (+ I J))))))))))',
                '(DEFINE FOO (LAMBDA (X) (IF (= X 1) (* 5 (HOO X)) (IF (= X 2) (HOO X) (FOO X)))))',
                '(LAMBDA (A B C) (LAMBDA (E F G) (LIST (OR A B (OR C D)) (* G O G O) (LAMBDA Y (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (X Y)))))))))))) (IF (= 9 2) (OR 1 2 3) A) (IF A B (IF A B (IF A B C))) "bye bye")))']

    for test in testlist:
        print(AbstractSchemeExpr.parse(test)[0].debruijn().annotateTC())

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

