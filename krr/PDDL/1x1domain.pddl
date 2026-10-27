(define (domain 1x1domain)
  (:requirements :strips :typing)
  
  (:types
    cell - object
    tile - object
  )
  (:predicates
    ;; Grid structure
    (north ?c1 ?c2 - cell)     ; c1 is north of c2
    (south ?c1 ?c2 - cell)     ; c1 is south of c2
    (east ?c1 ?c2 - cell)      ; c1 is east of c2
    (west ?c1 ?c2 - cell)      ; c1 is west of c2

    ;;tile is at a cell
    (at ?t - tile ?c - cell)

    ;; if cell is empty
    (empty ?c - cell)
  )

  ;; Slide a tile north into an adjacent empty cell
  (:action slide-north
    :parameters (?tile - tile ?from - cell ?to - cell)
    :precondition (and
      (at ?tile ?from)
      (empty ?to)
      (north ?to ?from)
    )
    :effect (and
      (not (at ?tile ?from))
      (at ?tile ?to)
      (not (empty ?to))
      (empty ?from)
    )
  )
  ;; Slide a tile south into an adjacent empty cell
  (:action slide-south
    :parameters (?tile - tile ?from - cell ?to - cell)
    :precondition (and
      (at ?tile ?from)
      (empty ?to)
      (south ?to ?from)
    )
    :effect (and
      (not (at ?tile ?from))
      (at ?tile ?to)
      (not (empty ?to))
      (empty ?from)
    )
  )
  ;; Slide a tile east into an adjacent empty cell
  (:action slide-east
    :parameters (?tile - tile ?from - cell ?to - cell)
    :precondition (and
      (at ?tile ?from)
      (empty ?to)
      (east ?to ?from)
    )
    :effect (and
      (not (at ?tile ?from))
      (at ?tile ?to)
      (not (empty ?to))
      (empty ?from)
    )
  )
  ;; Slide a tile west into an adjacent empty cell
  (:action slide-west
    :parameters (?tile - tile ?from - cell ?to - cell)
    :precondition (and
      (at ?tile ?from)
      (empty ?to)
      (west ?to ?from)
    )
    :effect (and
      (not (at ?tile ?from))
      (at ?tile ?to)
      (not (empty ?to))
      (empty ?from)
    )
  )
)