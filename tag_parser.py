from sexprs import *
import reader

key_words = ['DEFINE', 'LAMBDA', 'λ', 'IF', 'AND', 'OR', 'COND']
primitive_ops = ['+', '-']


def is_proper_list(expr):
    if not isinstance(expr, Pair):
        return False
    rest = expr.get_cdr()

    while isinstance(rest, Pair):
        rest = rest.get_cdr()

    if not isinstance(rest, Nil):
        return False
    return True


def is_quoted(sexpr): # TODO implement later
    if isinstance(sexpr, Pair) and isinstance(Pair.get_car(sexpr), Symbol) and \
                    Pair.get_car(sexpr).get_value() in reader.quotes_dict.values():
        return True
    return False


def is_const(sexpr):
    if isinstance(sexpr, Boolean) or \
            isinstance(sexpr, Char) or \
            isinstance(sexpr, AbstractNumber) or \
            isinstance(sexpr, String) or \
            isinstance(sexpr, Void): # maybe the last condition is useless
        return True
    elif is_quoted(sexpr):
        return True
    else: #TODO add unquoted support
        return False

# predicate for recognizing if then else expr
def is_variable(sexpr):
    if isinstance(sexpr, Symbol) and \
            not Symbol.get_value(sexpr) in key_words: # and \
    #not Symbol.get_value(sexpr) in primitive_ops:
        return True
    return False

# predicate for both IfThen & IfThenElse
def is_if(expr):
    # first check if it is a pair at all
    if isinstance(expr, Pair):
        if_token, rest_expr = expr.get_value()
        # second check if first token is if and rest is pair
        if isinstance(if_token, Symbol) and \
                        str(if_token.get_value()) == 'IF' and \
                isinstance(rest_expr, Pair):

            rest_expr2 = rest_expr.get_cdr()
            #third check for checking there are enough args in the pairs
            if isinstance(rest_expr2, Pair):

                rest_expr3 = rest_expr2.get_cdr()
                # fourth check if the else arg exists
                # if so it checks if its tail is Nil (IfThenElse)
                # otherwise checks if checks if else is Nil (IfThen)
                if isinstance(rest_expr3, Pair) and \
                        isinstance(rest_expr3.get_cdr(), Nil) or \
                        isinstance(rest_expr3, Nil):
                    return True
    return False


def is_def_expr(expr):
    if not is_proper_list(expr):
        return False

    def_word, rest = expr.get_value()
    if not isinstance(def_word, Symbol) or \
                    str(def_word.get_value()) != 'DEFINE':
        return False

    if not isinstance(rest, Pair):
        return False

    first_part, rest = rest.get_value()
    if not isinstance(rest, Pair):
        return False

    second_part, rest = rest.get_value()
    return isinstance(rest, Nil)

# a predicate for recognizing definition expressions
def is_simple_def(expr):
    return is_def_expr(expr)


def is_applic(expr):
    return is_proper_list(expr)
    # TODO need to make sure which option is correct
    #if isinstance(expr,Pair):
    #    op_word,rest = expr.get_value()
    #
    #
    #
    #    if isinstance(op_word,Symbol):
    #        return AbstractSchemeExpr.is_proper_list(rest)
    #return False


def is_lambdaInstance(expr):
    b = is_proper_list(expr) and \
        isinstance(expr.get_car(), Symbol) and \
        (str(expr.get_car().get_value()) == 'LAMBDA')
    return b


def is_lambda_simple(expr):
    if not is_lambdaInstance(expr):
        return False

    rest = expr.get_cdr()
    args_list, rest = rest.get_value()

    #TODO maybe to add a test that all the variables in the args are different
    if not is_proper_list(args_list):
        return False

    #while isinstance(args_list,Pair):
    #    arg,args_list = args_list.get_value()
    #    if not isinstance(arg,Symbol):
    #        return False
    return True


def is_lambda_var(expr):
    if not is_lambdaInstance(expr):
        return False

    rest = expr.get_cdr()
    lambda_var_arg = rest.get_car()
    if not isinstance(lambda_var_arg, Symbol):
        return False
    return True


def is_lambda_opt(expr):
    if not is_lambdaInstance(expr):
        return False

    rest = expr.get_cdr()
    args = rest.get_car()
    if not isinstance(args, Pair) or is_proper_list(args):
        return False

    #TODO maybe to add a test that all the variables in the args are different
    #while isinstance(args,Pair):
    #    arg,args = args.get_value()
    #    if not isinstance(arg,Symbol):
    #        return False

    #if not isinstance(args,Symbol):
    #    return False
    return True


def is_quasiquoted(expr):
    pass


def is_let(expr):
    if not is_proper_list(expr):
        return False

    if not isinstance(expr.get_car(), Symbol) or \
                    str(expr.get_car().get_value()) != 'LET':
        return False

    return is_let_body(expr)


def is_letStar(expr):
    if not is_proper_list(expr):
        return False

    if not isinstance(expr.get_car(), Symbol) or \
                    str(expr.get_car().get_value()) != 'LET*':
        return False

    return is_let_body(expr)


def is_letrec(expr):
    if not is_proper_list(expr):
        return False

    if not isinstance(expr.get_car(), Symbol) or \
                    str(expr.get_car().get_value()) != 'LETREC':
        return False

    return is_let_body(expr)


def is_let_body(expr):
    head, rest = expr.get_value()
    op_name = str(head.get_value())
    definitions, rest = rest.get_value()

    while isinstance(definitions, Pair):
        #print('inside loop')
        cur_def, definitions = definitions.get_value()
        #print(not isinstance(cur_def,Pair))
        if not isinstance(cur_def, Pair):
            return False
        cur_def_var, cur_def = cur_def.get_value()

        if not isinstance(cur_def, Pair) or \
                not isinstance(cur_def_var, Symbol) or \
                not isinstance(cur_def.get_cdr(), Nil):
            return False

        print(op_name == 'LETREC')
        if op_name == 'LETREC' and not \
            (is_lambda_simple(cur_def.get_car()) or
                 is_lambda_var(cur_def.get_car()) or
                 is_lambda_opt(cur_def.get_car())):
            return False

    if not isinstance(definitions, Nil) or not isinstance(rest, Pair):
        return False

    #TODO Sort the efficiency of this loop
    while isinstance(rest, Pair):
        cur_exp, rest = rest.get_value()
        #where <LE1>, <LE2>, etc, are λ-expressions, and <expr> is some instance of AbstractSchemeExpr,
        if op_name == 'LETREC' and \
                not isinstance(AbstractSchemeExpr.process(cur_exp), AbstractSchemeExpr):
            return False

    return True

    #while isinstance(rest.get_car(),Pair):
    #    lei_expr = rest.get_car().get_cdr() # lei = let expression i

    # this if makes sure each inner define is in proper list with length 2
    #           if not isinstance(lei_expr,Pair) or not isinstance(lei_expr.get_cdr(),Nil):
    #              return False

#
#           if(op_name == 'LETREC') and not isinstance(lei_expr.get_car(),AbstractLambda):
#              return False
#         rest = rest.get_cdr()

#    return isinstance(rest.get_cdr,Nil)

def is_cond(expr):
    if not is_proper_list(expr):
        return False

    cond_arg, rest = expr.get_value()
    if not isinstance(cond_arg, Symbol) or str(cond_arg) != 'COND':
        return False

    while isinstance(rest, Pair):
        inner_cond_expr, rest = rest.get_value()
        if not is_proper_list(inner_cond_expr) or \
                not isinstance(inner_cond_expr.get_cdr().get_cdr(), Nil):
            return False

    return True


def is_mit_def(expr):
    if not is_def_expr(expr):
        return False

    nna = expr.get_cdr().get_car()
    if not isinstance(nna, Pair) or isinstance(nna.get_cdr(), Nil) \
        or isinstance(nna.get_cdr(), Pair):
        return False
    return True


def is_and(expr):
    return is_proper_list(expr) and \
           isinstance(expr.get_car(), Symbol) and \
           str(expr.get_car()) == 'AND'


def is_or(expr):
    if isinstance(expr, Pair):
        or_arg, rest = expr.get_value()
        if isinstance(or_arg, Symbol) and \
                        str(or_arg.get_value()) == 'OR':
            return is_proper_list(rest)

    return False

#------------------------------------

class AbstractSchemeExpr:
    @staticmethod
    def parse(input):
        result, remaining = AbstractSexpr.readFromString(input)
        print(result)
        scheme_expr = AbstractSchemeExpr.process(result)
        return scheme_expr

    @staticmethod  # where the actual parsing occur
    def process(sexpr):
        # basic
        if is_const(sexpr):
            return Constant(sexpr)  # abstract syntax tree
        elif is_variable(sexpr):
            return Variable(sexpr)

        # Lambda forms
        elif is_lambda_simple(sexpr):
            return LambdaSimple(sexpr)
        elif is_lambda_var(sexpr):
            return LambdaVar(sexpr)
        elif is_lambda_opt(sexpr):
            return LambdaOpt(sexpr)

        #Syntactic Sugars
        elif is_let(sexpr):
            varvals = sexpr.cdr.car
            body = sexpr.cdr.cdr.car
            if isinstance(varvals, Nil):
                AbstractSchemeExpr.process(Pair(Pair(Symbol('LAMBDA'), [Nil(), body, Nil()]), [Nil()]))
            else:
                vars = []
                vals = []
                while not isinstance(varvals, Nil):
                    vars.append(varvals.car.car)
                    vals.append(varvals.car.cdr.car)
                    varvals = varvals.cdr
                vars = Pair(vars[0], vars[1:] + [Nil()])
                vals = Pair(vals[0], vals[1:] + [Nil()])
                return Applic(Pair(Pair(Symbol('LAMBDA'), [vars, body, Nil()]), vals))


        elif is_letStar(sexpr):
            return True
        elif is_letrec(sexpr):
            return True
        elif is_mit_def(sexpr):
            return True
        elif is_cond(sexpr):
            return True
        elif is_and(sexpr):
            return True

        # core forms
        elif is_if(sexpr):
            return IfThenElse(sexpr)
        elif is_simple_def(sexpr):
            return Def(sexpr)
        elif is_or(sexpr):
            return Or(sexpr)
        elif is_applic(sexpr): # must always come last
            return Applic(sexpr)
        else:
            print('format not supported: ' + str(sexpr))
            return Constant(Void()) #TODO in my opinion we should raise an exception here


    #TODO how to check is or and applic args are valid
    #TODO maybe the checks of args in if and or are meaningless
    #this function  checks if the expr is valid for inner parsing.
    def isValid(expr):
        return True

        ### Constant ###


class Constant(AbstractSchemeExpr):
    def __init__(self, sexpr):
        self.expr = sexpr

    def __str__(self):
        if isinstance(self.expr, Pair):
            print(isinstance(self.expr, Pair))
            quote, rest = self.expr.get_value()

            arg, nil = Pair.get_value(rest)
            return 'Constant(' + str(quote) + ' ' + str(arg) + ')'
        else:
            return 'Constant(' + str(self.expr) + ')'


### Variable ###

class Variable(AbstractSchemeExpr):
    def __init__(self, sexpr):
        self.value = Symbol.get_value(sexpr)

    def __str__(self):
        return 'Variable(' + str(self.value) + ')'


### Core Forms ###

class IfThenElse(AbstractSchemeExpr):
    def __init__(self, expr):
        irt = expr.get_cdr() # irt = if rest of tokens
        pred_expr, irt = irt.get_value()
        then_expr, irt = irt.get_value()
        if isinstance(irt, Pair):
            else_expr = irt.get_car()
            self.else_expr = AbstractSchemeExpr.process(else_expr)
        else:
            self.else_expr = Constant(Void())
        self.predicate = AbstractSchemeExpr.process(pred_expr)
        self.then_expr = AbstractSchemeExpr.process(then_expr)

    def __str__(self):
        return 'IfThenElse(' + str(self.predicate) + \
               ',' + str(self.then_expr) + ',' + str(self.else_expr) + ')'


class Applic(AbstractSchemeExpr):
    def __init__(self, expr):
        op, rest = expr.get_value()
        self.operator = AbstractSchemeExpr.process(op)
        self.args = []
        while not isinstance(rest, Nil):
            arg, rest = rest.get_value()
            self.args.append(AbstractSchemeExpr.process(arg))

    def __str__(self):
        ans = 'Applic(' + str(self.operator)
        for arg in self.args:
            ans += ',' + str(arg)
        return ans + ')'


class Or(AbstractSchemeExpr):
    def __init__(self, expr):
        or_arg, rest = expr.get_value()
        #self.or_arg = AbstractSchemeExpr.process(or_arg)
        self.args = []
        while not isinstance(rest, Nil):
            arg, rest = rest.get_value()
            self.args.append(AbstractSchemeExpr.process(arg))

    def __str__(self):
        ans = 'Or('
        for arg in self.args:
            if (arg == self.args[-1]):
                ans += str(arg)
            else:
                ans += str(arg) + ','
        return ans + ')'


class Def(AbstractSchemeExpr):
    def __init__(self, expr):
        def_word, rest = expr.get_value()
        defined_var, rest = rest.get_value()
        self.var = AbstractSchemeExpr.process(defined_var)
        self.val = AbstractSchemeExpr.process(rest.get_car())


    def __str__(self):
        return 'Define(' + str(self.var) + ',' + str(self.val) + ')'


### Lambda Forms ###

class AbstractLambda(AbstractSchemeExpr):
    pass


class LambdaSimple(AbstractLambda):
    def __init__(self, expr):
        rest = expr.get_cdr()
        self.var_list = []
        self.expr_list = []
        vars, rest = rest.get_value()

        while isinstance(vars, Pair):
            var, vars = vars.get_value()
            self.var_list.append(AbstractSchemeExpr.process(var))

        while isinstance(rest, Pair):
            cur_expr, rest = rest.get_value()
            self.expr_list.append(AbstractSchemeExpr.process(cur_expr))

    def __str__(self):
        ans = 'LambdaSimple( ('
        for var in self.var_list:
            if (var == self.var_list[-1]):
                ans += str(var) + ')'
            else:
                ans += str(var) + ','
        ans += '\n\t\t\t('
        for expr in self.expr_list:
            if (expr == self.expr_list[-1]):
                ans += str(expr) + ') )'
            else:
                ans += str(expr) + ','
        return ans


class LambdaVar(AbstractLambda):
    def __init__(self, expr):
        rest = expr.get_cdr()

        self.expr_list = []
        vars, rest = rest.get_value()
        self.vars = AbstractSchemeExpr.process(vars)

        while isinstance(rest, Pair):
            cur_expr, rest = rest.get_value()
            self.expr_list.append(AbstractSchemeExpr.process(cur_expr))

    def __str__(self):
        ans = 'LambdaVar( (' + str(self.vars) + ')\n\t\t\t('

        for expr in self.expr_list:
            if (expr == self.expr_list[-1]):
                ans += str(expr) + ') )'
            else:
                ans += str(expr) + ','
        return ans


class LambdaOpt(AbstractLambda):
    def __init__(self, expr):
        rest = expr.get_cdr()
        self.var_list = []
        self.expr_list = []
        vars, rest = rest.get_value()

        while isinstance(vars, Pair):
            var, vars = vars.get_value()
            self.var_list.append(AbstractSchemeExpr.process(var))

        self.last_var = AbstractSchemeExpr.process(vars)

        while isinstance(rest, Pair):
            cur_expr, rest = rest.get_value()
            self.expr_list.append(AbstractSchemeExpr.process(cur_expr))

    def __str__(self):
        ans = 'LambdaOpt( ('
        for var in self.var_list:
            ans += str(var) + ','
        ans += str(self.last_var) + ')\n\t\t\t('
        for expr in self.expr_list:
            if (expr == self.expr_list[-1]):
                ans += str(expr) + ') )'
            else:
                ans += str(expr) + ','
        return ans


class SyntacticSugar(AbstractSchemeExpr):
    pass

    def ic_2_nextedifs(expr): # cond -> if transformation
        pass

