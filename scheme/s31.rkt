#lang racket
(define diff
  (lambda (siki)
    (cond ((number? siki) 0)
          ((equal? 'x siki) 1)
          ((equal? '+ (car siki)) (cons '+ (map diff (cdr siki))))
          ((equal? '- (car siki)) (cons '- (map diff (cdr siki))))
          ((equal? '* (car siki)) (list '+ (list '* (cadr siki) (diff (caddr siki))) (list '* (diff (cadr siki)) (caddr siki))))
          ((equal? '** (car siki)) (list '* (caddr siki) (list '* (diff (cadr siki)) (list '** (cadr siki) (- (caddr siki) 1)))))
  )))

(define ** expt)

(define tangent
  (lambda (fx a)
    (list '+ (list '* ((eval `(lambda (x) ,(diff fx))) a) 'x) (- ((eval `(lambda (x) ,fx)) a)  (* ((eval `(lambda (x) ,(diff fx))) a) a)))
    ))
