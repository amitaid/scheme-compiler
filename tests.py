__author__ = 'amitaid'

from sexprs import *


def main():
    print(AbstractSexpr.readFromString('′(#\\x03bb x y z)')[0])
    print(AbstractSexpr.readFromString('`#\\lambda')[0])
    print(AbstractSexpr.readFromString(',@#\\lambda')[0])
    print(AbstractSexpr.readFromString(',#\\lambda')[0])

    print(AbstractSexpr.readFromString('+0h34')[0])

    print(AbstractSexpr.readFromString('0X54/0Hf50')[0])
    print(AbstractSexpr.readFromString('-00000000000000034/0x0000000000000000000000000043')[0])

    print(AbstractSexpr.readFromString('abc!!?bcd')[0])

    print(AbstractSexpr.readFromString('#t')[0])

    print(AbstractSexpr.readFromString('"123\lcdd""')[0])

    print(AbstractSexpr.readFromString('#\\lambda')[0])
    print(AbstractSexpr.readFromString('#\\x30')[0])
    print(AbstractSexpr.readFromString('#\\☺')[0])

    print(AbstractSexpr.readFromString('(   )')[0])


if __name__ == '__main__':
    main()

