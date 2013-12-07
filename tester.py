import os
import tag_parser


def testEqualInScheme(expected, prominant):
    os.system("echo (equal? " + expected + " " + prominant + ") | petite -q > 1.txt")
    reader = open("1.txt", 'r')
    output = reader.readline().strip()
    reader.close()
    return output


def testEqualInSchemeQuote(expected, prominant):
    os.system("echo (equal? '" + expected + " '" + prominant + ") | petite -q > 1.txt")
    reader = open("1.txt", 'r')
    output = reader.readline().strip()
    reader.close()
    return output


# Omer addition 
def testEqualInSchemeYag(expected, prominant):
    os.system("echo (let ((yag (lambda fl (map (lambda (f) (f)) ((lambda (x) (x x)) (lambda (p) (map (lambda (f) "
              "(lambda () (apply f (map (lambda (ff) (lambda y (apply (ff) y))) (p p) )))) fl))))))) "
              "(equal? (car " + expected + ") " + prominant + ")) | petite -q > 1.txt")
    reader = open("1.txt", 'r')
    output = reader.readline().strip()
    reader.close()
    return output


parse = tag_parser.AbstractSchemeExpr.parse
tests = list()

tests.append(["'x", "Constant", testEqualInScheme])
tests.append(["(lambda (x) (+ x 1))", "LambdaSimple", testEqualInSchemeQuote])
tests.append(['#\\tab', "Constant", testEqualInScheme])
tests.append(['#\\page', "Constant", testEqualInScheme])
tests.append(["(+ 1 2)", "Applic", testEqualInScheme])
tests.append(["(1 2 3 4 5)", "Applic", testEqualInSchemeQuote])
tests.append(["(let ((x 1) (y 2)) (+ x y))", "Applic", testEqualInScheme])
tests.append(["(let* ((x 1) (y x)) y)", "Applic", testEqualInScheme])
tests.append(["12345", "Constant", testEqualInScheme])
tests.append(["'12345", "Constant", testEqualInScheme])
tests.append(["'()", "Constant", testEqualInScheme])
tests.append(["(if #t 1)", "IfThenElse", testEqualInScheme])
tests.append(["(if #f 1 2)", "IfThenElse", testEqualInScheme])
tests.append(["(and 1 2 3 4 5)", "IfThenElse", testEqualInScheme])
tests.append(["(or #f #f 1)", "Or", testEqualInScheme])
tests.append(["(define x 1)", "Def", testEqualInSchemeQuote])
tests.append(["(cond (#f 1) (else 7))", "IfThenElse", testEqualInScheme])
tests.append(["#\\newline", "Constant", testEqualInScheme])
tests.append(["(let* ((x 6) (y 7) (z 9) (r #t)) (+ x y))", "Applic", testEqualInScheme])
tests.append(["(lambda (x) (lambda (y) #t))", "LambdaSimple", testEqualInSchemeQuote])
tests.append(["(lambda x (lambda (y) #t))", "LambdaVar", testEqualInSchemeQuote])
tests.append(["(lambda (x . y) (lambda (y) #t))", "LambdaOpt", testEqualInSchemeQuote])
tests.append(["x", "Variable", testEqualInSchemeQuote])
tests.append(['"follow your dreams. you can reach your goals, im living proof."', "Constant", testEqualInScheme])
tests.append(["`(1 2 3)", "Applic", testEqualInScheme])
tests.append(["`('a 'b 1 'd)", "Applic", testEqualInScheme])

# Omer additions 
tests.append(['(lambda () (+ 1 2))', "LambdaSimple", testEqualInSchemeQuote])
tests.append(['(letrec ((a (lambda () 1)) (b (lambda () 1))) (+ 1 2))', "Applic", testEqualInSchemeYag])
tests.append(['`(1 ,(+ 1 2) ,@(+ 6 2))', "Applic", testEqualInScheme])

index = 1

for i in tests:
    try:
        m, r = parse(i[0])
        if r != '':
            print("Test " + str(index) + " failed. didn't parse entire string. Left to parse: " + str(r))
        elif str(i[2](str(m).lower(), i[0])) != "#t":
            print("Test " + str(index) + " failed. Input and output are not equal? in Scheme. The input: " + i[0] +
                  " The output: " + str(m))
            print(str(i[2](str(m), i[0])))
        elif i[1] not in str(type(m)):
            print("Test " + str(index) + " failed. Wrong type. expected: " + i[1] + " Got: " + str(type(m)))
        else:
            print("Test " + str(index) + " passed.")

    except Exception:
        print("Test " + str(index) + " failed. Got an exception.")
    index += 1

# Additional tests that don't fit the above pattern 
atests = list()
atests.append(["(define (x y) (+ x y))", "(define x (lambda (y) (+ x y)))", "Def"])
atests.append(["#\\lambda", "#\\lambda", "Constant"])

# Omer additions 
atests.append(["(define (x . y) (+ x y))", "(define x (lambda y (+ x y)))", "Def"])
atests.append(["(define (x . (y)) (+ x y))", "(define x (lambda (y) (+ x y)))", "Def"])
atests.append(["(define (x . (y1 . y2)) (+ x y))", "(define x (lambda (y1 . y2) (+ x y)))", "Def"])

for i in atests:
    m, r = parse(i[0])
    if r != '':
        print("Test " + str(index) + " failed. didn't parse entire string. Left to parse: " + str(r))
    elif str(m).lower() != i[1]:
        print("Test " + str(index) + " failed. Wrong output string. Expected: " + i[1] + " Got: " + str(m))
    elif i[2] not in str(type(m)):
        print("Test " + str(index) + " failed. Wrong type. expected: " + i[1] + " Got: " + str(type(m)))
    else:
        print("Test " + str(index) + " passed.")
    index += 1

# Very shallow test for Letrec 
m, r = parse("(letrec ((x (lambda (z) 1)) (y (lambda (z) 1))) (+ 1 2))")
if r != '':
    print("Test " + str(index) + " failed. didn't parse entire string. Left to parse: " + str(r))
elif "Applic" not in str(type(m)):
    print("Test " + str(index) + " failed. Wrong type. Expected Applic, Got: " + str(type(m)))
elif "yag" not in str(m).lower():
    print("Test " + str(index) + "failed. Expected to turn Letrec expression to 'Yag' application.")
else:
    print("Test " + str(index) + " passed.")
    index += 1