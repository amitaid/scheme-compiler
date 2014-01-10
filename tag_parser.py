from sexprs import *

key_words = ['DEFINE', 'LAMBDA', 'λ', 'IF', 'AND', 'OR', 'COND']
primitive_ops = ['+', '-']

### sexprs predicates ###

gen_sym_counter = 0


def gen_sym():
    global gen_sym_counter
    new_gen_sym = '@' + str(gen_sym_counter)
    gen_sym_counter += 1
    return Symbol(new_gen_sym)


label_index = 0


def gen_label():
    global label_index
    new_label = 'L' + str(label_index)
    label_index += 1
    return new_label


class InvalidSyntax(Exception):
    pass


def is_void(sexpr):
    return isinstance(sexpr, Void)


def is_nil(sexpr):
    return isinstance(sexpr, Nil)


def is_boolean(sexpr):
    return isinstance(sexpr, Boolean)


def is_number(sexpr):
    return isinstance(sexpr, AbstractNumber)


def is_integer(sexpr):
    return isinstance(sexpr, Integer)


def is_fraction(sexpr):
    return isinstance(sexpr, Fraction)


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


def is_improper_list(sexpr):
    return is_pair(sexpr) and not is_proper_list(sexpr)

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
           not sexpr.get_value() in key_words

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
    return is_nil(sexpr.cdr.car) or \
           is_proper_list(sexpr.cdr.car)


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
    return is_pair(sexpr.cdr.car)


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
    varvals = [AbstractSchemeExpr.expand(x) for x in pair_to_list(sexpr.cdr.car)]
    body = AbstractSchemeExpr.expand(sexpr.cdr.cdr.car)
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
    varvals = [AbstractSchemeExpr.expand(x) for x in pair_to_list(sexpr.cdr.car)][::-1]
    body = sexpr.cdr.cdr.car
    if varvals:
        for varval in varvals:
            body = Pair(Symbol('LET'),
                        Pair(Pair(varval, Nil()),
                             Pair(body, Nil())))
    else:
        body = Pair(Pair(Symbol('LET'),
                         Pair(Nil(),
                              Pair(body, Nil()))),
                    Nil())
    return AbstractSchemeExpr.expand(body)


def expand_letrec(sexpr):
    varvals = [AbstractSchemeExpr.expand(x) for x in pair_to_list(sexpr.cdr.car)]
    body = AbstractSchemeExpr.expand(sexpr.cdr.cdr.car)
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
                              Pair(body,
                                   Nil()))),
                    Nil())


def expand_cond(sexpr):
    body_list = [AbstractSchemeExpr.expand(x) for x in pair_to_list(sexpr.cdr)][::-1]
    res = Nil()
    if len(body_list) == 0 or not is_pair(body_list[0]):
        raise InvalidSyntax
    if body_list[0].car.get_value() == 'ELSE':
        res = body_list[0].cdr.car
        body_list = body_list[1:]

    for item in body_list:
        res = Pair(Symbol('IF'),
                   Pair(item.car,
                        Pair(item.cdr.car,
                             Pair(res,
                                  Nil()))))
    return res


def expand_and(sexpr):
    first = AbstractSchemeExpr.expand(sexpr.cdr.car)
    if is_pair(sexpr.cdr.cdr):
        sexpr.cdr = sexpr.cdr.cdr
        return Pair(Symbol('IF'),
                    Pair(first,
                         Pair(AbstractSchemeExpr.expand(sexpr),
                              Pair(Boolean('#f'), Nil()))))
    else:
        return Pair(Symbol('IF'),
                    Pair(first,
                         Pair(first,
                              Pair(Boolean('#f'), Nil()))))


def expand_mit_define(sexpr):
    sexpr.cdr = AbstractSchemeExpr.expand(sexpr.cdr)
    name = sexpr.cdr.car.car
    args = sexpr.cdr.car.cdr
    body = sexpr.cdr.cdr.car
    sexpr.cdr.car = name
    sexpr.cdr.cdr = Pair(Pair(Symbol('LAMBDA'),
                              Pair(args,
                                   Pair(body,
                                        Nil()))),
                         Nil())
    return sexpr


def expand_quasiquote(sexpr):
    if is_unquote(sexpr):
        return AbstractSchemeExpr.expand(sexpr.cdr.car)
    elif is_unquote_splicing(sexpr):
        raise InvalidSyntax('unquote-splicing here makes no sense!')
    elif is_pair(sexpr):
        a = AbstractSchemeExpr.expand(sexpr.car)
        b = AbstractSchemeExpr.expand(sexpr.cdr)
        if is_unquote_splicing(a):
            return Pair(Symbol('append'),
                        Pair(a.cdr.car,
                             Pair(expand_quasiquote(b),
                                  Nil())))
        elif is_unquote_splicing(b):
            return Pair(Symbol('cons'),
                        Pair(expand_quasiquote(a),
                             Pair(b.cdr.car,
                                  Nil())))
        else:
            return Pair(Symbol('cons'),
                        Pair(expand_quasiquote(a),
                             Pair(expand_quasiquote(b),
                                  Nil())))
    elif is_vector(sexpr):
        return Pair(Symbol('list->vector'),
                    Pair(expand_quasiquote(list_to_pair(sexpr.get_value())),
                         Nil()))
    elif is_nil(sexpr) or is_symbol(sexpr):
        return Pair(Symbol('quote'),
                    Pair(AbstractSchemeExpr.expand(sexpr),
                         Nil()))
    else:
        return AbstractSchemeExpr.expand(sexpr)


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
        l = pair_to_list(AbstractSchemeExpr.process(sexpr.cdr.car))
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
        return IfThenElse(predicate, then_body, Void())
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
        sexpr, remaining = AbstractSexpr.readFromString(input_string)
        #print(sexpr)
        expanded = AbstractSchemeExpr.expand(sexpr)
        scheme_expr = AbstractSchemeExpr.process(expanded)
        return scheme_expr, remaining

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
        elif is_quote(sexpr):
            return Pair(sexpr.car, sexpr.cdr)
        elif is_quasiquoted(sexpr):
            return expand_quasiquote(sexpr.cdr.car)
        elif is_proper_list(sexpr):
            return Pair(AbstractSchemeExpr.expand(sexpr.car), AbstractSchemeExpr.expand(sexpr.cdr))
        else:
            return sexpr

    @staticmethod  # where the actual parsing occur
    def process(sexpr):
        # basic
        if is_const(sexpr):
            return Constant(sexpr)
        elif is_vector(sexpr):
            return Constant(Vector(list(map(AbstractSchemeExpr.process, sexpr.get_value()))))
        elif is_improper_list(sexpr):
            return list_to_pair(list(map(AbstractSchemeExpr.process, pair_to_list(sexpr))))
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

    def debruijn(self, bounded=list(), params=list()):
        return self

    def annotateTC(self, is_tp=false):
        return self

    def semantic_analysis(self):
        return self.debruijn().annotateTC()

    def code_gen(self):
        pass

### Constant ###
class Constant(AbstractSchemeExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if not is_const(self.value) and not is_vector(self.value) and not is_pair(self.value):
            return "'" + str(self.value)
        else:
            return str(self.value)

    def debruijn(self, bounded=list(), params=list()):
        return Constant(self.value)
        #return Constant(self.value.debruijn(bounded, params))


### Variable ###
class Variable(AbstractSchemeExpr):
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol.get_value()

    def __eq__(self, other):
        return isinstance(other, Variable) and \
               self.symbol.get_value() == other.symbol.get_value()

    def __ne__(self, other):
        return not self == other

    def debruijn(self, bounded=list(), params=list()):
        if self in params:
            return VarParam(self.symbol, params.index(self))
        else:
            search = [(x[0], x[1].index(self)) for x in enumerate(bounded) if self in x[1]]
            if search:
                return VarBound(self.symbol, search[0][0], search[0][1])
            else:
                return VarFree(self.symbol)


class VarFree(Variable):
    def __init__(self, symbol):
        super(VarFree, self).__init__(symbol)

    def __str__(self):
        return self.symbol.get_value()


class VarParam(Variable):
    def __init__(self, symbol, minor):
        super(VarParam, self).__init__(symbol)
        self.minor = minor

    def __str__(self):
        return self.symbol.get_value()
        # + '(' + str(self.minor) + ')'

    def code_gen(self):
        return "MOV(R0, STACK(FP-5-" + str(self.minor) + "));\n"


class VarBound(Variable):
    def __init__(self, symbol, major, minor):
        super(VarBound, self).__init__(symbol)
        self.major = major
        self.minor = minor

    def __str__(self):
        return self.symbol.get_value()
        # + '(' + str(self.major) + ', ' + str(self.minor) + ')'


### Core Forms ###

class IfThenElse(AbstractSchemeExpr):
    def __init__(self, predicate, then_body, else_body):
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body

    def __str__(self):
        res = '(if ' + str(self.predicate) + ' ' + str(self.then_body)
        if not is_void(self.else_body):
            res += ' ' + str(self.else_body)
        res += ')'
        return res

    def debruijn(self, bounded=list(), params=list()):
        return IfThenElse(self.predicate.debruijn(bounded, params),
                          self.then_body.debruijn(bounded, params),
                          self.else_body.debruijn(bounded, params))

    def annotateTC(self, is_tp=false):
        return IfThenElse(self.predicate.annotateTC(False),
                          self.then_body.annotateTC(is_tp),
                          self.else_body.annotateTC(is_tp))

    def code_gen(self):
        false_label = gen_label()
        exit_label = gen_label()
        code = self.predicate.code_gen() + '\n'
        code += '  CMP(R0, IMM(0));\n'
        code += '  JUMP_EQ(' + false_label + ');\n'
        code += self.then_body.code_gen()
        code += '  JUMP(' + exit_label + ');\n'
        code += ' ' + false_label + ":\n"
        code += self.else_body.code_gen()
        code += ' ' + exit_label + ":\n"
        return code


class Applic(AbstractSchemeExpr):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        return '(' + ' '.join([str(self.func)] + [str(x) for x in self.args]) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return Applic(self.func.debruijn(bounded, params),
                      [x.debruijn(bounded, params) for x in self.args])

    def annotateTC(self, is_tp=false):
        if is_tp:
            return ApplicTP(self.func.annotateTC(False),
                            [x.annotateTC(False) for x in self.args])
        else:
            return Applic(self.func.annotateTC(False),
                          [x.annotateTC(False) for x in self.args])


class ApplicTP(Applic):
    def __init__(self, func, args):
        super(ApplicTP, self).__init__(func, args)

    def __str__(self):
        return super(ApplicTP, self).__str__()
        # + 'TP'


class Or(AbstractSchemeExpr):
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return '(' + ' '.join(['or'] + [str(x) for x in self.elements]) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return Or([x.debruijn(bounded, params) for x in self.elements])

    def annotateTC(self, is_tp=false):
        return Or([x.annotateTC(False) for x in self.elements[:-1]] \
                  + [self.elements[-1].annotateTC(is_tp)])


class Def(AbstractSchemeExpr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return '(define ' + str(self.name) + ' ' + str(self.value) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return Def(self.name.debruijn(bounded, params),
                   self.value.debruijn(bounded, params))

    def annotateTC(self, is_tp=false):
        return Def(self.name, self.value.annotateTC(False))

        ### Lambda Forms ###


class AbstractLambda(AbstractSchemeExpr):
    pass


class LambdaSimple(AbstractLambda):
    def __init__(self, variables, body):
        self.variables = variables
        self.body = body

    def __str__(self):
        return '(lambda (' + ' '.join([str(x) for x in self.variables]) + ') ' + str(self.body) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return LambdaSimple(self.variables,
                            self.body.debruijn([params] + bounded, self.variables))

    def annotateTC(self, is_tp=false):
        return LambdaSimple(self.variables, self.body.annotateTC(True))


class LambdaVar(AbstractLambda):
    def __init__(self, var_list, body):
        self.var_list = var_list
        self.body = body

    def __str__(self):
        return '(lambda ' + str(self.var_list) + ' ' + str(self.body) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return LambdaVar(self.var_list,
                         self.body.debruijn([params] + bounded, [self.var_list]))

    def annotateTC(self, is_tp=false):
        return LambdaVar(self.var_list, self.body.annotateTC(True))


class LambdaOpt(AbstractLambda):
    def __init__(self, variables, var_list, body):
        self.variables = variables
        self.var_list = var_list
        self.body = body

    def __str__(self):
        return '(lambda (' + ' '.join([str(x) for x in self.variables]) + \
               ' . ' + str(self.var_list) + ') ' + str(self.body) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return LambdaOpt(self.variables, self.var_list,
                         self.body.debruijn([params] + bounded,
                                            self.variables + [self.var_list]))

    def annotateTC(self, is_tp=false):
        return LambdaOpt(self.variables, self.var_list, self.body.annotateTC(True))
