from sexprs import *
import reader

key_words = ['DEFINE', 'LAMBDA', 'λ', 'IF', 'AND', 'OR', 'COND']
primitive_ops = ['+', '-']


def is_void(sexpr):
    return isinstance(sexpr, Void)


def is_nil(sexpr):
    return isinstance(sexpr, Nil)


def is_boolean(sexpr):
    return isinstance(sexpr, Boolean)


def is_number(sexpr):
    return isinstance(sexpr, AbstractNumber)


def is_symbol(sexpr):
    return isinstance(sexpr, Symbol)


def is_char(sexpr):
    return isinstance(sexpr, Char)


def is_string(sexpr):
    return isinstance(sexpr, String)


def is_pair(sexpr):
    return isinstance(sexpr, Pair)


def is_proper_list(sexpr):
    if is_nil(sexpr):
        return False

    while is_pair(sexpr):
        sexpr = sexpr.get_cdr()

    return is_nil(sexpr)


def is_quoted(sexpr): # TODO implement later
    if is_pair(sexpr) and \
            is_symbol(sexpr.get_car()) and \
                    sexpr.get_car().get_value() in reader.quotes_dict.values():
        return True
    return False


def is_const(sexpr):
    if is_boolean(sexpr) or \
            is_char(sexpr) or \
            is_number(sexpr) or \
            is_string(sexpr) or \
            is_nil(sexpr) or \
            is_void(sexpr): # maybe the last condition is useless
        return True
    elif is_quoted(sexpr):
        return True
    else: #TODO add unquoted support
        return False


def is_variable(sexpr):
    if is_symbol(sexpr) and \
            not sexpr.get_value() in key_words: # and \
    #not Symbol.get_value(sexpr) in primitive_ops:
        return True
    return False

# predicate for both IfThen & IfThenElse
def is_if(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.get_car()) and \
           sexpr.get_car().get_value() == 'IF'


def is_def_expr(expr):
    if not is_proper_list(expr):
        return False

    def_word, rest = expr.get_value()
    if not is_symbol(def_word) or \
            str(def_word.get_value()) != 'DEFINE':
        return False

    if not is_pair(rest):
        return False

    first_part, rest = rest.get_value()
    if not is_pair(rest):
        return False

    second_part, rest = rest.get_value()
    return is_nil(rest)

# a predicate for recognizing definition expressions
def is_simple_def(expr):
    return is_def_expr(expr)


def is_applic(expr):
    return is_proper_list(expr)


def is_lambda(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.get_car()) and \
           sexpr.get_car().get_value() == 'LAMBDA'


def is_lambda_simple(sexpr):
    return is_proper_list(sexpr.get_cdr().get_car())


def is_lambda_var(sexpr):
    return is_symbol(sexpr.get_cdr().get_car())


def is_lambda_opt(sexpr):
    return is_pair(sexpr.get_cdr().get_car()) and not is_proper_list(sexpr.get_cdr().get_car())


def is_quasiquoted(expr):
    pass


def is_let(expr):
    return is_proper_list(expr) and expr.get_car().get_value() == 'LET'


def is_let_star(expr):
    return is_proper_list(expr) and expr.get_car().get_value() == 'LET*'


def is_letrec(expr):
    return is_proper_list(expr) and expr.get_car().get_value() == 'LETREC'


def is_let_body(expr):
    head, rest = expr.get_value()
    op_name = str(head.get_value())
    definitions, rest = rest.get_value()

    while is_pair(definitions):
        #print('inside loop')
        cur_def, definitions = definitions.get_value()
        #print(not isinstance(cur_def,Pair))
        if not is_pair(cur_def):
            return False
        cur_def_var, cur_def = cur_def.get_value()

        if not is_pair(cur_def) or \
                not is_symbol(cur_def_var) or \
                not is_nil(cur_def.get_cdr()):
            return False

        print(op_name == 'LETREC')
        if op_name == 'LETREC' and not \
            (is_lambda_simple(cur_def.get_car()) or
                 is_lambda_var(cur_def.get_car()) or
                 is_lambda_opt(cur_def.get_car())):
            return False

    if not is_nil(definitions) or not is_pair(rest):
        return False

    #TODO Sort the efficiency of this loop. also, huh??? isinstance scheme expr?
    while is_pair(rest):
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
    if not is_symbol(cond_arg) or str(cond_arg) != 'COND':
        return False

    while is_pair(rest):
        inner_cond_expr, rest = rest.get_value()
        if not is_proper_list(inner_cond_expr) or \
                not is_nil(inner_cond_expr.get_cdr().get_cdr()):
            return False

    return True


def is_mit_def(expr):
    if not is_def_expr(expr):
        return False

    nna = expr.get_cdr().get_car()
    if not is_pair(nna) or is_nil(nna.get_cdr()) \
        or is_pair(nna.get_cdr()):
        return False
    return True


def is_and(expr):
    return is_proper_list(expr) and \
           is_symbol(expr.get_car()) and \
           str(expr.get_car()) == 'AND'


def is_or(expr):
    return is_proper_list(expr) and \
           is_symbol(expr.get_car()) and \
           str(expr.get_car()) == 'OR'

#------------------------------------

def pair_to_list(sexpr):
    res = []
    while is_pair(sexpr):
        res.append(sexpr.get_car())
        sexpr = sexpr.get_cdr()

    if not is_nil(sexpr):
        res.append(sexpr)

    return res


class AbstractSchemeExpr:
    @staticmethod
    def parse(input_string):
        result, remaining = AbstractSexpr.readFromString(input_string)
        print(result)
        scheme_expr = AbstractSchemeExpr.process(result)
        return scheme_expr

    @staticmethod
    def build_let(sexpr):
        varvals = sexpr.cdr.car
        body = sexpr.cdr.cdr.car
        if is_nil(varvals):
            return AbstractSchemeExpr.process(Pair(Pair(Symbol('LAMBDA'), [Nil(), body, Nil()]), [Nil()]))
        else:
            variables = []
            values = []
            while not is_nil(varvals):
                variables.append(varvals.get_car().get_car())
                values.append(varvals.get_car().get_cdr().get_car())
                varvals = varvals.get_cdr()

            variables = Pair(variables[0], variables[1:] + [Nil()])
            values = Pair(values[0], values[1:] + [Nil()])
            return AbstractSchemeExpr.process(Pair(Pair(Symbol('LAMBDA'), [variables, body, Nil()]), [values]))

    # TODO Check
    @staticmethod
    def build_applic(sexpr):
        func = AbstractSchemeExpr.process(sexpr.get_car())
        args = list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.get_cdr())))
        return Applic(func, args)


    @staticmethod
    def build_lambda(sexpr):
        body = AbstractSchemeExpr.process(sexpr.get_cdr().get_cdr().get_car())

        if is_lambda_simple(sexpr):
            variables = list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.get_cdr().get_car())))
            return LambdaSimple(variables, body)

        elif is_lambda_var(sexpr):
            var_list = AbstractSchemeExpr.process(sexpr.get_cdr().get_car())
            return LambdaVar(var_list, body)

        elif is_lambda_opt(sexpr):
            l = pair_to_list(sexpr.get_cdr().get_car())
            variables = l[:-1]
            var_remaining = l[-1]
            return LambdaOpt(variables, var_remaining, body)

    @staticmethod  # where the actual parsing occur
    def process(sexpr):
        # basic
        if is_const(sexpr):
            return Constant(sexpr)  # abstract syntax tree
        elif is_variable(sexpr):
            return Variable(sexpr)

        # Lambda forms
        elif is_lambda(sexpr):
            return AbstractSchemeExpr.build_lambda(sexpr)

        #Syntactic Sugars
        elif is_let(sexpr):
            return AbstractSchemeExpr.build_let(sexpr)
        elif is_let_star(sexpr):
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
            return AbstractSchemeExpr.build_applic(sexpr)
        else:
            print('format not supported: ' + str(sexpr))
            return Constant(Void()) #TODO in my opinion we should raise an exception here


    #TODO how to check is or and applic args are valid
    #TODO maybe the checks of args in if and or are meaningless
    #this function  checks if the expr is valid for inner parsing.
    def is_valid(expr):
        return True

        ### Constant ###


class Constant(AbstractSchemeExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Constant(' + str(self.value) + ')'


### Variable ###

class Variable(AbstractSchemeExpr):
    def __init__(self, symbol, value=Void()):
        self.symbol = symbol
        self.value = value

    def __str__(self):
        return 'Variable(' + str(self.symbol) + ')'


### Core Forms ###

class IfThenElse(AbstractSchemeExpr):
    def __init__(self, predicate, then_body, else_body):
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body

    def __str__(self):
        return 'IfThenElse(' + str(self.predicate) + ',' + str(self.then_body) + ',' + str(self.else_body) + ')'


class Applic(AbstractSchemeExpr):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        return 'Applic(' + str(self.func) + ' ' + ' '.join([str(x) for x in self.args]) + ')'


class Or(AbstractSchemeExpr):
    def __init__(self, expr):
        or_arg, rest = expr.get_value()
        #self.or_arg = AbstractSchemeExpr.process(or_arg)
        self.args = []
        while not is_nil(rest):
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
    def __init__(self, variables, body):
        self.variables = variables
        self.body = body

    def __str__(self):
        return 'LambdaSimple( (' + ' '.join([str(x) for x in self.variables]) + ')\n\t\t\t' + str(self.body) + ')'


class LambdaVar(AbstractLambda):
    def __init__(self, var_list, body):
        self.var_list = var_list
        self.body = body

    def __str__(self):
        return 'LambdaVar( ' + str(self.var_list) + '\n\t\t\t' + str(self.body) + ')'


class LambdaOpt(AbstractLambda):
    def __init__(self, variables, var_list, body):
        self.variables = variables
        self.var_list = var_list
        self.body = body

    def __str__(self):
        return 'LambdaOpt( (' + ' '.join([str(x) for x in self.variables]) + \
               ' . ' + str(self.var_list) + ')\n\t\t\t' + str(self.body) + ')'


class SyntacticSugar(AbstractSchemeExpr):
    pass

    def ic_2_nextedifs(expr): # cond -> if transformation
        pass

