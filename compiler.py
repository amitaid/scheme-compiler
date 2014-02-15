import sys

import tag_parser

header = """#include <stdio.h>
#include <stdlib.h>

#include "arch/cisc.h"

/* change to 0 for no debug info to be printed: */
#define DO_SHOW 0

/* for debugging only, use SHOW("<some message>, <arg> */
#if DO_SHOW
#define SHOW(msg, x) { printf("%s %s = %ld\\n", (msg), (#x), (x)); }
#else
#define SHOW(msg, x) {}
#endif

int main()
{
  START_MACHINE;

  JUMP(CONTINUE);

#include "arch/scheme.lib"
#include "arch/char.lib"
#include "arch/io.lib"
#include "arch/math.lib"
#include "arch/string.lib"
#include "arch/system.lib"


#define SOB_FALSE 0
#define SOB_TRUE 1


 CONTINUE:
  CALL(MAKE_SOB_VOID);  /* SOB_Void = ADDR(1) */
  CALL(MAKE_SOB_NIL);   /* SOB_Nil = ADDR(2) */
  PUSH(IMM(0));
  CALL(MAKE_SOB_BOOL);  /* SOB_False = ADDR(3) */
  PUSH(IMM(1));
  CALL(MAKE_SOB_BOOL);  /* SOB_True = ADDR(5) */
  DROP(2);

  PUSH(IMM(1));  /* Creates the symbol table, ADDR(7) */
  CALL(MALLOC);
  DROP(1);
  MOV(IND(R0), IMM(-1)); // Symbol list initial value

  /* Initial stack */
  PUSH(IMM(0));
  PUSH(IMM(0));
  PUSH(IMM(0));
  PUSH(IMM(0));
  MOV(FP,SP);

"""


def gen_premade_text():
    return """
(define list (lambda x x))

(define Yag
    (lambda fs
        (let ((ms (map
                   (lambda (fi)
                        (lambda ms
                            (apply fi (map (lambda (mi)
                                (lambda args
                                        (apply (apply mi ms) args))) ms)))) fs)))
        (apply (car ms) ms))))

(define simple-map
    (lambda (func lst)
        (if (null? lst)
            lst
            (cons (func (car lst)) (simple-map func (cdr lst))))))

(define map
    (lambda (func lst . rest)
        (if (null? lst)
            lst
            (cons (apply func (cons (car lst) (simple-map car rest)))
                (apply map (cons func (cons (cdr lst) (simple-map cdr rest))))))))

"""
# (define take-cars
#     (lambda lists
#         (if (null? lists)
#             lists
#             (cons (car (car lists)) (apply take-cars (cdr lists))))))
#
# (define take-cdrs
#     (lambda lists
#         (if (null? lists)
#             lists
#             (cons (cdr (car lists)) (apply take-cdrs (cdr lists))))))
#
# (define map2
#     (lambda (func . lists)
#         (cons (apply func (take-cars lists)) (apply map2 (cons func (take-cdrs lists))))))




write_sob_code = """  PUSH(R0);
  CALL(WRITE_SOB);
  DROP(1);
  CALL(NEWLINE);

"""

footer = """
  STOP_MACHINE;

  return 0;
}
"""


def compile_scheme_file(src, dest):
    s = open(src, 'r')
    d = open(dest, 'w')
    text = s.read().strip()
    premade_text = gen_premade_text()
    premade = []
    expressions = []
    tag_parser.reset_data_structures()

    while premade_text:
        sexpr, premade_text = tag_parser.AbstractSchemeExpr.parse(premade_text)
        premade.append(sexpr.semantic_analysis())

    while text:
        sexpr, text = tag_parser.AbstractSchemeExpr.parse(text)
        expressions.append(sexpr.semantic_analysis())

    sym_table = tag_parser.sym_tab_cg()     # Need to generate symbol tables before writing constants
    builtin = tag_parser.gen_builtin()
    linking_code = tag_parser.link_symbols()

    d.write(header)
    d.write('  // Constant code generation\n')
    d.write(''.join(tag_parser.constants['const_code']))

    d.write('\n  // Symbol code generation\n')
    d.write(sym_table)
    d.write(builtin)
    d.write(linking_code)

    d.write('\n // Premade functions code\n')
    for expr in premade:
        code = expr.code_gen()
        if code:
            d.write(code)

    d.write('\n  // Program code\n')
    for expr in expressions:
        #print(expr)
        code = expr.code_gen()
        if code:
            d.write(code)
        if not tag_parser.is_void(expr) and not isinstance(expr, tag_parser.Def):
            d.write(write_sob_code)
    d.write(footer)

    # print(symbol_list)
    #
    # output = '\n'.join(map(str, code)) + '\n'
    # print(output)
    # d.write(output)

    s.close()
    d.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a compilation target.\n')
    else:
        compile_scheme_file(sys.argv[1], sys.argv[1].split('.')[0] + '.asm')
