(define (problem hello_world_problem)
  (:domain hello_world)
  
  (:objects
    alice bob - person
  )
  
  (:init
    ; Some parsers require a non-empty init, even though we don't have any true initial predicates
    ; So we add a dummy predicate that alice has greeted alice
    (greeted alice alice)
  )
  
  (:goal
    (and
      (greeted alice bob)
      (greeted bob alice)
    )
  )
)
