from tkinter import constants
from sexprs import *
import reader

key_words = ['Define', 'Lambda','λ','IF','and','or','cond']
primitive_ops =['+','-']

class AbstractSchemeExpr:

    @staticmethod
    def parse(input):
        result, remaining = AbstractSexpr.readFromString(input)
        print(result)
        scheme_expr = AbstractSchemeExpr.process(result)
        return scheme_expr

    @staticmethod  # where the actual parsing occur
    def process(result):
        if Constant.is_const(result):
            print('bla')
            ast = Constant(result)  # abstract syntax tree
        elif Applic.is_applic(result):
            print('bla5')
            ast = Applic(result)
        elif Variable.is_variable(result):
            print('bla2')
            ast =Variable(result)
        elif IfThenElse.is_if(result):
            print('bla3')
            ast = IfThenElse(result)
        elif Def.is_def(result):
            print('bla4')
            ast = Def(result)
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
            print(isinstance(self.expr,Pair))
            quate,rest = self.expr.get_value()

            arg,nil = Pair.get_value(rest)
            return 'Constant('+str(quate)+' '+str(arg)+')'
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
            return True
        elif Constant.is_quated(sexpr):
            return True
        else: #TODO add unquated support
            return False

### Variable ###

class Variable(AbstractSchemeExpr):
    def __init__(self,sexpr):
        self.value = Symbol.get_value(sexpr)

    def __str__(self):
        return 'Variable('+str(self.value)+')'

    # predicate for recognizing if then else expr
    def is_variable(sexpr):
        if isinstance(sexpr,Symbol) and \
        not Symbol.get_value(sexpr) in key_words: # and \
        #not Symbol.get_value(sexpr) in primitive_ops:
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

    def __init__(self,expr):
        op,rest = expr.get_value()
        self.operator = AbstractSchemeExpr.process(op)
        self.args = []
        while not isinstance(rest,Nil):
            arg,rest = rest.get_value()
            self.args.append(AbstractSchemeExpr.process(arg))
        b = False;

    def __str__(self):
        ans = 'Applic('+str(self.operator)
        for arg in self.args:
            ans +=  ','+str(arg)
        return ans + ')'

    def is_applic(expr):
        if isinstance(expr,Pair):
            op_word,rest = expr.get_value()
            print(str(op_word.get_value()) in primitive_ops)
            if isinstance(op_word,Symbol) and \
                str(op_word.get_value())in primitive_ops :
                while not isinstance(rest,Nil):
                    nov,rest = rest.get_value() # nov = number or var
                    if not isinstance(nov,AbstractNumber) \
                    and not isinstance(nov,Symbol):
                         return False
                return True
        return False

class Or(AbstractSchemeExpr):
    pass

    def is_or(expr):
        # a predicate for recognizing or expressions
        pass

class Def(AbstractSchemeExpr):

    def __init__(self,expr):
        def_word,rest = expr.get_value()
        defined_var,rest = rest.get_value()
        self.var = AbstractSchemeExpr.process(defined_var)
        self.val = AbstractSchemeExpr.process(rest.get_car())


    def __str__(self):
        return 'Define(' + str(self.var) + ',' + str(self.val) + ')'

    # a predicate for recognizing definition expressions
    def is_def(expr):
        if isinstance(expr,Pair):
            def_word,rest = expr.get_value()
            if isinstance(def_word,Symbol) \
                and  str(def_word.get_value()) == 'DEFINE' \
                and isinstance(rest,Pair):
                defined_var,rest = rest.get_value()   # can the defined var be a keyword?
                if isinstance(defined_var,Symbol) \
                and isinstance(rest,Pair):
                    val_expr,rest = rest.get_value()
                    if isinstance(rest,Nil):
                        return True
        return False

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

    def is_mit_def(expr):
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

