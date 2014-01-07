from tag_parser import AbstractSchemeExpr
from tag_parser import symbol_list


def compile_scheme_file(src, dest):
    s = open(src, 'r')
    d = open(dest, 'w')
    text = s.read().strip()
    code = []

    while text:
        sexpr, text = AbstractSchemeExpr.parse(text)
        code.append(sexpr.semantic_analysis())

    print(symbol_list)

    output = '\n'.join(map(lambda s: s.code_gen(), code)) + '\n'
    print(output)
    d.write(output)

    s.close()
    d.close()


if __name__ == '__main__':
    compile_scheme_file('test1.scm', 'test1.asm')
