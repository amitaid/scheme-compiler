import tag_parser


def compile_scheme_file(src, dest):
    s = open(src, 'r')
    d = open(dest, 'w')
    text = s.read().strip()
    code = ''

    while text:
        sexpr, text = tag_parser.AbstractSchemeExpr.parse(text)
        code += str(sexpr.semantic_analysis()) + '\n'
    print(code.strip())
    d.write(code.strip())

    s.close()
    d.close()


if __name__ == '__main__':
    compile_scheme_file('src.scm', 'dest.asm')