import tag_parser


class ExprStats:
    f = 0
    p = 0
    b = 0
    tp = 0

    @staticmethod
    def count(e):
        if not (isinstance(e, object)) or isinstance(e, (str, bool, int, float)):
            return
        elif type(e) is list:
            for x in e:
                ExprStats.count(x)
        elif isinstance(e, tag_parser.VarFree):
            ExprStats.f += 1
        elif isinstance(e, tag_parser.VarParam):
            ExprStats.p += 1
        elif isinstance(e, tag_parser.VarBound):
            ExprStats.b += 1
        elif isinstance(e, tag_parser.ApplicTP):
            ExprStats.tp += 1
            members = list(e.__dict__.keys())
            for m in members:
                ExprStats.count(getattr(e, m))
        else:
            members = list(e.__dict__.keys())
            for m in members:
                ExprStats.count(getattr(e, m))
        return

    @staticmethod
    def reset():
        ExprStats.f = 0
        ExprStats.p = 0
        ExprStats.b = 0
        ExprStats.tp = 0


parse = tag_parser.AbstractSchemeExpr.parse
tests = list()

# [test, fvar_num, pvar_num, bvar_num, tp_num]
tests.append(["(LAMBDA (X) (LAMBDA (Y Z) ((LAMBDA (X V) (F Z X)) (+ V Z X))))", 3, 2, 2, 2])
tests.append([
    "(LAMBDA X (LAMBDA (Y X) (LIST (IF Y X (IF Z T 2)) (OR (LAMBDA (X) (X Y)) X Y) 22 (D X (+ X Y)) (LAMBDA C (LAMBDA (A B . C) (LAMBDA (E F G) (LAMBDA (H I J) (IF (OR A B C) (D E F G) (D H (+ I J))))))))))",
    8, 11, 7, 4])
tests.append(["(DEFINE FOO (LAMBDA (X) (IF (= X 1) (* 5 (HOO X)) (IF (= X 2) (HOO X) (FOO X)))))", 7, 5, 0, 3])
tests.append([
    "(LAMBDA (A B C) (LAMBDA (E F G) (LIST (OR A B (OR C D)) (* G O G O) (LAMBDA Y (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (LAMBDA X (X Y)))))))))))) (IF (= 9 2) (OR 1 2 3) A) (IF A B (IF A B (IF A B C))) \"bye bye\")))",
    6, 3, 12, 2])

index = 1

for i in tests:
    x, y = parse(i[0])
    if y != '':
        print("Test {0} failed. Entire string was not parsed. Left to parse: {1}".format(str(index), str(y)))
    x = x.semantic_analysis()
    ExprStats.count(x)
    given = [ExprStats.f, ExprStats.p, ExprStats.b, ExprStats.tp]
    expected = i[1:]
    if given == expected:
        print("Test {0} passed.".format(str(index)))
    else:
        print("Test {0} failed!".format(str(index)))
        if given[0] != expected[0]:
            print("\t* Expected {1} FreeVars; found: {2}".format(str(index), expected[0], given[0]))
        if given[1] != expected[1]:
            print("\t* Expected {1} ParamVars; found: {2}".format(str(index), expected[1], given[1]))
        if given[2] != expected[2]:
            print("\t* Expected {1} BoundVars; found: {2}".format(str(index), expected[2], given[2]))
        if given[3] != expected[3]:
            print("\t* Expected {1} tails calls; found: {2}".format(str(index), expected[3], given[3]))
    ExprStats.reset()
    index += 1
