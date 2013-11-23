from email._header_value_parser import get_token
from sexprs import *


key_words = ['define', 'lambda','λ','if','else','then','and','or','cond']

class AbstractSchemeExpr:
    @staticmethod
    def parse(input):
        result, remaining = AbstractSexpr.readFromString(input)
        # dealing with core forms

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
        if isinstance(sexpr,Boolean) or  isinstance(sexpr,Char) \
            or  isinstance(sexpr,AbstractNumber) or  isinstance(sexpr,String):
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
    pass

    def is_if_then_else(expr):
        # first check if it is a pair at all
        if isinstance(expr,Pair):
            if_token = expr.get_car()
            rest_expr = expr.get_cdr()
            # second check if first token is if and rest is pair
            if isinstance(if_token,Symbol) and \
                str(if_token.get_value()) == 'IF' and \
                isinstance(rest_expr,Pair):

            #    predicate = rest_expr.get_car()  # extracts the pred - not needed
                rest_expr2 = rest_expr.get_cdr()

                # third check the then argument exists
                if isinstance(rest_expr2,Pair):

                 #   then_expr = rest_expr2.get_car() # extracts the then - not needed
                    rest_expr3 = rest_expr2.get_cdr()
                    # fourth check if the else arg exists

                    if isinstance(rest_expr3,Pair): # case proper list

                 #       else_expr = rest_expr3.get_car() # extracts the else - not needed
                        rest = rest_expr3.get_cdr()
                        if isinstance(rest,Nil):  # checks if the list end is Nil
                            return True
        #            elif not isinstance(rest_expr3,Nil): # case not improper
        #                return True
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

    # predicate for recognizing ifthen expr
    def is_if_then(expr):
        # first check if it is a pair at all
        if isinstance(expr,Pair):
            if_token = expr.get_car()
            rest_expr = expr.get_cdr()
            # second check if first token is if and rest is pair
            if isinstance(if_token,Symbol) and \
                str(if_token.get_value()) == 'IF' and \
                isinstance(rest_expr,Pair):

            #    predicate = rest_expr.get_car()  # extracts the pred - not needed
                rest_expr2 = rest_expr.get_cdr()

                # third check the then argument exists
                if isinstance(rest_expr2,Pair):

                 #   then_expr = rest_expr2.get_car() # extracts the then - not needed
                    rest = rest_expr2.get_cdr()
                    # fourth check if the rest is nil
                    if isinstance(rest,Nil):  # checks if the list end is Nil
                            return True
        #            elif not isinstance(rest_expr3,Nil): # case not improper
        #                return True
        return False
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

    def it2ite(expr): # if then -> if then else transformation
        if_token = expr.get_car()
        rest = expr.get_cdr()
        pred_expr = rest.get_car()
        rest2 = rest.get_cdr()
        rest2.
    def ic_2_nextedifs(expr): # cond -> if transformation
        pass

