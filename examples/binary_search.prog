(begin
    (define binary-search (lambda (v start end key)
        (define idx -1)
        (define mid  (floor (/ (+ start end) 2)))
        (if (equal? key (list-ref v mid))
            (* 1 mid)
            (if (> key (list-ref v mid))
                (binary-search v (+ mid 1) (length v) key)
                (binary-search v  start    (- mid 1)  key)
            )
            )
            ))
    (binary-search (list 1 2 3 4 5 6) 0 6 5)
            
)
            
