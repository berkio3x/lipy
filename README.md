# lipy
An interpreter for lisp/scheme dialect of programming
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
