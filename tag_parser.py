from tkinter import constants
from sexprs import *
import reader

key_words = ['define', 'lambda','λ','IF','else','then','and','or','cond']

class AbstractSchemeExpr:

    @staticmethod
    def parse(input):
        result, remaining = AbstractSexpr.readFromString(input)
        scheme_expr = AbstractSchemeExpr.process(result)
        return scheme_expr

    @staticmethod  # where the actual parsing occur
    def process(result):
        if Constant.is_const(result):
            ast = Constant(result)
        elif Variable.is_variable(result):
            ast =Variable(result)
        elif IfThenElse.is_if(result):
            ast = IfThenElse(result)
        else:
            print('format not supported: ' + str(result))
            ast = Constant(Void())

        return ast


### Constant ###

class Constant(AbstractSchemeExpr):

    def __init__(self,sexpr):
        self.expr = sexpr

    def __str__(self):
        if isinstance(self.expr,Pair):
            quate,rest = self.expr.get_value()
            arg,nil = rest.get_value()
            return 'Constant('+str(quate)+' '+str(rest)+')'
        else:
            return 'Constant('+str(self.expr)+')'

    def is_quated(sexpr): # TODO implement later
        if isinstance(sexpr,Pair) and isinstance(Pair.get_car(sexpr),Symbol) and \
            Pair.get_car(sexpr).get_value() in reader.quotes_dict.values():
            return True
        return False

    def is_const(sexpr):
        if isinstance(sexpr,Boolean) or \
            isinstance(sexpr,Char) or \
            isinstance(sexpr,AbstractNumber) or \
            isinstance(sexpr,String) or \
            isinstance(sexpr,Void): # maybe the last condition is useless
            return True;
        elif Constant.is_quated(sexpr):
            return True
        else: #TODO add unquated support
            return False

### Variable ###

class Variable(AbstractSchemeExpr):
    def __init__(self,sexpr):
        self.value = AbstractSexpr.get_value(sexpr)

    def __str__(self):
        return 'Variable('+str(self.value)+')'

    # predicate for recognizing if then else expr
    def is_variable(sexpr):
        if isinstance(sexpr,Symbol) and not Symbol.get_value(sexpr) in key_words:
            return True
        return False

### Core Forms ###

class IfThenElse(AbstractSchemeExpr):
    def __init__(self,expr):
        irt = expr.get_cdr() # irt = if rest of tokens
        pred_expr,irt = irt.get_value()
        then_expr,irt = irt.get_value()
        if isinstance(irt,Pair):
            else_expr = irt.get_car()
            self.else_expr = AbstractSchemeExpr.process(else_expr)
        else:
            self.else_expr = Constant(Void())
        self.predicate = AbstractSchemeExpr.process(pred_expr)
        self.then_expr = AbstractSchemeExpr.process(then_expr)

    def __str__(self):
        return 'IfThenElse('+str(self.predicate)+ \
        ','+str(self.then_expr)+','+str(self.else_expr)+')'

    # predicate for both IfThen & IfThenElse
    def is_if(expr):
        # first check if it is a pair at all
        if isinstance(expr,Pair):
            if_token,rest_expr = expr.get_value()
            # second check if first token is if and rest is pair
            if isinstance(if_token,Symbol) and \
                str(if_token.get_value()) == 'IF' and \
                isinstance(rest_expr,Pair):

                rest_expr2 = rest_expr.get_cdr()
                #third check for checking there are enough args in the pairs
                if isinstance(rest_expr2,Pair):

                    rest_expr3 = rest_expr2.get_cdr()
                    # fourth check if the else arg exists
                    # if so it checks if its tail is Nil (IfThenElse)
                    # otherwise checks if checks if else is Nil (IfThen)
                    if isinstance(rest_expr3,Pair) and  \
                        isinstance(rest_expr3.get_cdr(),Nil) or \
                        isinstance(rest_expr3,Nil):
                        return True
        return False

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

### Lambda Forms ###

class AbstractLambda(AbstractSchemeExpr):
    pass

class LambdaSimple(AbstractLambda):
    pass

class LambdaOpt(AbstractLambda):
    pass

class LambdaVar(AbstractLambda):
    pass

class syntacticSugar(AbstractSchemeExpr):
    pass



    def is_quasiquated(expr):
        pass

    def is_let(expr):
        pass

    def is_letStar(expr):
        pass

    def is_letrec(expr):
        pass

    def is_cond(expr):
        pass

    def is_and(expr):
        pass

    def ic_2_nextedifs(expr): # cond -> if transformation
        pass

