(define (domain hello_world)
  (:requirements :strips :typing)
  
  (:types
    person - object
  )
  
  (:predicates
    (greeted ?p1 ?p2 - person)  ; p1 has greeted p2
  )
  
  (:action say-hello
    :parameters (?speaker ?listener - person)
    :precondition (not (greeted ?speaker ?listener))
    :effect (greeted ?speaker ?listener)
  )
)