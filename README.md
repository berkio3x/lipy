# lipy
An interpreter for lisp/scheme dialect of programming

#### A simple program using variable assignment/conditional execution/inbuilt available math funcitons
```lisp
  (begin 
      (define x 10) 
      (define y 20)
      (if (< x y)
          (+ (sin x)  (cos y))
          (* x y)))
  ```
