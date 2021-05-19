# lipy
An interpreter for lisp/scheme dialect of programming.

[Example programs!](https://github.com/berkio3x/lipy/tree/main/examples)
```
                                 .-'~~~-.
                               .'o  oOOOo`.
                              :~~~-.oOo   o`.
                               `. \ ~-.  oOOo.
                                 `.; / ~.  OO:
                                 .'  ;-- `.o.'
                                ,'  ; ~~--'~
                                ;  ;
          _______\|/__________\\;_\\//___\|/________
```

#### A simple program using variable assignment/conditional execution/inbuilt available math funcitons
```lisp
  (begin 
      (define x 10) 
      (define y 20)
      (if (< x y)
          (+ (sin x)  (cos y))
          (* x y)))
  ```
  Calculate factorial
  ```lisp
   (begin 
   (define fact (lambda (n) 
       (if 
        (<= n 1) 
        1 
        (* n (fact (- n 1))))))
   (fact 100))
   
output:
933262154439441526816992388562667004907159682643816214685929638952175999932299156089414639761565182862
53697920827223758251185210916864000000000000000000000000

Time:
real    0m0.071s
user    0m0.057s
sys     0m0.014s

```

### variable assignment.
## set!
```lisp
  ( begin
        (define x 10)
        (set! x (+ x 10))
        (* x 2))
```
#### Procedures.
## lambda
```lisp
    (begin 
        (define amount (lambda (r) (* 2 (* r r))))
        (amount 20)
    )
```


#### Running the interpreter.
`python3.10 main.py examples/factorial.prog`
### NOTE:
  - To run with debug info , use `--loglevel debug` flag
  
