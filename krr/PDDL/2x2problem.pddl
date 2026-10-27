(define (problem 2x2problem)
  (:domain 2x2domain)

  (:objects
    c11 c12 c13 c14 c15
    c21 c22 c23 c24 c25
    c31 c32 c33 c34 c35
    c41 c42 c43 c44 c45 - cell

    pink1 pink2 pink3 pink4 - tile
    bigblock - block
  )

  (:init
    ;; adjacency (north/south)
    (north c11 c12) (south c12 c11)
    (north c12 c13) (south c13 c12)
    (north c13 c14) (south c14 c13)
    (north c14 c15) (south c15 c14)

    (north c21 c22) (south c22 c21)
    (north c22 c23) (south c23 c22)
    (north c23 c24) (south c24 c23)
    (north c24 c25) (south c25 c24)

    (north c31 c32) (south c32 c31)
    (north c32 c33) (south c33 c32)
    (north c33 c34) (south c34 c33)
    (north c34 c35) (south c35 c34)

    (north c41 c42) (south c42 c41)
    (north c42 c43) (south c43 c42)
    (north c43 c44) (south c44 c43)
    (north c44 c45) (south c45 c44)

    ;; adjacency (east/west) - follow same convention: (east A B) means A is east of B
    (east c21 c11) (west c11 c21)
    (east c31 c21) (west c21 c31)
    (east c41 c31) (west c31 c41)

    (east c22 c12) (west c12 c22)
    (east c32 c22) (west c22 c32)
    (east c42 c32) (west c32 c42)

    (east c23 c13) (west c13 c23)
    (east c33 c23) (west c23 c33)
    (east c43 c33) (west c33 c43)

    (east c24 c14) (west c14 c24)
    (east c34 c24) (west c24 c34)
    (east c44 c34) (west c34 c44)

    (east c25 c15) (west c15 c25)
    (east c35 c25) (west c25 c35)
    (east c45 c35) (west c35 c45)

    ;; initial placements: block anchor at c11 (covers c11,c12,c21,c22)
    (occupies bigblock c11)

    (at pink1 c13) (at pink2 c23) (at pink3 c33) (at pink4 c43)

    ;; mark empties (all cells not covered by block or pinks)
    (empty c14) (empty c15)
    (empty c24) (empty c25)
    (empty c31) (empty c32) (empty c34) (empty c35)
    (empty c41) (empty c42) (empty c44) (empty c45)
  )

  (:goal
    (occupies bigblock c24)
  )
)