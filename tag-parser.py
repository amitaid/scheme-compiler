from sexprs import *


class AbstractSchemeExpr:
    def __str__(self):
        pass

    @staticmethod
    def parse(input):
        result, remaining = AbstractSexpr.readFromString(input)


class Constant(AbstractSchemeExpr):
    pass


class Variable(AbstractSchemeExpr):
    pass


class IfThenElse(AbstractSchemeExpr):
    pass


class AbstractLambda(AbstractSchemeExpr):
    pass


class LambdaSimple(AbstractLambda):
    pass


class LambdaOpt(AbstractLambda):
    pass


class LambdaVar(AbstractLambda):
    pass


class Applic(AbstractSchemeExpr):
    pass


class Or(AbstractSchemeExpr):
    pass


class Def(AbstractSchemeExpr):
    pass