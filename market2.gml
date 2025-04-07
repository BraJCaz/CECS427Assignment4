graph [
  directed 0

  // Buyers
  node [
    id "B1"
    label "B1"
    type "buyer"
  ]
  node [
    id "B2"
    label "B2"
    type "buyer"
  ]
  node [
    id "B3"
    label "B3"
    type "buyer"
  ]

  // Sellers
  node [
    id "S1"
    label "S1"
    type "seller"
    price 0
  ]
  node [
    id "S2"
    label "S2"
    type "seller"
    price 0
  ]

  // Valuations (edges between buyers and sellers)
  edge [
    source "B1"
    target "S1"
    valuation 10
  ]
  edge [
    source "B1"
    target "S2"
    valuation 8
  ]
  edge [
    source "B2"
    target "S1"
    valuation 6
  ]
  edge [
    source "B2"
    target "S2"
    valuation 9
  ]
  edge [
    source "B3"
    target "S1"
    valuation 7
  ]
  edge [
    source "B3"
    target "S2"
    valuation 10
  ]
]
