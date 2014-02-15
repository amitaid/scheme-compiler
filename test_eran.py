import subprocess
from os import remove
from datetime import *

from compiler import *


def assert_equals(expr, expectedResult):
    if (expectedResult != ""):
        expectedResult += '\n'
    testFile = open("tmpsource.txt", 'w+')
    tmpmakeLog = open("tmpmakeLog.txt", 'w+')
    testFile.write(expr)
    testFile.close()

    compile_scheme_file("tmpsource.txt", "tmptarget.asm")

    pm = subprocess.Popen(['make', 'tmptarget'], stdout=tmpmakeLog)
    pm.wait()

    with open('tmpoutput.txt', 'w+') as tmpoutput_f:
        p = subprocess.Popen('tmptarget', stdout=tmpoutput_f, stderr=tmpoutput_f)
        p.wait()
    tmpoutput_f = open('tmpoutput.txt')
    result = tmpoutput_f.read()
    tmpoutput_f.close()
    tmpmakeLog.close()
    remove("tmpoutput.txt")
    remove("tmpmakeLog.txt")
    remove("tmpsource.txt")
    remove("tmptarget")
    remove("tmptarget.asm")
    if (result == expectedResult):
        print("Success!")  # in result: \n"+result[0:-1])
        return True
    else:
        print("Failure Res: \n" + result[0:-1] + "\nExpected: \n" + expectedResult + "\n")
        return False


def assert_contains(expr, expectedResult):
    testFile = open("tmpsource.txt", 'w+')
    tmpmakeLog = open("tmpmakeLog.txt", 'w+')
    testFile.write(expr)
    testFile.close()

    compile_scheme_file("tmpsource.txt", "tmptarget.asm")

    #subprocess.call(['make'],stdout=tmpmakeLog)
    pm = subprocess.Popen(['make', 'tmptarget'], stdout=tmpmakeLog)  #,stderr=tmpmakeLog
    pm.wait()

    with open('tmpoutput.txt', 'w+') as tmpoutput_f:
        p = subprocess.Popen('tmptarget', stdout=tmpoutput_f, stderr=tmpoutput_f)
        p.wait()
    tmpoutput_f = open('tmpoutput.txt')
    result = tmpoutput_f.read()
    tmpoutput_f.close()
    tmpmakeLog.close()
    remove("tmpoutput.txt")
    remove("tmpmakeLog.txt")
    remove("tmpsource.txt")
    remove("tmptarget")
    remove("tmptarget.asm")
    if (expectedResult in result):
        print("Success!")  # in result: \n"+result[0:-1])
        return True
    else:
        print("Failure Res: \n" + result[0:-1] + "\nExpected: " + expectedResult + "\n")
        return False


def run():
    check = True

    print("\n#integer\n")
    #integer
    check = assert_equals("1", "1") and check
    check = assert_equals("-1", "-1") and check

    print("\n#boolean\n")
    check = assert_equals("#t", "#t") and check
    check = assert_equals("#f", "#f") and check

    print("\n#char\n")
    check = assert_equals("#\\newline", "#\\newline") and check
    check = assert_equals("#\\M", "#\\M") and check

    print("\n#string\n")
    check = assert_equals("\"hello\"", "\"hello\"") and check
    check = assert_equals("\"itay\"", "\"itay\"") and check

    print("\n#nil\n")
    check = assert_equals("()", "()") and check

    print("\n#if\n")
    check = assert_equals("(if #t 1)", "1") and check
    check = assert_equals("(if #f 1)", "") and check
    check = assert_equals("(if #t 1 2)", "1") and check
    check = assert_equals("(if #f 1 2)", "2") and check

    print("\n#nested if\n")
    check = assert_equals("(if (if #f #t #f) 1 2)", "2") and check
    check = assert_equals("(if (if #t #t #f) 1 2)", "1") and check

    print("\n#or\n")
    check = assert_equals("(or)", "#f") and check
    check = assert_equals("(or 1 2 3)", "1") and check
    check = assert_equals("(or #t #t)", "#t") and check
    check = assert_equals("(or #t #t #t #t #t)", "#t") and check
    check = assert_equals("(or #f #f #f #f #f)", "#f") and check
    check = assert_equals("(or #f #f #f #f 1)", "1") and check
    check = assert_equals("(or 1 #t #t #t #t)", "1") and check
    check = assert_equals("(or 1 #f #f #f #f)", "1") and check

    print("\n#nested or\n")
    check = assert_equals("(or #f #f #f #f (or #f #f 1))", "1") and check
    check = assert_equals("(or #f #f (or #f #f 1) #f #t)", "1") and check

    print("\n#and\n")
    check = assert_equals("(and)", "#t") and check
    check = assert_equals("(and 1 2 3)", "3") and check
    check = assert_equals("(and #t #t)", "#t") and check
    check = assert_equals("(and #t #t #t #t #t)", "#t") and check
    check = assert_equals("(and #f #f #f #f #f)", "#f") and check
    check = assert_equals("(and #f #f #f #f 1)", "#f") and check
    check = assert_equals("(and 1 #t #t #t #t)", "#t") and check
    check = assert_equals("(and 1 2 3 4 #f)", "#f") and check
    check = assert_equals("(and 1 2 3 4 #t)", "#t") and check

    print("\n#nested and\n")
    check = assert_equals("(and #t #t #t #t (and #t #t 1))", "1") and check
    check = assert_equals("(and #t #t (and #t #t 1) #t (and #t #t 2))", "2") and check

    print("\n#define\n")
    check = assert_equals("(DEFINE X 1)", "") and check
    check = assert_equals("(define x 4) (define y 5) (define y 6) (define z 9) ", "") and check
    check = assert_equals("(DEFINE X 1)\nX(DEFINE X 2)\nX", "1\n2") and check

    print("\n#multiple scheme exprs\n")
    check = assert_equals("1 \n 2", "1\n2") and check
    check = assert_equals("1 2 3 4 5", "1\n2\n3\n4\n5") and check
    check = assert_equals(
        "'abc\n'efg\n'hij\n(define a 1)(define b 2)(define c 3)(define d 4)(define e 5)(define f 6)(define g 7)\na\nb\nc\nd\ne\nf\ng",
        "ABC\nEFG\nHIJ\n1\n2\n3\n4\n5\n6\n7") and check

    print("\n#freeVar\n")
    check = assert_equals("(define x 1) \n x", "1") and check
    check = assert_equals("(define h 111)\n((lambda (x y z) h) 1 2 3)", "111") and check
    check = assert_equals("1 2 3 4 5 (define x 6) x", "1\n2\n3\n4\n5\n6") and check

    print("\n#param\n")
    check = assert_contains("(LAMBDA (X Y Z) X)", "#<closure") and check
    check = assert_equals("((lambda (x y z) y) 5 2 3)", "2") and check

    print("\n#lambda body\n")
    check = assert_equals("((lambda (x y z) #t) 1 2 3)", "#t") and check
    check = assert_contains("((lambda (x) (lambda (y) y)) 1)", "#<closure") and check

    print("\n#nested Lambda\n")
    check = assert_contains("(define h 3)\n(LAMBDA (X Y Z) (LAMBDA (Q W E) H))", "#<closure") and check

    print("\n#LET*\n")
    check = assert_equals("(let* ((x 1) (y (+ x 1))) (list y x))", "(2 . (1 . ()))")
    check = assert_equals("(let* ((x 1) (y (+ x 1)) (z (* y y)) (t (- z x))) (+ x y z))", "7") and check
    check = assert_equals("(let* ((x 1) (y (+ x 1)) (z (* y y)) (t (- z x))) (* t x x))", "3") and check
    check = assert_equals("(let* ((a 1) (b 1) (c (* a b))) c)", "1") and check

    print("\n#lexical scope  \n")
    check = assert_equals("(((lambda (x) (lambda (y) y)) 1) 2)", "2") and check
    check = assert_equals("(((lambda (x) (lambda (y) x)) 1) 2)", "1") and check

    print("\n#Param , Bound , Free var heavy checks\n")
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) a ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "1999") and check
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) b ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "2999") and check
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) c ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "3999") and check
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) d ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "4999") and check
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) e ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "5999") and check
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) f ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "6999") and check
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) g ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "7999") and check
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) h ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "8999") and check
    check = assert_equals(
        "((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) i ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "9999") and check
    check = assert_equals(
        "(DEFINE j 10999)\n((lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) j ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 )",
        "10999") and check
    check = assert_equals(
        "((lambda () ((lambda (d e f) ((lambda (g) ((lambda (j k l) e ) 10999 11999 12999) ) 7999) ) 4999 5999 6999 )))",
        "5999") and check

    print("\n#Lambda var\n")
    check = assert_contains("(lambda lst 1)", "#<closure") and check
    check = assert_contains("(lambda lst lst)", "#<closure") and check
    check = assert_equals("((lambda lst 1))", "1") and check
    check = assert_equals("((lambda lst lst))", "()") and check
    check = assert_equals("((lambda lst lst) 1)", "(1 . ())") and check
    check = assert_equals("((lambda lst lst) 1 2 3 )", "(1 . (2 . (3 . ())))") and check
    check = assert_equals("((lambda a a))", "()") and check

    print("\n#Lambda Opt\n")
    check = assert_contains("(lambda (a . b) 1)", "#<closure") and check
    check = assert_equals("((lambda (a . b) 111) 222 )", "111") and check
    check = assert_equals("((lambda (a b c . d) a) 111 222 333 )", "111") and check
    check = assert_equals("((lambda (a b c . d) b) 111 222 333 )", "222") and check
    check = assert_equals("((lambda (a b c . d) c) 111 222 333 )", "333") and check
    check = assert_equals("((lambda (a b c . d) d) 111 222 333 )", "()") and check
    check = assert_equals("((lambda (a b c . d) d) 111 222 333 444 555 666 777 888 )",
                          "(444 . (555 . (666 . (777 . (888 . ())))))") and check

    print("\n#Library Functions Check\n")
    print("\n#plus\n")
    # integer
    check = assert_equals("(+)", "0/1") and check
    check = assert_equals("(+ 1)", "1") and check
    check = assert_equals("(+ 123456789)", "123456789") and check
    check = assert_equals("(+ 1 1)", "2") and check
    check = assert_equals("(+ 1 2 3 4 5 6 7 8 9 10)", "55") and check
    check = assert_equals("(+ 10 9 8 7 6 5 4 3 2 1)", "55") and check

    #plus fraction
    check = assert_equals("(+ 1/2 1/3 1/4)", "26/24") and check
    check = assert_equals("(+ 1/2 1/2)", "4/4") and check
    check = assert_equals("(+ 1/2 1/2 1/4)", "20/16") and check
    check = assert_equals("(+ 1/2 1/2 1/4 1/4)", "96/64") and check
    check = assert_equals("(+ 1/3 1/4)", "7/12") and check

    #plus numbers
    check = assert_equals("(+ 0/2 0 1 2)", "6/2") and check
    check = assert_equals("(+ 1/2 0 1/2 2)", "12/4") and check

    print("\n#minus\n")
    check = assert_equals("(- 1)", "-1") and check
    check = assert_equals("(- 2)", "-2") and check
    check = assert_equals("(- 3)", "-3") and check
    check = assert_equals("(- 4)", "-4") and check
    check = assert_equals("(- 5)", "-5") and check
    check = assert_equals("(- 6)", "-6") and check
    check = assert_equals("(- 10)", "-10") and check
    check = assert_equals("(- 11)", "-11") and check
    check = assert_equals("(- 12)", "-12") and check

    check = assert_equals("(- 1234567)", "-1234567") and check
    check = assert_equals("(- 1 1)", "0") and check
    check = assert_equals("(- 1 2 3 4 5 6 7 8 9 10)", "-53") and check
    check = assert_equals("(- 1 10 9 8 7 6 5 4 3 2)", "-53") and check
    check = assert_equals("(- 1 2 4 3 5 8 7 6 9 10)", "-53") and check

    check = assert_equals("(- 1/2 1/2)", "0/4") and check
    check = assert_equals("(- 1 1/2)", "1/2") and check
    check = assert_equals("(- 0 1/2)", "-1/2") and check
    check = assert_equals("(- 2 1 1/2 1/4)", "2/8") and check
    check = assert_equals("(- 2 1 1/2 1/4 1/4)", "0/32") and check
    check = assert_equals("(- 2 1 1/2 1/4 1/4 1/2)", "-32/64") and check

    print("\n#Multiply\n")
    check = assert_equals("(*)", "1/1") and check
    check = assert_equals("(* 1)", "1") and check
    check = assert_equals("(* 123456789)", "123456789") and check
    check = assert_equals("(* 1 0)", "0") and check
    check = assert_equals("(* 1 1)", "1") and check
    check = assert_equals("(* 1 2 3 4)", "24") and check
    check = assert_equals("(* 4 3 2 1)", "24") and check
    check = assert_equals("(* 3 4 1 2)", "24") and check

    check = assert_equals("(* 1/2 0)", "0/2") and check
    check = assert_equals("(* 1/2 1)", "1/2") and check
    check = assert_equals("(* 1/2 2)", "2/2") and check
    check = assert_equals("(* 24 1/2 1/3 1/4 1/1)", "24/24") and check
    check = assert_equals("(* 2 1/2 3 1/3 1/4 4 1/1 1)", "24/24") and check

    print("\n#Divide\n")
    check = assert_equals("(/ 1)", "1") and check
    check = assert_equals("(/ 1/1)", "1") and check

    check = assert_equals("(/ 2)", "1/2") and check
    check = assert_equals("(/ 2/1)", "1/2") and check

    check = assert_equals("(/ 0 1)", "0") and check
    check = assert_equals("(/ 1 1)", "1") and check
    check = assert_equals("(/ 4 2)", "4/2") and check
    check = assert_equals("(/ 24 1 2 3 4)", "24/24") and check
    check = assert_equals("(/ 24 4 3 2 1)", "24/24") and check
    check = assert_equals("(/ 24 3 2 4 1)", "24/24") and check

    check = assert_equals("(/ 1/2 1/4 1/3)", "12/2") and check
    check = assert_equals("(/ 3/3 2/1)", "3/6") and check

    print("\n#fraction\n")
    check = assert_equals("10/1", "10/1") and check
    check = assert_equals("10/2", "10/2") and check
    check = assert_equals("10/3", "10/3") and check
    check = assert_equals("-10/4", "-10/4") and check
    check = assert_equals("-0x234abc/37", "-2312892/37") and check

    print("\n#quote\n")
    check = assert_equals("'(1 2 3)", "(1 . (2 . (3 . ())))") and check
    check = assert_equals("'(define itay 3)", "(DEFINE . (ITAY . (3 . ())))") and check

    print("\n#null?\n")
    check = assert_equals("(null? ())", "#t") and check
    check = assert_equals("(null? 1)", "#f") and check
    check = assert_equals("(null? '())", "#t") and check
    check = assert_equals("(null? (if #t () 1))", "#t") and check
    check = assert_equals("(null? (if #t 1 ()))", "#f") and check

    print("\n#boolean?\n")
    check = assert_equals("(boolean? #f)", "#t") and check
    check = assert_equals("(boolean? #t)", "#t") and check
    check = assert_equals("(boolean? #f)", "#t") and check
    check = assert_equals("(boolean? 1)", "#f") and check
    check = assert_equals("(boolean? 1)", "#f") and check
    check = assert_equals("(boolean? ())", "#f") and check
    check = assert_equals("(boolean? 0)", "#f") and check

    print("\n#pair?\n")
    check = assert_equals("(pair? '(1))", "#t") and check
    check = assert_equals("(pair? '(1 2 3))", "#t") and check
    check = assert_equals("(pair? #t)", "#f") and check
    check = assert_equals("(pair? #f)", "#f") and check
    check = assert_equals("(pair? 1)", "#f") and check

    print("\n#procedure?\n")
    check = assert_equals("(procedure? (lambda x x))", "#t") and check
    check = assert_equals("(procedure? (lambda (x) x))", "#t") and check
    check = assert_equals("(procedure? (lambda (x . y) x))", "#t") and check
    check = assert_equals("(procedure? #t)", "#f") and check
    check = assert_equals("(procedure? #f)", "#f") and check
    check = assert_equals("(procedure? 1)", "#f") and check

    print("\n#vector?\n")
    check = assert_equals("(vector? '#('(1 2 3) '(4 5 6) '(7 8 9)))", "#t") and check
    check = assert_equals("(vector? '#('() '(4 5 6) '()))", "#t") and check
    check = assert_equals("(vector? '(1 2 3))", "#f") and check
    check = assert_equals("(vector? 1)", "#f") and check

    print("\n#char?\n")
    check = assert_equals("(char? #\\newline)", "#t") and check
    check = assert_equals("(char? #\\return)", "#t") and check
    check = assert_equals("(char? #\\tab)", "#t") and check
    check = assert_equals("(char? #\\page)", "#t") and check
    check = assert_equals("(char? #\\lambda)", "#t") and check
    check = assert_equals("(char? #\\x03bb)", "#t") and check
    check = assert_equals("(char? #\\x05D0)", "#t") and check
    check = assert_equals("(char? #\\xFDFA)", "#t") and check

    check = assert_equals("(char? #\\x0041)", "#t") and check  #A
    check = assert_equals("(char? #\\x0042)", "#t") and check  #B

    check = assert_equals("(char? 1)", "#f") and check
    check = assert_equals("(char? 'a)", "#f") and check
    check = assert_equals("(char? \"a\")", "#f") and check

    print("\n#integer?\n")
    check = assert_equals("(integer? 1)", "#t") and check
    check = assert_equals("(integer? 123456789)", "#t") and check
    check = assert_equals("(integer? '1)", "#t") and check
    check = assert_equals("(integer? 1/2)", "#f") and check
    check = assert_equals("(integer? 0/1)", "#f") and check
    check = assert_equals("(integer? 1/1)", "#f") and check
    check = assert_equals("(integer? \"1\")", "#f") and check
    check = assert_equals("(integer? #t)", "#f") and check

    print("\n#number?\n")
    check = assert_equals("(number? 1)", "#t") and check
    check = assert_equals("(number? 123456789)", "#t") and check
    check = assert_equals("(number? '1)", "#t") and check
    check = assert_equals("(number? 1/2)", "#t") and check
    check = assert_equals("(number? 1/1)", "#t") and check
    check = assert_equals("(number? 0/1)", "#t") and check
    check = assert_equals("(number? \"1\")", "#f") and check
    check = assert_equals("(number? #t)", "#f") and check

    print("\n#string?\n")  #add more tests after symbol->string is done
    check = assert_equals("(string? \"1\")", "#t") and check
    check = assert_equals("(string? '\"quotedstr\")", "#t") and check
    check = assert_equals("(string? \"im sexy and i know it.\")", "#t") and check
    check = assert_equals("(string? \"abc\") (+ 2 2/3)", "#t\n8/3") and check
    check = assert_equals("(string? #\\newline)", "#f") and check
    check = assert_equals("(string? '1)", "#f") and check
    check = assert_equals("(string? 1/2)", "#f") and check
    check = assert_equals("(string? #t)", "#f") and check

    print("\n#symbol? \n")
    check = assert_equals("(symbol? 'a)", "#t") and check
    check = assert_equals("(symbol? 'blah)", "#t") and check
    check = assert_equals("(symbol? 'boogala)", "#t") and check
    check = assert_equals("(symbol? '\"quotedstr\")", "#f") and check
    check = assert_equals("(symbol? \"im sexy and i know it.\")", "#f") and check
    check = assert_equals("(symbol? #\\newline)", "#f") and check
    check = assert_equals("(symbol? '1)", "#f") and check
    check = assert_equals("(symbol? 1/2)", "#f") and check
    check = assert_equals("(symbol? #t)", "#f") and check

    print("\n#quote\n")
    check = assert_equals("'(define itay 3)", "(DEFINE . (ITAY . (3 . ())))") and check
    check = assert_equals("'('a 'b 'c)",
                          "((QUOTE . (A . ())) . ((QUOTE . (B . ())) . ((QUOTE . (C . ())) . ())))") and check

    print("\n#list\n")
    check = assert_equals("(list 1 2 3 4 5 6 7 8)", "(1 . (2 . (3 . (4 . (5 . (6 . (7 . (8 . ()))))))))") and check
    check = assert_equals("(list 1 2 3 4 5)", "(1 . (2 . (3 . (4 . (5 . ())))))") and check

    print("\n#cons\n")
    check = assert_equals("(cons 1 2)", "(1 . 2)") and check
    check = assert_equals("(cons #t 'a)", "(#t . A)") and check
    check = assert_equals("(cons 1 (cons 2 (cons 3 ())))", "(1 . (2 . (3 . ())))") and check
    check = assert_equals("(cons 'a 'b)", "(A . B)") and check

    print("\n#cons and pair?\n")
    check = assert_equals("(pair? (cons #t 'a))", "#t") and check
    check = assert_equals("(pair? (cons 1 (cons 2 (cons 3 ()))))", "#t") and check

    print("\n#car\n")
    check = assert_equals("(car '(1 2 3))", "1") and check
    check = assert_equals("(car (cons 1 (cons 2 (cons 3 ()))))", "1") and check
    check = assert_equals("(car (cons 'a 'b))", "A") and check
    check = assert_equals("(car (cons (cons 1 2) 3))", "(1 . 2)") and check
    check = assert_equals("(car (car (cons (cons 1 2) 3)))", "1") and check

    print("\n#cdr\n")
    check = assert_equals("(cdr '(1 2 3))", "(2 . (3 . ()))") and check
    check = assert_equals("(cdr (cons 1 (cons 2 (cons 3 ()))))", "(2 . (3 . ()))") and check
    check = assert_equals("(cdr '(1 . 2))", "2") and check
    check = assert_equals("(cdr (cons 1 2))", "2") and check
    check = assert_equals("(cdr (cons 'a 'c))", "C") and check
    check = assert_equals("(cdr (cons (cons 1 2) 3))", "3") and check
    check = assert_equals("(cdr (cdr (cdr '(1 . (2 . (3 . ()))))))", "()") and check

    print("\n#combo car cdr\n")
    check = assert_equals("(car (cdr '(1 2 3)))", "2") and check
    check = assert_equals("(car (cdr (cdr '(1 . (2 . (3 . ()))))))", "3") and check
    check = assert_equals("(car (cdr '(1 . (2 . (3 . ())))))", "2") and check
    check = assert_equals("(cdr (cons 1 2))", "2") and check
    check = assert_equals("(cdr (cons 'a 'b))", "B") and check
    check = assert_equals("(car (cons 1 2))", "1") and check
    check = assert_equals("(car (cons 'c 'd))", "C") and check
    check = assert_equals("(cdr (cons 'a (cons 'b 'c)))", "(B . C)") and check
    check = assert_equals("(cons 1 4)", "(1 . 4)") and check
    check = assert_equals("(cons (car '(1)) (car '(4)))", "(1 . 4)") and check

    print("\n#vector\n")
    check = assert_equals("'#( #t '(4 5 6) '())",
                          "#3(#t (QUOTE . ((4 . (5 . (6 . ()))) . ())) (QUOTE . (() . ())))") and check

    print("\n#string-length\n")
    check = assert_equals("(string-length \"itayPitay\")", "9") and check
    check = assert_equals("(string-length \"\")", "0") and check

    print("\n#vector-length\n")
    check = assert_equals("(vector-length #(hello my name is kaki))", "5") and check
    check = assert_equals("(vector-length '#( #t '(4 5 6) '()))", "3") and check
    check = assert_equals("(vector-length '#(define itay 3))", "3") and check
    check = assert_equals("(vector-length #())", "0") and check

    print("\n#append\n")
    check = assert_equals("(append '(1 2 3) '(4 5 6))", "(1 . (2 . (3 . (4 . (5 . (6 . ()))))))") and check
    check = assert_equals("(append '() '(4 5 6))", "(4 . (5 . (6 . ())))") and check
    check = assert_equals("(append () '(4 5 6))", "(4 . (5 . (6 . ())))") and check
    check = assert_equals("(append '(4 5 6) '() )", "(4 . (5 . (6 . ())))") and check
    check = assert_equals("(append '(4 5 6) () )", "(4 . (5 . (6 . ())))") and check

    print("\n#reverse\n")
    check = assert_equals("(reverse '(1 2 3))", "(3 . (2 . (1 . ())))") and check
    check = assert_equals("(reverse '())", "()") and check
    check = assert_equals("(reverse ())", "()") and check
    check = assert_equals("(reverse '(1))", "(1 . ())") and check

    print("\n#zero?\n")
    check = assert_equals("(zero? 0)", "#t") and check
    check = assert_equals("(zero? 0/2)", "#t") and check
    check = assert_equals("(zero? 1)", "#f") and check
    check = assert_equals("(zero? 1/1)", "#f") and check
    check = assert_equals("(zero? 'a)", "#f") and check
    check = assert_equals("(zero? (lambda x x))", "#f") and check

    print("\n#apply\n")
    check = assert_equals("(apply zero? '(0))", "#t") and check
    check = assert_equals("(apply + 0/2 '(0 1 2))", "6/2") and check
    check = assert_equals("(apply + 1/2 '(0 1/2 2))", "12/4") and check
    check = assert_equals("(apply + 1/2 0/1 0 '(0 1/2 2))", "12/4") and check
    check = assert_equals("(apply + '(1/2 0 1/2 2))", "12/4") and check
    check = assert_equals("(apply + 1/2 0 1/2 2 ())", "12/4") and check
    check = assert_equals("(apply (lambda (a b c) b) 1999 2999 3999 ())", "2999") and check
    check = assert_equals(
        "(apply (lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) a ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 ())",
        "1999") and check
    check = assert_equals(
        "(apply (lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) d ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 ())",
        "4999") and check
    check = assert_equals(
        "(apply (lambda (a b c) ((lambda (d e f) ((lambda (g h i) ((lambda (j k l) g ) 10999 11999 12999) ) 7999 8999 9999 ) ) 4999 5999 6999 )) 1999 2999 3999 ())",
        "7999") and check

    print("\n#negative?\n")
    check = assert_equals("(negative? -1)", "#t") and check
    check = assert_equals("(negative? -3/3)", "#t") and check
    check = assert_equals("(negative? (- 1 5))", "#t") and check
    check = assert_equals("(negative? (- -1 0))", "#t") and check
    check = assert_equals("(negative? (- -2 1/2))", "#t") and check
    check = assert_equals("(negative? (- 0 -1))", "#f") and check
    check = assert_equals("(negative? (- 0/1 -1/1))", "#f") and check
    check = assert_equals("(negative? 0)", "#f") and check
    check = assert_equals("(negative? 6)", "#f") and check
    check = assert_equals("(negative? 6/7)", "#f") and check

    print("\n#fraction?\n")
    check = assert_equals("(fraction? 6/7)", "#t") and check
    check = assert_equals("(fraction? (/ 6 7))", "#t") and check
    check = assert_equals("(fraction? (/ 0 1))", "#f") and check
    check = assert_equals("(fraction? 12)", "#f") and check
    check = assert_equals("(fraction? 'a)", "#f") and check

    print("\n#void?\n")
    check = assert_equals("(void? (if #f 1))", "#t") and check
    check = assert_equals("(void? (if #t 1))", "#f") and check

    print("\n#MAKE STRING\n")
    check = assert_equals("(make-string 10 #\-)", "\"----------\"") and check
    check = assert_equals("(make-string 5 #\+)", "\"+++++\"") and check
    check = assert_equals("(make-string 3 #\=)", "\"===\"") and check

    print("\n#MAKE vector\n")
    check = assert_equals("(make-vector 3 'a)", "#3(A A A)") and check
    check = assert_equals("(make-vector 5 (car (cons 1 2)))", "#5(1 1 1 1 1)") and check
    check = assert_equals("(make-vector 6 )", "#6(0 0 0 0 0 0)") and check
    check = assert_equals("(make-vector 8)", "#8(0 0 0 0 0 0 0 0)") and check

    print("\n#vector-ref\n")
    check = assert_equals("(vector-ref '#(#t #f) 1)", "#f") and check
    check = assert_equals("(vector-ref '#(#t #f) 0)", "#t") and check
    check = assert_equals("(vector-ref '#( #t '(4 5 6) '()) 0)", "#t") and check
    check = assert_equals("(vector-ref '#(hello my name is kaki) 2)", "NAME") and check

    print("\n#vector\n")
    check = assert_equals("(vector)", "#0()") and check
    check = assert_equals("(vector 1 2 3)", "#3(1 2 3)") and check
    check = assert_equals("(vector #t '(4 5 6) '())", "#3(#t (4 . (5 . (6 . ()))) ())") and check

    print("\n#string-ref\n")
    check = assert_equals("(string-ref \"1\" 0)", "#\\1") and check
    check = assert_equals("(string-ref \"quotedstr\" 2)", "#\\o") and check
    check = assert_equals("(string-ref \"im sexy and i know it.\" 6)", "#\\y") and check

    print("\n#APPLY checks\n")
    check = assert_equals("(apply + '(4))", "4") and check
    check = assert_equals("(apply + '(2))", "2") and check
    check = assert_equals("(apply + '(4))", "4") and check
    check = assert_equals("(apply + '(8))", "8") and check
    check = assert_equals("(apply + '(14))", "14") and check
    check = assert_equals("(apply cons 1 2 '())", "(1 . 2)") and check
    check = assert_equals("(apply cons '(1 2))", "(1 . 2)") and check
    check = assert_equals("(apply cons 1 '(2))", "(1 . 2)") and check
    check = assert_equals("(apply (lambda (x) ((lambda (x) x) 5)) 3 '())", "5") and check
    check = assert_equals("(apply (lambda (x) ((lambda () x) )) 3 '())", "3") and check
    check = assert_equals("(apply (lambda (x y) (apply cons x y '())) '(1 2))", "(1 . 2)") and check

    print("\n#MAP checks\n")
    check = assert_equals("(map + '(1 2 3) '(4 5 6))", "(5 . (7 . (9 . ())))") and check
    check = assert_equals("(map + '(1 2 3) '(4 5 6) '(7 8 9))", "(12 . (15 . (18 . ())))") and check
    check = assert_equals("(map + '(1 2 3))", "(1 . (2 . (3 . ())))") and check
    check = assert_equals("(map + '() '() '())", "()") and check
    check = assert_equals("(map zero? '(3))", "(#f . ())") and check
    check = assert_equals("(map cons '(13 40) '(37 4))", "((13 . 37) . ((40 . 4) . ()))") and check
    check = assert_equals("(map (lambda (x y z) 5) '(1 2 3 4 ) '(1 2 3 4 ) '(1 1 1 1 ))",
                          "(5 . (5 . (5 . (5 . ()))))") and check
    check = assert_equals("(map list '(1 2) '(4 5) '(7 8))",
                          "((1 . (4 . (7 . ()))) . ((2 . (5 . (8 . ()))) . ()))") and check
    check = assert_equals("(map cons '(1) '(2))", "((1 . 2) . ())") and check
    check = assert_equals("((lambda (x y ) (map cons x y)) '(1) '(2))", "((1 . 2) . ())") and check
    check = assert_equals("(map cons '((1)) '((2)))", "(((1 . ()) . (2 . ())) . ())") and check
    check = assert_equals("(map (lambda (x y ) (cons x y)) '(1) '(2))", "((1 . 2) . ())") and check
    check = assert_equals("(map (lambda (x y ) ((lambda (x y) (cons x y)) x y)) '(1) '(2))", "((1 . 2) . ())") and check
    check = assert_equals("(map (lambda (x) (map zero? x)) '((1)))", "((#f . ()) . ())") and check

    print("\n#symbol->string\n")
    check = assert_equals("(symbol->string 'ITAY)", "\"ITAY\"") and check
    check = assert_equals("(symbol->string ((lambda () 'ITAY)))", "\"ITAY\"") and check
    check = assert_equals("(apply symbol->string ((lambda () 'ITAY)) ())", "\"ITAY\"") and check
    check = assert_equals("(or #f #f #f (apply symbol->string ((lambda () 'ITAY)) ()))", "\"ITAY\"") and check
    check = assert_equals("(symbol->string 'itayPitay)", "\"ITAYPITAY\"") and check
    check = assert_equals("(eq? (symbol->string 'itayPitay) (symbol->string 'itayPitay))", "#f") and check

    print("\n#string->symbol\n")
    check = assert_equals("(string->symbol \"ITAY\")", "ITAY") and check  #NOT WORKING PRINTING ITAY AND NOT "ITAY"
    check = assert_equals("'(define itayPitay king)\n\n(string->symbol \"ITAY\")",
                          "(DEFINE . (ITAYPITAY . (KING . ())))\nITAY") and check
    check = assert_equals("'(define itay king)\n\n(string->symbol \"ITAY\")",
                          "(DEFINE . (ITAY . (KING . ())))\nITAY") and check

    check = assert_equals("(string->symbol \"ITAY\")", "ITAY") and check
    check = assert_equals("(string->symbol \"a\")", "a") and check
    check = assert_equals("(string->symbol \"eran\")", "eran") and check

    check = assert_equals("(eq? (string->symbol \"ITAY\") (string->symbol \"ITAY\"))", "#t") and check
    check = assert_equals("(eq? (string->symbol \"ITAY\") 'itay)", "#t") and check
    check = assert_equals("(eq? (string->symbol \"ITAY\") 'ITAY)", "#t") and check



    #FROM HERE WE ALSO CHECK FULL FILES.

    print("\n#check =\n")
    check = assert_equals("""
(= 1)
(= 1 1)
(= 1 1/1)
(= (+ 1/2 1/2) (- 4/3 1/3) (/ 2 2) (/ 1 1) (* 2 1/2) (* 1 1/1) 1 1/1 2/2 3/3 4/4)
(= 0 0/1 0/2 (- 1 1))

(= 1 2)
(= 1/1 1/2)
(= 1 2 3 4)
(= 1 1/2 1/3)

""", "#t\n#t\n#t\n#t\n#t\n#f\n#f\n#f\n#f") and check

    print("\n#check >\n")
    check = assert_equals("""


(> 0)
(> 2 1)
(> 9 8 7 6 5 4 3 2 1)
(> 9/1 8/1 7/2 6/2 2 1)
(> 1/2 1/3 1/4 1/5)
(> 1/2 -1)


(> -1 2)
(> 1 2)
(> 1 2 3 4)
(> 1/1 2/2 3/3 4/4)
(> 1/5 1/3 1/2)
  
    

""", "#t\n#t\n#t\n#t\n#t\n#t\n#f\n#f\n#f\n#f\n#f") and check

    print("\n#check <\n")
    check = assert_equals("""


(< 0)
(< 2 1)
(< 9 8 7 6 5 4 3 2 1)
(< 9/1 8/1 7/2 6/2 2 1)
(< 1/2 1/3 1/4 1/5)
(< 1/2 -1)


(< -1 2)
(< 1 2)
(< 1 2 3 4)
(< 1/1 2/2 3/3 4/4)
(< 1/5 1/3 1/2)


    

""", "#t\n#f\n#f\n#f\n#f\n#f\n#t\n#t\n#t\n#f\n#t") and check

    print("\n#check < >\n")
    check = assert_equals("""


(> 1/1 2/2 3/3 4/4)
(< 1/1 2/2 3/3 4/4)


""", "#f\n#f") and check

    print("\n#remainder\n")
    check = assert_equals("""


(= (remainder 6 4) 2)
(= (remainder 6 -4) 2)
(= (remainder -6 4) -2)


(= (remainder -6 -4) -2)
(= (remainder 1 6) 1)
(= (remainder -1 6) -1)

(= (remainder 0 6) 0)
(= (remainder 6 3) 0)


""", "#t\n#t\n#t\n#t\n#t\n#t\n#t\n#t") and check

    print("\n#eq?\n")
    check = assert_equals("""

(define xxx (lambda y y))
(eq? 1 1)
(eq? 1 2/2)
(eq? 1/2 2/4)
(eq? 1/2 2/4)
(eq? #\\a #\\a)
(eq? 'abc 'abc)

(eq? () ())
(eq? (if #f 1234) (if #f 5678))
(eq? #t #t)
(eq? #f #f)

(eq? '(1 2 3) '(1 2 3))
(eq? '#(1 2 3) '#(1 2 3))

(eq? "abc" "abc")

(eq? xxx xxx)

(eq? 1 'a)
(eq? '(1 2 3) '#(1 2 3))
(eq? 1/2 1)
(eq? #t #f)
(eq? #f #t)

""",
                          "#t\n#t\n#t\n#t\n#t\n#t\n#t\n#t\n#t\n#t\n#f\n#f\n#t\n#t\n#f\n#f\n#f\n#f\n#f") and check  #(eq? (cdr '(a b c) ) '(b c))

    print("\n#QUASI-QUOTE\n")
    check = assert_equals("""
(define d 4999)
(define foo +)
(define x 1234)
(define y 5678)
(define g 7999)
  
`(a b c ,d e f ,@(list (foo x y)) ,g h)


""", "(A . (B . (C . (4999 . (E . (F . (6912 . (7999 . (H . ())))))))))") and check

    if (check):
        print("All is good\n")


start_time = datetime.now()
run()
end_time = datetime.now()
execution_time = end_time - start_time
print("Executed in %d seconds." % (execution_time.total_seconds()))




