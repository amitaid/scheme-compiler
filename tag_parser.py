from sexprs import *
from reader import list_to_pair

key_words = ['DEFINE', 'LAMBDA', 'λ', 'IF', 'AND', 'OR', 'COND']
primitive_ops = ['+', '-']

### sexprs predicates ###

gen_sym_counter = 0


class InvalidSyntax(Exception):
    pass


def gen_sym():
    global gen_sym_counter
    new_gen_sym = '@' + str(gen_sym_counter)
    gen_sym_counter += 1
    return Symbol(new_gen_sym)


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


def is_vector(sexpr):
    return isinstance(sexpr, Vector)


def is_proper_list(sexpr):
    if is_nil(sexpr):
        return False

    while is_pair(sexpr):
        sexpr = sexpr.cdr

    return is_nil(sexpr)

### AbstractSchemeExpr Predicates ###

def is_quote(sexpr): # TODO implement later
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'quote'


def is_const(sexpr):
    return is_boolean(sexpr) or \
           is_char(sexpr) or \
           is_number(sexpr) or \
           is_string(sexpr) or \
           is_nil(sexpr) or \
           is_void(sexpr)


def is_variable(sexpr):
    return is_symbol(sexpr) and \
           not sexpr.get_value() in key_words # and \
    #not Symbol.get_value(sexpr) in primitive_ops:

# predicate for both IfThen & IfThenElse
def is_if(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'IF'


def is_define(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'DEFINE'


def is_applic(sexpr):
    return is_proper_list(sexpr)


def is_lambda(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'LAMBDA'

# These will only be called if is_lambda succeeded
def is_lambda_simple(sexpr):
    return is_nil(sexpr.cdr.car) or is_proper_list(sexpr.cdr.car)


def is_lambda_var(sexpr):
    return is_symbol(sexpr.cdr.car)


def is_lambda_opt(sexpr):
    return is_pair(sexpr.cdr.car) and \
           not is_proper_list(sexpr.cdr.car)


def is_quasiquoted(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'quasiquote'


def is_unquote(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'unquote'


def is_unquote_splicing(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'unquote-splicing'


def is_let(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'LET'


def is_let_star(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'LET*'


def is_letrec(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'LETREC'


def is_cond(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'COND'


def is_mit_def(sexpr):
    return is_proper_list(sexpr.cdr.car)


def is_and(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           str(sexpr.car) == 'AND'


def is_or(sexpr):
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           str(sexpr.car) == 'OR'

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

######## Builders and expanders #########

def expand_let(sexpr):
    varvals = pair_to_list(sexpr.cdr.car)
    body = sexpr.cdr.cdr.car
    if varvals:
        variables = []
        values = []
        for varval in varvals:
            variables.append(varval.car)
            values.append(varval.cdr.car)

        variables = list_to_pair(variables + [Nil()])
        values = list_to_pair(values + [Nil()])
        return Pair(Pair(Symbol('LAMBDA'),
                         Pair(variables,
                              Pair(body, Nil()))),
                    values)
    else:
        return Pair(Pair(Symbol('LAMBDA'),
                         Pair(Nil(),
                              Pair(body, Nil()))),
                    Nil())


def expand_let_star(sexpr):
    varvals = pair_to_list(sexpr.cdr.car)[::-1]
    body = sexpr.cdr.cdr.car
    if varvals:
        for varval in varvals:
            var = Pair(varval.car, Nil())
            val = Pair(varval.cdr.car, Nil())
            body = Pair(Pair(Symbol('LAMBDA'),
                             Pair(var,
                                  Pair(body, Nil()))),
                        val)
        return body
        #
        #first = varvals.car
        #sexpr.cdr.car = varvals.cdr
        #return Pair(Symbol('LET'),
        #            Pair(Pair(first, Nil()),
        #                 Pair(sexpr, Nil())))
    else:
        Pair(Pair(Symbol('LAMBDA'),
                  Pair(Nil(),
                       Pair(body, Nil()))),
             Nil())


def expand_letrec(sexpr):
    varvals = pair_to_list(sexpr.cdr.car)
    body = sexpr.cdr.cdr.car
    if varvals:
        variables = []
        body_and_les = [body]
        for varval in varvals:
            variables.append(varval.car)
            body_and_les.append(varval.cdr.car)

        variables = list_to_pair([gen_sym()] + variables + [Nil()])

        lambdas = []
        for i in range(len(body_and_les)):
            lambdas.append(Pair(Symbol('LAMBDA'),
                                Pair(variables,
                                     Pair(body_and_les[i], Nil()))))

        lambdas = list_to_pair(lambdas + [Nil()])
        return Pair(Symbol('Yag'), Pair(lambdas, Nil()))
    else:
        return Pair(Pair(Symbol('LAMBDA'),
                         Pair(Nil(),
                              Pair(body, Nil()))),
                    Nil())


def expand_cond(sexpr):
    body_list = pair_to_list(sexpr.cdr)[::-1]
    res = Nil()
    if len(body_list) == 0 or not is_pair(body_list[0]):
        raise InvalidSyntax
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


def expand_and(sexpr):
    first = sexpr.cdr.car
    if is_pair(sexpr.cdr.cdr):
        sexpr.cdr = sexpr.cdr.cdr
        return Pair(Symbol('IF'),
                    Pair(first,
                         Pair(sexpr,
                              Pair(Boolean('#f'), Nil()))))
    else:
        return Pair(Symbol('IF'),
                    Pair(first,
                         Pair(first,
                              Pair(Boolean('#f'), Nil()))))


def expand_mit_define(sexpr):
    name = sexpr.cdr.car.car
    args = sexpr.cdr.car.cdr
    body = sexpr.cdr.cdr.car
    sexpr.cdr.car = name
    sexpr.cdr.cdr = Pair(Symbol('LAMBDA'),
                         Pair(args,
                              Pair(body,
                                   Nil())))

    return sexpr


def expand_quasiquote(sexpr):
    #print(str(sexpr))
    if is_unquote(sexpr):
        return sexpr.cdr.car
    elif is_unquote_splicing(sexpr):
        raise InvalidSyntax('unquote-splicing here makes no sense!')
    elif is_pair(sexpr):
        a = sexpr.car
        b = sexpr.cdr
        if is_unquote_splicing(a):
            return Pair(Symbol('quasiquote'),
                        Pair(Symbol('append'),
                             Pair(Pair(Symbol('unquote'),
                                       Pair(Pair(a.cdr.car,
                                                 Nil()),
                                            Nil())),
                                  Pair(Pair(Symbol('unquote'),
                                            Pair(Pair(Symbol('expand-qq'),
                                                      Pair(b,
                                                           Nil())),
                                                 Nil())),
                                       Nil()))))
        elif is_unquote_splicing(b):
            return Pair(Symbol('quasiquote'),
                        Pair(Symbol('cons'),
                             Pair(Pair(Symbol('unquote'),
                                       Pair(Pair(Symbol('expand-qq'),
                                                 Pair(a,
                                                      Nil())),
                                            Nil())),
                                  Pair(Pair(Symbol('unquote'),
                                            Pair(Pair(b.cdr.car,
                                                      Nil()),
                                                 Nil())),
                                       Nil()))))
        else:
            return Pair(Symbol('quasiquote'),
                        Pair(Symbol('cons'),
                             Pair(Pair(Symbol('unquote'),
                                       Pair(Pair(Symbol('expand-qq'),
                                                 Pair(a,
                                                      Nil())),
                                            Nil())),
                                  Pair(Pair(Symbol('unquote'),
                                            Pair(Pair(Symbol('expand-qq'),
                                                      b),
                                                 Nil())),
                                       Nil()))))
    elif is_vector(sexpr):
        return Pair(Symbol('quasiquote'),
                    Pair(Symbol('list->vector'),
                         Pair(Pair(Symbol('unquote'),
                                   Pair(Pair(Symbol('expand-qq'),
                                             Pair(Pair(Symbol('vector->list'),
                                                       Pair(sexpr,
                                                            Nil())),
                                                  Nil())),
                                        Nil())),
                              Nil())))
    elif is_nil(sexpr) or is_symbol(sexpr):
        return Pair(Symbol('quasiquote'),
                    Pair(Pair(Symbol('quote'),
                              Pair(Pair(Symbol('unquote'),
                                        Pair(sexpr,
                                             Nil())),
                                   Nil())),
                         Nil()))
    else:
        return sexpr


def build_applic(sexpr):
    func = AbstractSchemeExpr.process(sexpr.car)
    args = list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.cdr)))
    return Applic(func, args)


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


def build_if(sexpr):
    parsed_sexpr = list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.cdr)))
    if len(parsed_sexpr) < 2 or len(parsed_sexpr) > 3:
        raise InvalidSyntax('Incorrect number of arguments for IF')

    predicate = parsed_sexpr[0]
    then_body = parsed_sexpr[1]

    if len(parsed_sexpr) == 2:
        return IfThenElse(predicate, then_body, Constant(Void()))
    else:
        return IfThenElse(predicate, then_body, parsed_sexpr[2])


def build_or(sexpr):
    return Or(list(map(AbstractSchemeExpr.process, pair_to_list(sexpr.cdr))))


def build_define(sexpr):
    var = AbstractSchemeExpr.process(sexpr.cdr.car)
    expr = AbstractSchemeExpr.process(sexpr.cdr.cdr.car)
    return Def(var, expr)


class AbstractSchemeExpr:
    @staticmethod
    def parse(input_string):
        #print('hi')
        sexpr, remaining = AbstractSexpr.readFromString(input_string)
        print(sexpr)
        expanded = AbstractSchemeExpr.expand(sexpr)
        print(sexpr)
        scheme_expr = AbstractSchemeExpr.process(expanded)
        print(sexpr)
        return scheme_expr

    @staticmethod
    def expand(sexpr):
        if is_let(sexpr):
            return expand_let(sexpr)
        elif is_let_star(sexpr):
            return expand_let_star(sexpr)
        elif is_letrec(sexpr):
            return expand_letrec(sexpr)
        elif is_cond(sexpr):
            return expand_cond(sexpr)
        elif is_and(sexpr):
            return expand_and(sexpr)
        elif is_quasiquoted(sexpr):
            return expand_quasiquote(sexpr.cdr.car)
        else:
            return sexpr

    @staticmethod  # where the actual parsing occur
    def process(sexpr):
        # basic
        if is_const(sexpr):
            return Constant(sexpr)
        elif is_vector(sexpr):
            return Constant(Vector(list(map(AbstractSchemeExpr.process, sexpr.get_value()))))
        elif is_variable(sexpr):
            return Variable(sexpr)
        elif is_quote(sexpr):
            return Constant(AbstractSchemeExpr.process(sexpr.cdr.car))
        elif is_quasiquoted(sexpr):
            return Constant(AbstractSchemeExpr.process(sexpr.cdr.car))

        # Lambda forms
        elif is_lambda(sexpr):
            return build_lambda(sexpr)

        # core forms
        elif is_if(sexpr):
            return build_if(sexpr)
        elif is_define(sexpr):
            if is_mit_def(sexpr):
                return AbstractSchemeExpr.process(expand_mit_define(sexpr))
            return build_define(sexpr)
        elif is_or(sexpr):
            return build_or(sexpr)
        elif is_applic(sexpr): # must always come last
            return build_applic(sexpr)
        else:
            print('format not supported: ' + str(sexpr))
            return Constant(Void()) #TODO in my opinion we should raise an exception here


### Constant ###
class Constant(AbstractSchemeExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if isinstance(self.value, Constant):
            return "'" + str(self.value)
        else:
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
        return '(' + ' '.join([str(self.func)] + [str(x) for x in self.args]) + ')'


class Or(AbstractSchemeExpr):
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return '(' + ' '.join(['or'] + [str(x) for x in self.elements]) + ')'


class Def(AbstractSchemeExpr):
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
        return '(lambda (' + ' '.join([str(x) for x in self.variables]) + ') ' + str(self.body) + ')'


class LambdaVar(AbstractLambda):
    def __init__(self, var_list, body):
        self.var_list = var_list
        self.body = body

    def __str__(self):
        return '(lambda ' + str(self.var_list) + ' ' + str(self.body) + ')'


class LambdaOpt(AbstractLambda):
    def __init__(self, variables, var_list, body):
        self.variables = variables
        self.var_list = var_list
        self.body = body

    def __str__(self):
        return '(lambda (' + ' '.join([str(x) for x in self.variables]) + \
               ' . ' + str(self.var_list) + ')' + str(self.body) + ')'
