from sexprs import *


key_words = ['define', 'lambda','λ','if','else','then','and','or','cond']

class AbstractSchemeExpr:
    @staticmethod
    def parse(input):
        result, remaining = AbstractSexpr.readFromString(input)
        # dealing with core forms


### Constant ###

class Constant(AbstractSchemeExpr):
    pass

    def is_quated(sexpr): # TODO implement later
        return False

    def is_const(sexpr):
        if isinstance(sexpr,Boolean) or  isinstance(sexpr,Char) \
            or  isinstance(sexpr,AbstractNumber) or  isinstance(sexpr,String):
            return True;
        elif Constant.is_quated(sexpr):
            return True
        else: #TODO add unquated support
            return False


### Variable ###

class Variable(AbstractSchemeExpr):
    pass

    def is_variable(sexpr):
    # predicate for recognizing if then else expr
        if isinstance(sexpr,Symbol) and not sexpr in key_words:
            return True;
        elif sexpr in key_words:
            print("Error: is a key word" +  str(sexpr)) #TODO maybe throw exception
        return False;


### Lambda Forms ###

class AbstractLambda(AbstractSchemeExpr):
    pass

class LambdaSimple(AbstractLambda):
    pass

class LambdaOpt(AbstractLambda):
    pass


class LambdaVar(AbstractLambda):
    pass

### Core Forms ###

class IfThenElse(AbstractSchemeExpr):
    pass

    def is_if_then_else(expr):
        # predicate for recognizing if then else expr
        pass

    def is_if_then(expr):
        # predicate for recognizing ifthen expr
        pass

    def it2ite(expr): # if then -> if then else transformation
        pass          # syntactic sugar

class Applic(AbstractSchemeExpr):
    pass

    def is_applic(expr):
        # a predicate for recognizing applicative expressions
        pass

class Or(AbstractSchemeExpr):
    pass

    def is_or(expr):
        # a predicate for recognizing or expressions
        pass


class Def(AbstractSchemeExpr):
    pass

    def is_def(expr):
        # a predicate for recognizing definition expressions
        pass