(define (domain 2x2domain)
  (:requirements :strips :typing)
  (:types
    cell - object
    tile - object
    block - object
  )

  (:predicates
    (north ?c1 ?c2 - cell) ;; ?c1 is north of ?c2
    (south ?c1 ?c2 - cell)
    (east  ?c1 ?c2 - cell) ;; ?c1 is east of ?c2
    (west  ?c1 ?c2 - cell)

    (at ?t - tile ?c - cell)
    (occupies ?b - block ?c - cell) ;; block anchor = top-left cell
    (empty ?c - cell)
  )

  ;; 1x1 tile moves
  (:action slide-tile-north
    :parameters (?tile - tile ?from - cell ?to - cell)
    :precondition (and (at ?tile ?from) (empty ?to) (north ?to ?from))
    :effect (and (not (at ?tile ?from)) (at ?tile ?to) (not (empty ?to)) (empty ?from))
  )

  (:action slide-tile-south
    :parameters (?tile - tile ?from - cell ?to - cell)
    :precondition (and (at ?tile ?from) (empty ?to) (south ?to ?from))
    :effect (and (not (at ?tile ?from)) (at ?tile ?to) (not (empty ?to)) (empty ?from))
  )

  (:action slide-tile-east
    :parameters (?tile - tile ?from - cell ?to - cell)
    :precondition (and (at ?tile ?from) (empty ?to) (east ?to ?from))
    :effect (and (not (at ?tile ?from)) (at ?tile ?to) (not (empty ?to)) (empty ?from))
  )

  (:action slide-tile-west
    :parameters (?tile - tile ?from - cell ?to - cell)
    :precondition (and (at ?tile ?from) (empty ?to) (west ?to ?from))
    :effect (and (not (at ?tile ?from)) (at ?tile ?to) (not (empty ?to)) (empty ?from))
  )

  ;; 2x2 block moves (anchor = top-left ?from). The block covers:
  ;;   ?from, east-of-?from, south-of-?from, south-of-(east-of-?from)
  (:action slide-block-north
    :parameters (?b - block
                 ?from ?from_east ?from_south ?from_se - cell
                 ?to ?to_east - cell)
    :precondition (and
      (occupies ?b ?from)
      (east  ?from_east ?from)
      (south ?from_south ?from)
      (south ?from_se ?from_east)

      (north ?to ?from)
      (east  ?to_east ?to)

      (empty ?to)
      (empty ?to_east)
    )
    :effect (and
      (not (occupies ?b ?from)) (occupies ?b ?to)
      (not (empty ?to)) (not (empty ?to_east))
      (empty ?from_south) (empty ?from_se)
    )
  )

  (:action slide-block-south
    :parameters (?b - block
                 ?from ?from_east ?from_south ?from_se - cell
                 ?to ?to_east - cell)
    :precondition (and
      (occupies ?b ?from)
      (east  ?from_east ?from)
      (south ?from_south ?from)
      (south ?from_se ?from_east)

      (south ?to ?from)
      (east  ?to_east ?to)
      (empty ?to) (empty ?to_east)
    )
    :effect (and
      (not (occupies ?b ?from)) (occupies ?b ?to)
      (not (empty ?to)) (not (empty ?to_east))
      (empty ?from) (empty ?from_east)
    )
  )

  (:action slide-block-east
    :parameters (?b - block
                 ?from ?from_south ?from_east ?from_se - cell
                 ?to ?to_south - cell)
    :precondition (and
      (occupies ?b ?from)
      (south ?from_south ?from)
      (east  ?from_east ?from)
      (south ?from_se ?from_east)

      (east ?to ?from)
      (south ?to_south ?to)

      (empty ?to) (empty ?to_south)
    )
    :effect (and
      (not (occupies ?b ?from)) (occupies ?b ?to)
      (not (empty ?to)) (not (empty ?to_south))
      (empty ?from) (empty ?from_south)
    )
  )

  (:action slide-block-west
    :parameters (?b - block
                 ?from ?from_south ?from_east ?from_se - cell
                 ?to ?to_south - cell)
    :precondition (and
      (occupies ?b ?from)
      (south ?from_south ?from)
      (east  ?from_east ?from)
      (south ?from_se ?from_east)

      (west ?to ?from)
      (south ?to_south ?to)

      (empty ?to) (empty ?to_south)
    )
    :effect (and
      (not (occupies ?b ?from)) (occupies ?b ?to)
      (not (empty ?to)) (not (empty ?to_south))
      (empty ?from_east) (empty ?from_se)
    )
  )
)