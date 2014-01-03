from tag_parser import AbstractSchemeExpr


def compile_scheme_file(src, dest):
    s = open(src, 'r')
    d = open(dest, 'w')
    text = s.read().strip()
    code = []

    while text:
        sexpr, text = AbstractSchemeExpr.parse(text)
        code.append(sexpr.semantic_analysis())

    output = '\n'.join(map(str, code))
    print(output)
    d.write(output)

    s.close()
    d.close()


if __name__ == '__main__':
    compile_scheme_file('src.scm', 'dest.asm')
