from main import execute_program


progs =[
   
    ('''(+ 100 200)''', 300),
    ('''(- 2 2)''',   0),
    ('''(* 3 2 2)''', 12),
    ('''(/ 6 2)''',   3),
    ('''(if (> 1 2) (+ 2 2) (* 2 3))''',   6),
    ('''(if (> 3 2) (+ 1 2) (* 2 3))''',   3),
    ('''(begin (define x 10) (set! x (+ 2 x)) (+ 1 x))''',13),
    ('''(define x 10)''', None),
    
    
    # String 
    
    ('''(print "hello")''','"hello"'),
    ('''(print "hello world")''','"hello world"'),
    
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
    ('''(begin (define amount (lambda (r) (* 2 (* r r)))) (amount 20))''',800)
]
    
    
if __name__ == "__main__":
    for prog in progs:
        source, output = prog
        out = execute_program(source, file=False)
        assert out == output
        print(f'Test: {source} => {out}','......OK')
