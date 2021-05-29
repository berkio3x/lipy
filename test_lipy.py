from main import execute_program
from utils import colors

progs =[

    # Quote
    #('''(cons (quote a) (quote (b c)))''',["a","b","c"]),
    #("""(cons a""", "a"),
    ('''(cons 1 nil)''', [1]),  
    ('''(cons 1 1)''', [1, 1]),  
    ('''(+ -2 -4)''', -6),  
    ('''(cons -2 (- 4 2))''', [-2, 2]),  
    ('''(+ 100 200)''', 300),
    ('''(- 2 2)''',   0),
    ('''(* 3 2 2)''', 12),
    ('''(/ 6 2)''',   3),

    # Conditional Execution
    ('''(if (> 1 2) (+ 2 2) (* 2 3))''',   6),
    ('''(if (> 3 2) (+ 1 2) (* 2 3))''',   3),
    ('''(+ 1 (cond ((> 30 4) 2) ((> 4 3) 1)))''', 3),
    ('''(+ 1 (cond ((> 3 4) 1) ((> 1 3) 2) (#t 3)))''', 4),
    
    ('''(begin (define x 10) (set! x (+ 2 x)) (+ 1 x))''',13),
    ('''(define x 10)''', None),
    
    
    # String 
    
    ('''(print "hello")''','"hello"'),
    ('''(print "hello")''','"hello"'),
    ('''(string? "hello world")''','#t'),
    ('''(string? 10)''','#f'),
    ('''(string-len "Hello World")''',11),
    ('''(string-ref "Hello World" 4)''','o'),
    #('''(begin (define name "Nemo" 4) (string-set! name 0 "L" ) (print name))''','Lemo'),
    
    #Lists
    #('''(cons 1 2)''', [1,2]),
    ('''(car (list 1 2 3 4))''', 1),
    ('''(car (cdr (list 1 2 3 4)))''', 2),
    ('''(car (cdr (cdr (list 1 2 3 4))))''', 3),
    ('''(cdr (list 1 2 3 4))''', [2, 3, 4]),
    ('''(begin (define x (list 1 2 3 4)) (list-ref x 2))''',3),
    ('''(list 1 2 (list 3 4))''',[1, 2, [3, 4]]),


    # Procedures
    ('''((lambda (x) (+ x x)) 10)''',20),
    ('''(begin (define amount (lambda (r) (* 2 (* r r)))) (amount 20))''',800),
]
    
    
if __name__ == "__main__":
    for prog in progs:
        source, output = prog
        out = execute_program(source, file=False)
        try:
            assert out == output
            print(f'{colors.OKCYAN}Test:{colors.ENDC} {source} => {out},{colors.OKGREEN}......OK {colors.ENDC}')
        except AssertionError:
            print(f'Expected: {output}, got: {colors.FAIL} {out} {colors.ENDC}')
