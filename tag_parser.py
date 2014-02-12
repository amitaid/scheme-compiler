from sexprs import *

#key_words = ['DEFINE', 'LAMBDA', 'λ', 'IF', 'AND', 'OR', 'COND']
#primitive_ops = ['+', '-',]

#symbol table

# todo -1 must be replaced with the appropiate code for the primitive procedures
# todo must take care of variables whose name is a keyword
symbol_table = {}

builtin = {'+': 'PLUS', '-': 'MINUS', '*': 'MULT', '/': 'DIVIDE',
           '>': 'GREATER', '<': 'SMALLER', '=': 'EQUAL', 'APPEND': 'APPEND',
           'NULL?': 'IS_NULL', 'NUMBER?': 'IS_NUMBER', 'ZERO?': 'IS_ZERO',
           'PAIR?': 'IS_PAIR', 'PROCEDURE?': 'IS_PROCEDURE', 'BOOLEAN?': 'IS_BOOLEAN',
           'CHAR?': 'IS_CHAR', 'STRING?': 'IS_STRING', 'INTEGER?': 'IS_INTEGER', 'VECTOR?': 'IS_VECTOR',
           'CONS': 'CONS', 'CAR': 'CAR', 'CDR': 'CDR', 'VECTOR': 'VECTOR_CONSTRUCTOR', 'VECTOR-LENGTH': 'VECTOR_LENGTH',
           'VECTOR-REF': 'VECTOR_REF', 'MAKE-VECTOR': 'MAKE_VECTOR', 'STRING': 'STRING_CONSTRUCTOR'}


def sym_tab_cg():
    global mem_ptr, symbol_table
    first_link = True
    code = ''
    for sym in builtin.keys():
        Constant(String(sym))  # Generate constants so all symbols have strings in const table
        symbol_table[sym] = -1

    for sym in symbol_table.keys():
        code += make_symbol_link(sym)
        if first_link:
            code += "  MOV(IND(IMM(7)), R0);\n"  # First link is in 7
            first_link = False
        else:
            code += "  MOV(INDD(R1,1), R0);\n"  # Update previous link's next pointer
        code += "  MOV(R1, R0);\n"

    return code


def make_symbol_link(symbol_string):
    global mem_ptr, symbol_table, constants
    code = "  PUSH(IMM(6));\n"
    code += "  CALL(MALLOC);\n"
    code += "  DROP(1);\n"
    code += "  MOV(IND(R0), " + str(mem_ptr + 4) + ");\n"  # Pointer to bucket
    code += "  MOV(INDD(R0,1), IMM(-1));\n"
    code += "  MOV(INDD(R0,2),T_SYMBOL);\n"
    code += "  MOV(INDD(R0,3), " + str(mem_ptr + 4) + ");\n"  # Pointer to bucket"
    code += "  MOV(INDD(R0,4), IMM(" + str(constants[String(symbol_string)]) + "));\n"
    code += "  MOV(INDD(R0,5), IMM(-1));\n"
    symbol_table[symbol_string] = mem_ptr + 2
    mem_ptr += 6
    return code


def gen_builtin():
    global mem_ptr, symbol_table
    code = ''
    for sym in builtin.keys():
        code += '  PUSH(LABEL(' + builtin[sym] + '));\n'
        code += '  PUSH(IMM(0));\n'
        code += '  CALL(MAKE_SOB_CLOSURE);\n'
        code += '  DROP(2);\n'
        code += '  MOV(R1, INDD(' + str(symbol_table[sym]) + ',1));\n'
        code += '  MOV(INDD(R1,1), IMM(' + str(mem_ptr) + '));\n'
        mem_ptr += 3
    return code


gen_sym_counter = 0


def gen_sym():
    global gen_sym_counter
    new_gen_sym = '@' + str(gen_sym_counter)
    gen_sym_counter += 1
    return Symbol(new_gen_sym)


label_index = 0


def gen_label():
    global label_index
    new_label = str(label_index)
    label_index += 1
    return new_label


class InvalidSyntax(Exception):
    pass


### sexprs predicates ###

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

def is_quote(sexpr):  # TODO implement later
    return is_proper_list(sexpr) and \
           is_symbol(sexpr.car) and \
           sexpr.car.get_value() == 'quote'


def is_const(sexpr):
    return is_boolean(sexpr) or \
           is_char(sexpr) or \
           is_number(sexpr) or \
           is_string(sexpr) or \
           is_nil(sexpr) or \
           is_void(sexpr)  # or \
    #       is_symbol(sexpr)  # or \
    #(is_pair(sexpr) and not is_symbol(sexpr.car))


def is_variable(sexpr):
    return is_symbol(sexpr)


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
    func = AbstractSchemeExpr.process(AbstractSchemeExpr.expand(sexpr.car))
    args = list(map(AbstractSchemeExpr.expand, pair_to_list(sexpr.cdr)))
    args = list(map(AbstractSchemeExpr.process, args))
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
    if not isinstance(var, Variable):
        raise InvalidSyntax('Attempt to use define without a variable')
    expr = AbstractSchemeExpr.process(sexpr.cdr.cdr.car)
    return Def(var, expr)


class AbstractSchemeExpr:
    @staticmethod
    def parse(input_string):
        sexpr, remaining = AbstractSexpr.readFromString(input_string)
        sexpr = AbstractSchemeExpr.expand(sexpr)
        sexpr = AbstractSchemeExpr.process(sexpr)
        return sexpr, remaining

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
            if is_pair(sexpr.cdr.car):
                sexpr.cdr.car = list_to_pair(
                    list(map(AbstractSchemeExpr.expand, pair_to_list(sexpr.cdr.car))) + [Nil()])
                sexpr.cdr.car = list_to_pair(list(
                    map(lambda x: String(x.value) if isinstance(x, Symbol) else x,
                        pair_to_list(sexpr.cdr.car))))
            else:
                sexpr.cdr.car = AbstractSchemeExpr.expand(sexpr.cdr.car)
            return sexpr
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
            return Constant(sexpr.cdr.car)
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
        elif is_applic(sexpr):  # must always come last
            return build_applic(sexpr)
        else:
            print('format not supported: ' + str(sexpr))
            return Constant(Void())  # TODO in my opinion we should raise an exception here

    def debruijn(self, bounded=list(), params=list()):
        return self

    def annotateTC(self, is_tp=False):
        return self

    def semantic_analysis(self):
        res = self.debruijn().annotateTC()
        res.analyze_env()
        return res

    def analyze_env(self, env_count=0, arg_count=0):
        pass

    def code_gen(self):
        pass


### Constant ###
constants = {sexprs.Void(): 1,
             sexprs.Nil(): 2,
             sexprs.Boolean('#f'): 3,
             sexprs.Boolean('#t'): 5,
             'const_code': []}
mem_ptr = 8


class Constant(AbstractSchemeExpr):
    def __init__(self, value):
        self.value = value
        add_const(self.value)


    def __str__(self):
        if not is_const(self.value) and not is_vector(self.value) and not is_pair(self.value):
            return "'" + str(self.value)
        else:
            return str(self.value)

    def debruijn(self, bounded=list(), params=list()):
        return Constant(self.value)
        #return Constant(self.value.debruijn(bounded, params))

    def code_gen(self):
        return '  MOV(R0, ' + str(constants[self.value]) + ');\n'


def cg_integer(const):
    code = '  /* Const ' + str(const) + ' */\n'
    code += '  PUSH(IMM(' + str(const.value) + '));\n'
    code += '  CALL(MAKE_SOB_INTEGER);\n'
    code += '  DROP(1);\n\n'
    return code


def cg_fraction(const):
    code = '  /* Const ' + str(const) + ' */\n'
    code += Constant(const.denum).code_gen()
    code += '  PUSH(R0);\n'
    code += Constant(const.numer).code_gen()
    code += '  PUSH(R0);\n'
    code += '  CALL(MAKE_SOB_FRACTION);\n'
    code += '  DROP(2);\n\n'
    return code


def cg_char(const):
    code = '  /* Const ' + str(const) + ' */\n'
    code += '  PUSH(IMM(' + str(ord(const.value)) + '));\n'
    code += '  CALL(MAKE_SOB_CHAR);\n'
    code += '  DROP(1);\n\n'
    return code


def cg_pair(const):
    code = '  /* Const ' + str(const) + ' */\n'
    if is_const(const.car):
        car = Constant(const.car)
    else:
        car = const.car
    if is_const(const.cdr) or is_pair(const.cdr):
        cdr = Constant(const.cdr)
    else:
        cdr = const.cdr
    code += cdr.code_gen()
    code += '  PUSH(R0);\n'
    code += car.code_gen()
    code += '  PUSH(R0);\n'
    code += '  CALL(MAKE_SOB_PAIR);\n'
    code += '  DROP(2);\n\n'
    return code


def cg_string(const):
    code = '  /* Const ' + str(const) + ' */\n'
    for ch in const.value:
        code += '  PUSH(IMM(' + str(ord(ch)) + '));\n'
    code += '  PUSH(IMM(' + str(len(const.value)) + '));\n'
    code += '  CALL(MAKE_SOB_STRING);\n'
    code += '  DROP(' + str(len(const.value) + 1) + ');\n\n'
    return code


def cg_vector(const):
    code = '  /* Const ' + str(const) + ' */\n'
    for item in const.value:
        code += item.code_gen()
        code += '  PUSH(R0);\n'
    code += '  PUSH(IMM(' + str(len(const.value)) + '));\n'
    code += '  CALL(MAKE_SOB_VECTOR);\n'
    code += '  DROP(' + str(len(const.value) + 1) + ');\n\n'
    return code


def cg_symbol(const):
    pass  # TODO


def update_consts(const, code, mem_size):
    global constants, mem_ptr
    constants['const_code'].append(code)
    constants[const] = mem_ptr
    mem_ptr += mem_size


def add_const(const):
    if const not in constants:
        if is_integer(const):
            update_consts(const, cg_integer(const), 2)
        elif is_fraction(const):
            update_consts(const, cg_fraction(const), 3)
        elif is_pair(const):
            update_consts(const, cg_pair(const), 3)
        elif is_string(const):
            update_consts(const, cg_string(const), 2 + len(const.value))
        elif is_vector(const):
            update_consts(const, cg_vector(const), 2 + len(const.value))
        elif is_char(const):
            update_consts(const, cg_char(const), 2)
            #elif is_symbol(const):
            #    update_consts(const, cg_symbol(const), 2)


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
        Constant(String(self.symbol.value))
        if self.symbol.value not in symbol_table:
            symbol_table[self.symbol.value] = -1

    def __str__(self):
        return self.symbol.get_value()

    def code_gen(self):
        code = '  MOV(R0, INDD(' + str(symbol_table[self.symbol.value]) + ', 1));\n'
        code += '  MOV(R0, INDD(R0, 1));\n'
        return code


class VarParam(Variable):
    def __init__(self, symbol, minor):
        super(VarParam, self).__init__(symbol)
        self.minor = minor

    def __str__(self):
        return self.symbol.get_value()
        # + '(' + str(self.minor) + ')'

    def code_gen(self):
        return '  MOV(R0, FPARG(' + str(self.minor + 2) + '));\n'


class VarBound(Variable):
    def __init__(self, symbol, major, minor):
        super(VarBound, self).__init__(symbol)
        self.major = major
        self.minor = minor

    def __str__(self):
        return self.symbol.get_value()
        # + '(' + str(self.major) + ', ' + str(self.minor) + ')'

    def code_gen(self):
        code = '  MOV(R0, FPARG(0));\n'
        code += '  MOV(R0, INDD(R0, ' + str(self.major) + '));\n'
        code += '  MOV(R0, INDD(R0, ' + str(self.minor) + '));\n'
        return code


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

    def annotateTC(self, is_tp=False):
        return IfThenElse(self.predicate.annotateTC(False),
                          self.then_body.annotateTC(is_tp),
                          self.else_body.annotateTC(is_tp))

    def analyze_env(self, env_count=0, arg_count=0):
        self.predicate.analyze_env(env_count, arg_count)
        self.then_body.analyze_env(env_count, arg_count)
        self.else_body.analyze_env(env_count, arg_count)

    def code_gen(self):
        label = gen_label()
        true_label = 'L_THEN_' + label
        false_label = 'L_ELSE_' + label
        exit_label = 'L_IF_EXIT_' + label
        code = self.predicate.code_gen() + '\n'
        code += '  CMP(IND(R0), T_BOOL);\n'  # If predicate isn't T_BOOL, it's true
        code += '  JUMP_NE(' + true_label + ');\n'
        code += '  CMP(INDD(R0,1), INDD(3,1));\n'  # If predicate is T_BOOL, compare values
        code += '  JUMP_EQ(' + false_label + ');\n'
        code += ' ' + true_label + ":\n"
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

    def annotateTC(self, is_tp=False):
        if is_tp:
            return ApplicTP(self.func.annotateTC(False),
                            [x.annotateTC(False) for x in self.args])
        else:
            return Applic(self.func.annotateTC(False),
                          [x.annotateTC(False) for x in self.args])

    def analyze_env(self, env_count=0, arg_count=0):
        self.func.analyze_env(env_count, arg_count),
        for x in self.args:
            x.analyze_env(env_count, arg_count)

    def code_gen(self):
        label = gen_label()
        code = ''

        for arg in reversed(self.args):
            code += arg.code_gen()
            code += '  PUSH(R0);\n'
        code += '  PUSH(IMM(' + str(len(self.args)) + '));\n'
        code += self.func.code_gen()
        code += '  MOV(R1,R0);\n'
        code += '  PUSH(R0);\n'
        code += '  CALL(IS_SOB_CLOSURE);\n'
        code += '  DROP(1);\n'
        code += '  CMP(R0,IMM(1));\n'
        code += '  JUMP_EQ(L_APPLIC_EXIT_' + label + ');\n'

        #TODO ERROR

        code += ' L_APPLIC_EXIT_' + label + ':\n'
        code += '  MOV(R0,R1);\n'
        code += '  PUSH(INDD(R0,1));\n'
        code += '  CALLA(INDD(R0,2));\n'
        code += '  DROP(1);\n'
        code += '  POP(R1);\n'
        code += '  DROP(R1);\n'
        return code


class ApplicTP(Applic):
    def __init__(self, func, args):
        super(ApplicTP, self).__init__(func, args)

    def __str__(self):
        return super(ApplicTP, self).__str__()  # + 'TP'

    def analyze_env(self, env_count=0, arg_count=0):
        self.func.analyze_env(env_count, arg_count),
        for x in self.args:
            x.analyze_env(env_count, arg_count)

    def code_gen(self):
        label = gen_label()
        applic_tc_prep_label = 'L_APPLIC_TP_PREP_' + label
        applic_tc_loop_label = 'L_APPLIC_TP_LOOP_' + label
        applic_tc_exit_label = 'L_APPLIC_TP_EXIT_' + label

        code = ''

        for arg in reversed(self.args):
            code += arg.code_gen()
            code += '  PUSH(R0);\n'
        code += '  PUSH(IMM(' + str(len(self.args)) + '));\n'
        code += self.func.code_gen()

        code += '  MOV(R1,R0);\n'
        code += '  PUSH(R0);\n'
        code += '  CALL(IS_SOB_CLOSURE);\n'
        code += '  DROP(1);\n'
        code += '  CMP(R0,IMM(1));'
        code += '  JUMP_EQ(' + applic_tc_prep_label + ');\n'

        #TODO ERROR

        code += ' ' + applic_tc_prep_label + ':\n'
        code += '  MOV(R0,R1);\n'
        code += '  PUSH(INDD(R0, 1));\n'  # here the diffenece from applic starts
        code += '  PUSH(FPARG(-1));\n'  # Olf Return addr
        code += '  MOV(R1,FPARG(-2));\n'  # Old FP
        code += '  MOV(R5,FPARG(1));\n'  # Store n in R5
        code += '  MOV(R2, IMM(' + str(len(self.args) + 3) + '));\n'  # Store m in R2
        code += '  MOV(R3,FP);\n'  # Upper pointer
        code += '  MOV(FP,R1);\n'  # FP moves to the old FP
        code += '  MOV(R4,FP);\n'  # Lower pointer

        code += ' ' + applic_tc_loop_label + ':\n'
        code += '  CMP(R2, IMM(0));\n'
        code += '  JUMP_EQ(' + applic_tc_exit_label + ');\n'
        code += '  MOV(STACK(R4),STACK(R3));'
        code += '  INCR(R3);\n'
        code += '  INCR(R4);\n'
        code += '  DECR(R2);\n'
        code += '  JUMP(' + applic_tc_loop_label + ');\n'

        code += ' ' + applic_tc_exit_label + ':\n'
        code += '  SUB(SP, R5);\n'
        code += '  SUB(SP, 4);\n'
        code += '  JUMPA(INDD(R0,2));\n'

        return code


class Or(AbstractSchemeExpr):
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return '(' + ' '.join(['or'] + [str(x) for x in self.elements]) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return Or([x.debruijn(bounded, params) for x in self.elements])

    def annotateTC(self, is_tp=False):
        return Or([x.annotateTC(False) for x in self.elements[:-1]] \
                  + [self.elements[-1].annotateTC(is_tp)])

    def analyze_env(self, env_count=0, arg_count=0):
        for x in self.elements:
            x.analyze_env(env_count, arg_count)

    def code_gen(self):
        label = gen_label()
        exit_label = 'L_OR_EXIT_' + label
        code = ''
        for element in self.elements[:-1]:
            code += element.code_gen()
            code += '  CMP(IND(R0), IND(3));\n'
            code += '  JUMP_NE(' + exit_label + ');\n'
        code += self.elements[-1].code_gen()
        code += ' ' + exit_label + ':\n'
        return code


class Def(AbstractSchemeExpr):
    def __init__(self, var, value):
        self.var = var
        self.value = value

    def __str__(self):
        return '(define ' + str(self.var) + ' ' + str(self.value) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return Def(self.var.debruijn(bounded, params),
                   self.value.debruijn(bounded, params))

    def annotateTC(self, is_tp=False):
        return Def(self.var,
                   self.value.annotateTC(False))

    def analyze_env(self, env_count=0, arg_count=0):
        self.value.analyze_env(env_count, arg_count)

    def code_gen(self):
        code = self.value.code_gen()
        code += "  MOV(R1, INDD(" + str(symbol_table[self.var.symbol.value]) + ",1));\n"
        code += "  MOV(INDD(R1,1), R0);\n"
        code += "  MOV(R0, IMM(1));\n"
        return code


        ### Lambda Forms ###


class AbstractLambda(AbstractSchemeExpr):
    pass


class LambdaSimple(AbstractLambda):
    def __init__(self, variables, body):
        self.variables = variables
        self.body = body
        self.env_depth = 0
        self.parent_args = 0

    def __str__(self):
        return '(lambda (' + ' '.join([str(x) for x in self.variables]) + ') ' + \
               str(self.body) + ')'  #{' + str(self.env_depth) + '}'

    def debruijn(self, bounded=list(), params=list()):
        return LambdaSimple(self.variables,
                            self.body.debruijn([params] + bounded, self.variables))

    def annotateTC(self, is_tp=False):
        return LambdaSimple(self.variables,
                            self.body.annotateTC(True))

    def analyze_env(self, env_count=0, arg_count=0):
        self.env_depth = env_count
        self.parent_args = arg_count
        self.body.analyze_env(env_count + 1, len(self.variables))

    def code_gen(self):
        label = gen_label()
        env_copy_label = 'L_ENV_LOOP_' + label
        current_args_copy_label = 'L_ARGS_LOOP_' + label
        build_closure_label = 'L_BUILD_CLOS_' + label
        closure_code_label = 'L_CLOS_CODE_' + label
        closure_exit_label = 'L_CLOS_EXIT_' + label

        # setting registers for 1st loop
        code = '  PUSH(IMM(' + str(self.env_depth + 1) + '));\n'
        code += '  CALL(MALLOC);\n'
        code += '  DROP(1);\n'
        code += '  MOV(R1, R0);\n'  # New env

        if self.env_depth > 0:
            code += '  MOV(R2, FPARG(0));\n'  # Old env
            code += '  MOV(R3, IMM(1));\n'  # j
            code += '  MOV(R4, IMM(0));\n'

            # first loop - the environments copy
            code += ' ' + env_copy_label + ':\n'
            code += '  MOV(R0, INDD(R2,R4));\n'
            code += '  MOV(INDD(R1,R3),R0);\n'  # maybe this needs to be split to 2 commands
            code += '  INCR(R3);\n'
            code += '  INCR(R4);\n'
            code += '  CMP(R4, IMM(' + str(self.env_depth) + '));\n'
            code += '  JUMP_LT(' + env_copy_label + ');\n'

            # setting registers for 2nd loop, now R1 holds the new env
            code += '  PUSH(FPARG(1));\n'  # Number of arguments
            code += '  CALL(MALLOC);\n'
            code += '  DROP(1);\n'
            code += '  MOV(IND(R1),R0);\n'
            code += '  MOV(R2,R0);\n'
            code += '  MOV(R3,IMM(0));\n'  # i
            code += '  MOV(R4,IMM(2));\n'  # j

            # 2nd loop - current (param) stack args (vars) copy
            code += ' ' + current_args_copy_label + ':\n'
            code += '  CMP(R3,FPARG(1));\n'
            code += '  JUMP_GE(' + build_closure_label + ');\n'
            code += '  MOV(INDD(R2,R3),FPARG(R4));\n'
            code += '  INCR(R3);\n'
            code += '  INCR(R4);\n'
            code += '  JUMP(' + current_args_copy_label + ');\n'

        else:
            code += '  MOV(R2, IMM(0));\n'
            #    code += '  PUSH(IMM(0));\n'

        code += ' ' + build_closure_label + ':\n'
        # building the actual closure
        code += '  PUSH(LABEL(' + closure_code_label + '));\n'
        code += '  MOV(IND(R1), R2);\n'
        code += '  PUSH(R1);\n'
        code += '  CALL(MAKE_SOB_CLOSURE);\n'
        code += '  DROP(2);\n'
        code += '  JUMP(' + closure_exit_label + ');\n'

        code += ' ' + closure_code_label + ':\n'
        code += '  PUSH(FP);\n'
        code += '  MOV(FP,SP);\n'
        #TODO WHATEVER THAT IS WRITTEN IN THE CLASS NOTES, CHECK VALIDITY OF ARGS ANS STUFF
        code += self.body.code_gen()
        code += '  POP(FP);\n'
        code += '  RETURN;\n'

        code += ' ' + closure_exit_label + ':\n'

        return code


class LambdaVar(AbstractLambda):
    def __init__(self, var_list, body):
        self.var_list = var_list
        self.body = body
        self.env_depth = 0
        self.parent_args = 0

    def __str__(self):
        return '(lambda ' + str(self.var_list) + ' ' + str(self.body) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return LambdaVar(self.var_list,
                         self.body.debruijn([params] + bounded, [self.var_list]))

    def annotateTC(self, is_tp=False):
        return LambdaVar(self.var_list, self.body.annotateTC(True))

    def analyze_env(self, env_count=0, arg_count=0):
        self.env_depth = env_count
        self.parent_args = arg_count
        self.body.analyze_env(env_count + 1, 1)

    def code_gen(self):
        label = gen_label()
        env_copy_label = 'L_VAR_ENV_LOOP_' + label
        current_args_copy_label = 'L_VAR_ARGS_LOOP_' + label
        build_closure_label = 'L_VAR_BUILD_CLOS_' + label
        closure_code_label = 'L_VAR_CLOS_CODE_' + label
        closure_stack_loop_label = 'L_VAR_STACK_LOOP_' + label
        closure_stack_loop_exit_label = 'L_VAR_STACK_EXIT_LOOP_' + label
        closure_exit_label = 'L_VAR_CLOS_EXIT_' + label

        # setting registers for 1st loop
        code = '  PUSH(IMM(' + str(self.env_depth + 1) + '));\n'
        code += '  CALL(MALLOC);\n'
        code += '  DROP(1);\n'
        code += '  MOV(R1, R0);\n'  # New env

        if self.env_depth > 0:
            code += '  MOV(R2, FPARG(0));\n'  # Old env
            code += '  MOV(R3, IMM(1));\n'  # j
            code += '  MOV(R4, IMM(0));\n'

            # first loop - the environments copy
            code += ' ' + env_copy_label + ':\n'
            code += '  MOV(R0, INDD(R2,R4));\n'
            code += '  MOV(INDD(R1,R3),R0);\n'  # maybe this needs to be split to 2 commands
            code += '  INCR(R3);\n'
            code += '  INCR(R4);\n'
            code += '  CMP(R4, IMM(' + str(self.env_depth) + '));\n'
            code += '  JUMP_LT(' + env_copy_label + ');\n'

            # setting registers for 2nd loop, now R1 holds the new env
            code += '  PUSH(FPARG(1));\n'  # Number of arguments
            code += '  CALL(MALLOC);\n'
            code += '  DROP(1);\n'
            code += '  MOV(IND(R1),R0);\n'
            code += '  MOV(R2,R0);\n'
            code += '  MOV(R3,IMM(0));\n'  # i
            code += '  MOV(R4,IMM(2));\n'  # j

            # 2nd loop - current (param) stack args (vars) copy
            code += ' ' + current_args_copy_label + ':\n'
            code += '  CMP(R3,FPARG(1));\n'
            code += '  JUMP_GE(' + build_closure_label + ');\n'
            code += '  MOV(INDD(R2,R3),FPARG(R4));\n'
            code += '  INCR(R3);\n'
            code += '  INCR(R4);\n'
            code += '  JUMP(' + current_args_copy_label + ');\n'

        else:
            code += '  MOV(R2, IMM(0));\n'
            #    code += '  PUSH(IMM(0));\n'

        code += ' ' + build_closure_label + ':\n'
        # building the actual closure
        code += '  PUSH(LABEL(' + closure_code_label + '));\n'
        code += '  MOV(IND(R1), R2);\n'
        code += '  PUSH(R1);\n'
        code += '  CALL(MAKE_SOB_CLOSURE);\n'
        code += '  DROP(2);\n'
        code += '  JUMP(' + closure_exit_label + ');\n'

        code += ' ' + closure_code_label + ':\n'
        code += '  PUSH(FP);\n'
        code += '  MOV(FP,SP);\n'

        code += '  MOV(R0, IMM(2));\n'  # Move nil to R0
        code += '  MOV(R1, FPARG(1));\n'  # Number of arguments
        code += '  ADD(R1, IMM(1));\n'  # Position of last argument

        code += ' ' + closure_stack_loop_label + ':\n'
        code += '  CMP(R1,IMM(1));\n'  # End condition
        code += '  JUMP_EQ(' + closure_stack_loop_exit_label + ');\n'

        code += '  PUSH(R0);\n'
        code += '  PUSH(FPARG(R1));\n'  # Push the next item
        code += '  CALL(MAKE_SOB_PAIR);\n'
        code += '  DROP(2);\n'

        code += '  DECR(R1);\n'
        code += '  JUMP(' + closure_stack_loop_label + ');\n'

        code += ' ' + closure_stack_loop_exit_label + ':\n'
        code += '  POP(FP);\n'
        code += '  MOV(R1, FP);\n'
        code += '  MOV(R2, STARG(0));\n'  # Env
        code += '  MOV(R3, STARG(-1));\n'  # Ret addr
        code += '  MOV(STACK(R1), R0);\n'  # New arg list
        code += '  INCR(R1);\n'
        code += '  MOV(STACK(R1), IMM(1));\n'  # Number of args
        code += '  INCR(R1);\n'
        code += '  MOV(STACK(R1), R2);\n'
        code += '  INCR(R1);\n'
        code += '  MOV(STACK(R1), R3);\n'
        code += '  INCR(R1);\n'
        code += '  MOV(SP, R1);\n'

        code += '  PUSH(FP);\n'
        code += '  MOV(FP,SP);\n'
        #TODO WHATEVER THAT IS WRITTEN IN THE CLASS NOTES, CHECK VALIDITY OF ARGS ANS STUFF
        code += self.body.code_gen()
        code += '  POP(FP);\n'
        code += '  RETURN;\n'

        code += ' ' + closure_exit_label + ':\n'

        return code


class LambdaOpt(AbstractLambda):
    def __init__(self, variables, var_list, body):
        self.variables = variables
        self.var_list = var_list
        self.body = body
        self.env_depth = 0
        self.parent_args = 0

    def __str__(self):
        return '(lambda (' + ' '.join([str(x) for x in self.variables]) + \
               ' . ' + str(self.var_list) + ') ' + str(self.body) + ')'

    def debruijn(self, bounded=list(), params=list()):
        return LambdaOpt(self.variables, self.var_list,
                         self.body.debruijn([params] + bounded,
                                            self.variables + [self.var_list]))

    def annotateTC(self, is_tp=False):
        return LambdaOpt(self.variables, self.var_list, self.body.annotateTC(True))

    def analyze_env(self, env_count=0, arg_count=0):
        self.env_depth = env_count
        self.parent_args = arg_count
        self.body.analyze_env(env_count + 1, len(self.variables) + 1)

    def code_gen(self):
        label = gen_label()
        env_copy_label = 'L_OPT_ENV_LOOP_' + label
        current_args_copy_label = 'L_OPT_ARGS_LOOP_' + label
        build_closure_label = 'L_OPT_BUILD_CLOS_' + label
        closure_code_label = 'L_OPT_CLOS_CODE_' + label
        closure_stack_loop_label = 'L_OPT_STACK_LOOP_' + label
        closure_stack_loop_exit_label = 'L_OPT_STACK_LOOP_EXIT_' + label
        stack_copy_loop_label = 'L_OPT_STACK_COPY_LOOP_' + label
        stack_copy_loop_exit_label = 'L_OPT_STACK_COPY_LOOP_EXIT_' + label
        closure_exit_label = 'L_OPT_CLOS_EXIT_' + label

        # setting registers for 1st loop
        code = '  PUSH(IMM(' + str(self.env_depth + 1) + '));\n'
        code += '  CALL(MALLOC);\n'
        code += '  DROP(1);\n'
        code += '  MOV(R1, R0);\n'  # New env

        if self.env_depth > 0:
            code += '  MOV(R2, FPARG(0));\n'  # Old env
            code += '  MOV(R3, IMM(1));\n'  # j
            code += '  MOV(R4, IMM(0));\n'

            # first loop - the environments copy
            code += ' ' + env_copy_label + ':\n'
            code += '  MOV(R0, INDD(R2,R4));\n'
            code += '  MOV(INDD(R1,R3),R0);\n'  # maybe this needs to be split to 2 commands
            code += '  INCR(R3);\n'
            code += '  INCR(R4);\n'
            code += '  CMP(R4, IMM(' + str(self.env_depth) + '));\n'
            code += '  JUMP_LT(' + env_copy_label + ');\n'

            # setting registers for 2nd loop, now R1 holds the new env
            code += '  PUSH(FPARG(1));\n'  # Number of arguments
            code += '  CALL(MALLOC);\n'
            code += '  DROP(1);\n'
            code += '  MOV(IND(R1),R0);\n'
            code += '  MOV(R2,R0);\n'
            code += '  MOV(R3,IMM(0));\n'  # i
            code += '  MOV(R4,IMM(2));\n'  # j

            # 2nd loop - current (param) stack args (vars) copy
            code += ' ' + current_args_copy_label + ':\n'
            code += '  CMP(R3,FPARG(1));\n'
            code += '  JUMP_GE(' + build_closure_label + ');\n'
            code += '  MOV(INDD(R2,R3),FPARG(R4));\n'
            code += '  INCR(R3);\n'
            code += '  INCR(R4);\n'
            code += '  JUMP(' + current_args_copy_label + ');\n'

        else:
            code += '  MOV(R2, IMM(0));\n'
            #    code += '  PUSH(IMM(0));\n'

        code += ' ' + build_closure_label + ':\n'
        # building the actual closure
        code += '  PUSH(LABEL(' + closure_code_label + '));\n'
        code += '  MOV(IND(R1), R2);\n'
        code += '  PUSH(R1);\n'
        code += '  CALL(MAKE_SOB_CLOSURE);\n'
        code += '  DROP(2);\n'
        code += '  JUMP(' + closure_exit_label + ');\n'

        code += ' ' + closure_code_label + ':\n'
        code += '  PUSH(FP);\n'
        code += '  MOV(FP,SP);\n'

        code += '  MOV(R0, IMM(2));\n'  # Move nil to R0
        code += '  MOV(R1, FPARG(1));\n'  # Number of arguments
        code += '  INCR(R1);\n'  # Position of last argument
        code += '  MOV(R4, FPARG(1));\n'  # n in R4
        code += '  MOV(R5, IMM(' + str(len(self.variables) + 1) + '));\n'  # m in R5

        code += ' ' + closure_stack_loop_label + ':\n'
        code += '  CMP(R1, R5);\n'  # End condition
        code += '  JUMP_EQ(' + closure_stack_loop_exit_label + ');\n'

        code += '  PUSH(R0);\n'
        code += '  PUSH(FPARG(R1));\n'  # Push the next item
        code += '  CALL(MAKE_SOB_PAIR);\n'
        code += '  DROP(2);\n'

        code += '  DECR(R1);\n'
        code += '  JUMP(' + closure_stack_loop_label + ');\n'

        code += ' ' + closure_stack_loop_exit_label + ':\n'
        code += '  POP(FP);\n'
        code += '  MOV(R1, FP);\n'
        code += '  MOV(R2, STARG(0));\n'  # Env
        code += '  MOV(R3, STARG(-1));\n'  # Ret addr
        code += '  MOV(STACK(R1), R0);\n'  # New arg list
        code += '  INCR(R1);\n'
        code += '  SUB(R4, R5);\n'  # n-m in R4
        code += '  ADD(R4, FP);\n'  # R4 points to the last non-opt argument, FP+n-m
        code += '  INCR(R4);\n'

        code += ' ' + stack_copy_loop_label + ':\n'
        code += '  CMP(R5, IMM(1));\n'
        code += '  JUMP_EQ(' + stack_copy_loop_exit_label + ');\n'
        code += '  MOV(STACK(R1), STACK(R4));\n'
        code += '  INCR(R1);\n'
        code += '  INCR(R4);\n'
        code += '  DECR(R5);\n'
        code += '  JUMP(' + stack_copy_loop_label + ');\n'

        code += ' ' + stack_copy_loop_exit_label + ':\n'
        code += '  MOV(STACK(R1), ' + str(len(self.variables) + 1) + ');\n'  # Number of args
        code += '  INCR(R1);\n'
        code += '  MOV(STACK(R1), R2);\n'
        code += '  INCR(R1);\n'
        code += '  MOV(STACK(R1), R3);\n'
        code += '  INCR(R1);\n'
        code += '  MOV(SP, R1);\n'

        code += '  PUSH(FP);\n'
        code += '  MOV(FP,SP);\n'
        #TODO WHATEVER THAT IS WRITTEN IN THE CLASS NOTES, CHECK VALIDITY OF ARGS ANS STUFF
        code += self.body.code_gen()
        code += '  POP(FP);\n'
        code += '  RETURN;\n'

        code += ' ' + closure_exit_label + ':\n'

        return code
