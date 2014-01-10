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

 CONTINUE:
"""


def generate_footer():
    return """
  STOP_MACHINE;

  return 0;
}
"""


def compile_scheme_file(src, dest):
    name = '.'.join(dest.split('.')[:-1])

    s = open(src, 'r')
    d = open(dest, 'w')
    text = s.read().strip()
    # code = []

    d.write(generate_header())
    while text:
        sexpr, text = AbstractSchemeExpr.parse(text)
        print(str(sexpr))
        d.write(str(sexpr.semantic_analysis()) + '\n')

        #code.append(sexpr.semantic_analysis())

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
