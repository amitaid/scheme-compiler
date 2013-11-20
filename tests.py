__author__ = 'amitaid'

from sexprs import *


def parse(input):
    print(input + ' => ' + str(AbstractSexpr.readFromString(input)[0]))


def main():
    #print(AbstractSexpr.readFromString(
    #    r'(-0H432 +0123/0x52 ab53$$ "bla bla \n \l bla" #\pAge #\tAb #\xFDFA #\M () #(1 2 3 #(1 2 3)) 72 . 5)')[0])

    #print(AbstractSexpr.readFromString('′(#\\x03bb x y z)')[0])
    #print(AbstractSexpr.readFromString('`#\\lambda')[0])
    #print(AbstractSexpr.readFromString(',@#\\lambda')[0])
    #print(AbstractSexpr.readFromString(',#\\lambda')[0])

    #print(AbstractSexpr.readFromString('#\pAge')[0])

    #print(proper_list.match('(a v)')[0])
    #
    #print(fraction.match('5/0xa')[0])
    #
    #print(AbstractSexpr.readFromString('#t')[0])
    #
    #print(AbstractSexpr.readFromString('"123\lcdd""')[0])
    #
    #print(AbstractSexpr.readFromString('#\\lambda')[0])
    #print(AbstractSexpr.readFromString('#\\x30')[0])
    #print(AbstractSexpr.readFromString('#\\☺')[0])
    #
    parse('5 #((1 . 1 . 2))) (3 4)')
    parse(',8/3')
    parse('(1 . ( 1 . 2))')


if __name__ == '__main__':
    main()

