(begin 
  (define x 10) 
  (define y 20)
  (if (> x y)
    (+ (sin x)  (cos y))
    (* x (set! y (+ y 10)))))

