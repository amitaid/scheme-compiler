from tkinter import constants
from sexprs import *


key_words = ['define', 'lambda','λ','if','else','then','and','or','cond']

class AbstractSchemeExpr:

    @staticmethod
    def parse(input):
        result, remaining = AbstractSexpr.readFromString(input)
        Scheme_expr = AbstractSchemeExpr.process(result)



    @staticmethod  # where the actual parsing occur
    def process(result):
        if Constant.is_const(result):
            ast = Constant(result)
        elif Variable.is_variable(result)
        elif IfThenElse.is_if(result):
            ast = IfThenElse(result)
        else:
            print('format not supported: ' + result)
            ast = Constant(Void())

        return ast

    # this function gets a token of string and a pair, and extracts the token if available
    def get_token(token,pair):  # token is a string/char
        if isinstance(pair,Pair):
            if str(pair.get_car().get_value()) == token: #  isinstance(pair.get_car(),Symbol) and
                #print(pair)
                return (pair.get_car(),pair.get_cdr())
            else:
                #print(pair.cdr)
                pair2 = Pair.get_cdr(pair)
                return AbstractSchemeExpr.get_token(token,pair2)
        if not isinstance(pair,Nil) and str(pair.get_car().get_value()) == token:
            return (pair.get_car(),Nil)
        return None

### Constant ###

class Constant(AbstractSchemeExpr):

    def __init__(self,sexpr):
        self.expr = sexpr

    def is_quated(sexpr): # TODO implement later
        return False

    def is_const(sexpr):
        if isinstance(sexpr,Boolean) or \
            isinstance(sexpr,Char) or \
            isinstance(sexpr,AbstractNumber) or \
            isinstance(sexpr,String) or \
            isinstance(sexpr,Void):
            return True;
        elif Constant.is_quated(sexpr):
            return True
        else: #TODO add unquated support
            return False

### Variable ###

class Variable(AbstractSchemeExpr):
    def __init__(self,sexpr):
        self.value = AbstractSexpr.get_value(sexpr)

    def is_variable(sexpr):
    # predicate for recognizing if then else expr
        if isinstance(sexpr,Symbol): #and not Symbol.get_value(sexpr) in key_words:
            return True;
        elif Symbol.get_value(sexpr) in key_words:
            print("Error: is a key word" +  str(sexpr)) #TODO maybe throw exception
        return True;


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
    def __init__(self,expr,ete): # expand to else
        irt = expr.get_cdr() # if rest of tokens
        pred_expr,irt = irt.get_value()
        then_expr,irt = irt.get_value()
        if isinstance(irt,Pair):
            else_expr = irt.get_car();
            self.else_expr = AbstractSchemeExpr.process(else_expr)
        else:
            self.else_expr = Constant(Void())
        self.predicate = AbstractSchemeExpr.process(pred_expr)
        self.then_expr = AbstractSchemeExpr.process(then_expr)

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

