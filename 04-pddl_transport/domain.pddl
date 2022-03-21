(define (domain transport)
    (:predicates (car ?c) (place ?p) (box ?b) (at ?x ?y) (empty ?c) (full ?c))
    (:action load
        :parameters (?b ?c ?p)
        :precondition (and 
                    (box ?b)
                    (car ?c)
                    (place ?p)
                    (empty ?c)
                    (at ?c ?p)
                    (at ?b ?p)
                    )
        :effect (and 
                (at ?b ?c)
                (not (at ?b ?p))
                (full ?c)
                (not (empty ?c)
                ))
    )
    (:action unload
        :parameters (?b ?c ?p)
        :precondition (and 
                    (box ?b)
                    (car ?c)
                    (place ?p)
                    (full ?c)
                    (at ?c ?p)
                    (at ?b ?c)
                    )
        :effect (and 
                (at ?b ?p)
                (not (at ?b ?c))
                (empty ?c)
                (not (full ?c)
                ))
    )
    (:action move
        :parameters (?c ?po ?pd)
        :precondition (and 
                    (car ?c)
                    (place ?po)
                    (place ?pd)
                    (at ?c ?po)
                    )
        :effect (and
                    (at ?c ?pd) 
                    (not (at ?c ?po))
                    )
    )
    
    
    
)