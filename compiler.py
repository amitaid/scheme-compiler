from tag_parser import AbstractSchemeExpr


def generate_header():
    return """#include <stdio.h>
#include <stdlib.h>

#include "cisc.h"

/* change to 0 for no debug info to be printed: */
#define DO_SHOW 1

/* for debugging only, use SHOW("<some message>, <arg> */
#if DO_SHOW
#define SHOW(msg, x) { printf("%s %s = %ld\n", (msg), (#x), (x)); }
#else
#define SHOW(msg, x) {}
#endif

int main()
{
  START_MACHINE;

  JUMP(CONTINUE);

#include "char.lib"
#include "io.lib"
#include "math.lib"
#include "string.lib"
#include "system.lib"

  CALL(MAKE_SOB_VOID);  /* SOB_Void = ADDR(1) */
  CALL(MAKE_SOB_NIL);   /* SOB_Nil = ADDR(2) */
  PUSH(IMM(0));
  CALL(MAKE_SOB_BOOL);  /* SOB_False = ADDR(3) */
  DROP(1);
#define SOB_FALSE INDD(3,1)

 CONTINUE:
"""

#TODO: Add basic functions and includes.

def generate_footer():
    return """
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
        sexpr, text = AbstractSchemeExpr.parse(text)
        expressions.append(sexpr.semantic_analysis())

    d.write(generate_header())
    for expr in expressions:
        print(str(expr))
        d.write(str(expr) + '\n')
    d.write(generate_footer())

    # print(symbol_list)
    #
    # output = '\n'.join(map(str, code)) + '\n'
    # print(output)
    # d.write(output)

    s.close()
    d.close()


if __name__ == '__main__':
    compile_scheme_file('src.scm', 'src.asm')
