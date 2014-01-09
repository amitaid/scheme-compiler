from tag_parser import AbstractSchemeExpr


def generate_c_file(name):
    f = open(name + '.c', 'w')

    f.write("""#include <stdio.h>
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
#include \"""" + name + """.asm\"

  STOP_MACHINE;

  return 0;
}
""")
    f.close()


def compile_scheme_file(src, dest):
    name = '.'.join(dest.split('.')[:-1])
    generate_c_file(name)

    s = open(src, 'r')
    d = open(dest, 'w')
    text = s.read().strip()
    # code = []

    while text:
        sexpr, text = AbstractSchemeExpr.parse(text)
        print(str(sexpr))
        d.write(str(sexpr.semantic_analysis()) + '\n')

        #code.append(sexpr.semantic_analysis())

    # print(symbol_list)
    #
    # output = '\n'.join(map(str, code)) + '\n'
    # print(output)
    # d.write(output)

    s.close()
    d.close()


if __name__ == '__main__':
    compile_scheme_file('src.scm', 'src.asm')
