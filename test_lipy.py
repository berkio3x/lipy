from main import execute_program


progs =[
    (
    '''
    ( begin
        (define x 10)
        (set! x (+ x 10))
        (* x 2))
    ''',
    40),
    
    ('''
    (begin 
        (define amount (lambda (r) (* 2 (* r r))))
        (amount 20)
    )
    ''',
    800)
]
    
    
if __name__ == "__main__":
    for prog in progs:
        source, output = prog
        assert execute_program(source, file=False) == output
