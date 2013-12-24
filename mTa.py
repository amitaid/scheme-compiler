import os
import tag_parser


def runInPetite(s):
    text_file = open("Output.txt", "w")
    text_file.write(s)
    text_file.close()
    os.system("cat Output.txt | petite > 1.txt")
    reader = open("1.txt", 'r')
    output = reader.readlines()[3].strip()
    reader.close()
    os.system("rm 1.txt")
    #os.system("rm Output.txt") 
    return output[4:]


def testEqualInScheme(expected, prominant):
    stringToTest = "(case-sensitive #f)(equal? {0} {1})".format(expected, prominant)
    return runInPetite(stringToTest)


def testEqualInSchemeQuote(expected, prominant):
    stringToTest = "(case-sensitive #f)(equal? '{0} '{1})".format(expected, prominant)
    return runInPetite(stringToTest)

# Omer addition 
def testEqualInSchemeYag(expected, prominant):
    stringToTest = "(case-sensitive #f) (let ((yag (lambda fl (map (lambda (f) (f)) ((lambda (x) (x x)) (lambda (p) (map (lambda (f)\
                    (lambda () (apply f (map (lambda (ff) (lambda y (apply (ff) y))) (p p) )))) fl))))))) \
                    (equal? (car {0}) {1}))".format(expected, prominant)

    return runInPetite(stringToTest)


parse = tag_parser.AbstractSchemeExpr.parse
tests = list()

tests.append(["'4", "Constant", testEqualInScheme])
tests.append(["'3/4", "Constant", testEqualInScheme])
tests.append(["'asdf", "Constant", testEqualInScheme])
tests.append(['"moshe"', "Constant", testEqualInScheme])
tests.append(['\'"moshe"', "Constant", testEqualInScheme])
tests.append(["'#t", "Constant", testEqualInScheme])
tests.append(["'#F", "Constant", testEqualInScheme])
tests.append(["'#(2 3 4)", "Constant", testEqualInScheme])
tests.append(["'#(2 3 4 (5 6 7) (8 9))", "Constant", testEqualInScheme])
tests.append(["'(2 . 3)", "Constant", testEqualInScheme])
tests.append(["'(2 3)", "Constant", testEqualInScheme])
tests.append(["'()", "Constant", testEqualInScheme])
tests.append(["'#()", "Constant", testEqualInScheme])
tests.append(["'(1 () 2 (3 . 4) (5 . 6) (7 8 . 9) . 10)", "Constant", testEqualInScheme])

tests.append(["4", "Constant", testEqualInScheme])
tests.append(["4/3", "Constant", testEqualInScheme])
tests.append(["#t", "Constant", testEqualInScheme])
tests.append(["#F", "Constant", testEqualInScheme])

tests.append(["(if 1 2 3)", "IfThenElse", testEqualInScheme])
tests.append(["(if #t 2 3)", "IfThenElse", testEqualInScheme])
tests.append(["(if #f 2 3)", "IfThenElse", testEqualInScheme])

tests.append(["(car '(a b c))", "Applic", testEqualInScheme])
tests.append(["(cons 'a 'b)", "Applic", testEqualInScheme])
tests.append(["(car (cdr (cdr '(a b c))))", "Applic", testEqualInScheme])
tests.append(["(null? (cdr (cdr (cdr '(a b c)))))", "Applic", testEqualInScheme])
tests.append(["""(let ((a 2) (b 3) (c 5))
  (+ a b c))""", "Applic", testEqualInScheme])
tests.append(["(or 1 2 3)", "Or", testEqualInScheme])
tests.append(["(and 1 2 3)", "IfThenElse", testEqualInScheme])
tests.append(["""(cond (#f 1)
      (#f 2)
      (#f 3)
      (#f 4)
      (else 'ok))""", "IfThenElse", testEqualInScheme])
tests.append(["""(let* ((a 2)
       (a (+ a 1)) ; 3
       (a (+ a 1)) ; 4
       (a (+ a 1)) ; 5
       )
  (* a a)) ; 25\n """, "Applic", testEqualInScheme])

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
  