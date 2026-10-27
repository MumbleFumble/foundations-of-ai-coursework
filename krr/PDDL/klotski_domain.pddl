(define (domain klotski_domain)
  (:requirements :strips :typing :equality)

  (:types
    cell - object
    block - object
    block1x1 block1x2 block2x1 block2x2 - block
  )

  (:predicates
    ;; grid adjacency
    (north ?c1 ?c2 - cell)
    (south ?c1 ?c2 - cell)
    (east ?c1 ?c2 - cell)
    (west ?c1 ?c2 - cell)

    ;; which cells each block occupies
    (occupies ?b - block ?c - cell)

    ;; whether a cell is free
    (empty ?c - cell)
  )

  ;; Generic template for movement of any block
  ;; We'll duplicate it for each direction for clarity
  (:action slide-north
    :parameters (?b - block ?from1 ?to1 - cell)
    :precondition (and
      (occupies ?b ?from1)
      (north ?to1 ?from1)
      (empty ?to1)
    )
    :effect (and
      (not (occupies ?b ?from1))
      (occupies ?b ?to1)
      (empty ?from1)
      (not (empty ?to1))
    )
  )

  (:action slide-south
    :parameters (?b - block ?from1 ?to1 - cell)
    :precondition (and
      (occupies ?b ?from1)
      (south ?to1 ?from1)
      (empty ?to1)
    )
    :effect (and
      (not (occupies ?b ?from1))
      (occupies ?b ?to1)
      (empty ?from1)
      (not (empty ?to1))
    )
  )

  (:action slide-east
    :parameters (?b - block ?from1 ?to1 - cell)
    :precondition (and
      (occupies ?b ?from1)
      (east ?to1 ?from1)
      (empty ?to1)
    )
    :effect (and
      (not (occupies ?b ?from1))
      (occupies ?b ?to1)
      (empty ?from1)
      (not (empty ?to1))
    )
  )

  (:action slide-west
    :parameters (?b - block ?from1 ?to1 - cell)
    :precondition (and
      (occupies ?b ?from1)
      (west ?to1 ?from1)
      (empty ?to1)
    )
    :effect (and
      (not (occupies ?b ?from1))
      (occupies ?b ?to1)
      (empty ?from1)
      (not (empty ?to1))
    )
  )
)
