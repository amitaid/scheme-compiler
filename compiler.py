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

#include "arch/char.lib"
#include "arch/io.lib"
#include "arch/math.lib"
#include "arch/string.lib"
#include "arch/system.lib"
#include "arch/scheme.lib"


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

  PUSH(IMM(2));  /* Creates the symbol table */
  CALL(MALLOC);
  DROP(1);

"""

#TODO: Add basic functions and includes.

write_sob_code = """  PUSH(R0);
  CALL(WRITE_SOB);
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
    expressions = []

    while text:
        sexpr, text = tag_parser.AbstractSchemeExpr.parse(text)
        expressions.append(sexpr.semantic_analysis())

    d.write(header)
    d.write('  /* Constant code generation /*\n')
    d.write(''.join(tag_parser.constants['const_code']))

    d.write('\n  /* Symbol code generation */\n')
    d.write(tag_parser.sym_tab_cg())

    d.write('\n  /* Program code */\n')
    for expr in expressions:
        print(expr)
        code = expr.code_gen()
        if code:
            d.write(code)
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
