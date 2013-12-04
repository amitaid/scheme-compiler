from sexprs import *

key_words = ['DEFINE', 'LAMBDA', 'λ', 'IF', 'AND', 'OR', 'COND']
primitive_ops = ['+', '-']

### sexprs predicates ###

class SyntaxError(Exception):
    pass


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
        sexpr = sexpr.cdr

    return is_nil(sexpr)

### AbstractSchemeExpr Predicates ###

def is_quoted(sexpr): # TODO implement later
    if is_pair(sexpr) and \
            is_symbol(sexpr.car) and \
                    sexpr.car.get_value() == 'quote':
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
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'IF'


def is_define(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'DEFINE'


def is_applic(expr):
    return is_proper_list(expr)


def is_lambda(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'LAMBDA'

# These will only be called if is_lambda succeeded
def is_lambda_simple(sexpr):
    return is_proper_list(sexpr.cdr.car)


def is_lambda_var(sexpr):
    return is_symbol(sexpr.cdr.car)


def is_lambda_opt(sexpr):
    return is_pair(sexpr.cdr.car) and not is_proper_list(sexpr.cdr.car)


def is_quasiquoted(expr):
    return is_proper_list(expr) and expr.car.get_value() == 'quasiquote'


def is_unquote(expr):
    return is_proper_list(expr) and expr.car.get_value() == 'unquote'


def is_unquote_splicing(expr):
    return is_proper_list(expr) and expr.car.get_value() == 'unquote-splicing'


def is_let(expr):
    return is_proper_list(expr) and expr.car.get_value() == 'LET'


def is_let_star(expr):
    return is_proper_list(expr) and expr.car.get_value() == 'LET*'


def is_letrec(expr):
    return is_proper_list(expr) and expr.car.get_value() == 'LETREC'


def is_cond(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'COND'


#def is_mit_def(sexpr):
#    return is_pair(sexpr) and \
#           is_pair(sexpr.cdr.car) and \
#           not is_proper_list(sexpr.cdr.car)


def is_and(expr):
    return is_proper_list(expr) and \
           is_symbol(expr.car) and \
           str(expr.car) == 'AND'


def is_or(expr):
    return is_proper_list(expr) and \
           is_symbol(expr.car) and \
           str(expr.car) == 'OR'

#------------------------------------

# Helper function to expand a pair list to a python list
def pair_to_list(sexpr):
    res = []
    while is_pair(sexpr):
        res.append(sexpr.car)
        sexpr = sexpr.cdr

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
    def expand_let(sexpr):
        varvals = sexpr.cdr.car
        body = sexpr.cdr.cdr.car
        if is_nil(varvals):
            return Pair(Pair(Symbol('LAMBDA'), [Nil(), body, Nil()]), [Nil()])
        else:
            variables = []
            values = []
            while not is_nil(varvals):
                variables.append(varvals.car.car)
                values.append(varvals.car.cdr.car)
                varvals = varvals.cdr

            variables = Pair(variables[0], variables[1:] + [Nil()])
            values = Pair(values[0], values[1:] + [Nil()])
            return Pair(Pair(Symbol('LAMBDA'), [variables, body, Nil()]), [values])

    @staticmethod
    def expand_let_star(sexpr):
        varvals = sexpr.cdr.car
        if is_nil(varvals):
            return sexpr.cdr.cdr
        else:
            first = varvals.car
            sexpr.cdr.car = varvals.cdr
            return Pair(Symbol('LET'), [Pair((first), [Nil()]), sexpr, Nil()])


    @staticmethod
    def expand_cond(sexpr):
        body_list = pair_to_list(sexpr.cdr)[::-1]
        res = Nil()
        if len(body_list) == 0 or not is_pair(body_list[0]):
            raise SyntaxError
        if body_list[0].car.get_value() == 'ELSE':
            res = body_list[0].cdr.car
            body_list = body_list[1:]

        while body_list:
            res = Pair(Symbol('IF'),
                       [body_list[0].car,
                        body_list[0].cdr.car,
                        res, Nil()])
            body_list = body_list[1:]

        return res

    @staticmethod
    def expand_and(sexpr):
        first = sexpr.cdr.car
        if is_pair(sexpr.cdr.cdr):
            sexpr.cdr = sexpr.cdr.cdr
            return Pair(Symbol('IF'), [first, sexpr, Boolean('#f'), Nil()])
        else:
            return Pair(Symbol('IF'), [first, first, Boolean('#f'), Nil()])


    @staticmethod
    def build_applic(sexpr):
        func = AbstractSchemeExpr.process(sexpr.car)
        args = list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.cdr)))
        return Applic(func, args)


    @staticmethod
    def build_lambda(sexpr):
        body = AbstractSchemeExpr.process(sexpr.cdr.cdr.car)

        if is_lambda_simple(sexpr):
            variables = list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.cdr.car)))
            return LambdaSimple(variables, body)

        elif is_lambda_var(sexpr):
            var_list = AbstractSchemeExpr.process(sexpr.cdr.car)
            return LambdaVar(var_list, body)

        elif is_lambda_opt(sexpr):
            l = pair_to_list(sexpr.cdr.car)
            variables = l[:-1]
            var_remaining = l[-1]
            return LambdaOpt(variables, var_remaining, body)

    @staticmethod
    def build_if(sexpr):
        parsed_sexpr = list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.cdr)))
        if len(parsed_sexpr) < 2 or len(parsed_sexpr) > 3:
            print('error: exception is supposed to be here - not valid number of args')
            return True

        predicate = parsed_sexpr[0]
        then_body = parsed_sexpr[1]

        if len(parsed_sexpr) == 2:
            return IfThenElse(predicate, then_body, Constant(Void()))
        return IfThenElse(predicate, then_body, parsed_sexpr[2])

    @staticmethod
    def build_or(sexpr):
        return Or(list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.cdr))))

    @staticmethod
    def build_define(sexpr):
        pass


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
            return AbstractSchemeExpr.process(AbstractSchemeExpr.expand_let(sexpr))
        elif is_let_star(sexpr):
            return AbstractSchemeExpr.process(AbstractSchemeExpr.expand_let_star(sexpr))
        elif is_letrec(sexpr):
            return True
        elif is_cond(sexpr):
            return AbstractSchemeExpr.process(AbstractSchemeExpr.expand_cond(sexpr))
        elif is_and(sexpr):
            return AbstractSchemeExpr.process(AbstractSchemeExpr.expand_and(sexpr))
        elif is_quasiquoted(sexpr):
            return True
        elif is_unquote(sexpr):
            return True
        elif is_unquote_splicing(sexpr):
            return True

        # core forms
        elif is_if(sexpr):
            return AbstractLambda.build_if(sexpr)
        elif is_define(sexpr):
            return AbstractSchemeExpr.build_define(sexpr)
        elif is_or(sexpr):
            return AbstractSchemeExpr.build_or(sexpr)
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
        return str(self.value)


### Variable ###

class Variable(AbstractSchemeExpr):
    def __init__(self, symbol):
        self.name = symbol.get_value()

    def __str__(self):
        return self.name


### Core Forms ###

class IfThenElse(AbstractSchemeExpr):
    def __init__(self, predicate, then_body, else_body):
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body

    def __str__(self):
        return '(if ' + str(self.predicate) + ' ' + str(self.then_body) + ' ' + str(self.else_body) + ')'


class Applic(AbstractSchemeExpr):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        return '(' + str(self.func) + ' ' + ' '.join([str(x) for x in self.args]) + ')'


class Or(AbstractSchemeExpr):
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return '(or ' + ' '.join(list(map(str, self.elements))) + ')'


class Define(AbstractSchemeExpr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return '(define ' + str(self.name) + ' ' + str(self.value) + ')'


### Lambda Forms ###

class AbstractLambda(AbstractSchemeExpr):
    pass


class LambdaSimple(AbstractLambda):
    def __init__(self, variables, body):
        self.variables = variables
        self.body = body

    def __str__(self):
        return '(λ (' + ' '.join([str(x) for x in self.variables]) + ')\n\t\t\t' + str(self.body) + ')'


class LambdaVar(AbstractLambda):
    def __init__(self, var_list, body):
        self.var_list = var_list
        self.body = body

    def __str__(self):
        return '(λ ' + str(self.var_list) + '\n\t\t\t' + str(self.body) + ')'


class LambdaOpt(AbstractLambda):
    def __init__(self, variables, var_list, body):
        self.variables = variables
        self.var_list = var_list
        self.body = body

    def __str__(self):
        return '(λ (' + ' '.join([str(x) for x in self.variables]) + \
               ' . ' + str(self.var_list) + ')\n\t\t\t' + str(self.body) + ')'


class SyntacticSugar(AbstractSchemeExpr):
    pass

    def ic_2_nextedifs(expr): # cond -> if transformation
        pass

