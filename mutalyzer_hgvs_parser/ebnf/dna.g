description_dna: reference ":" (COORDINATE_SYSTEM ".")? variants

// -----

variants: ("[" ((variant (";" variant)*) | "=") "]") | variant | "="

variant: location (conversion | deletion | deletion_insertion | duplication
                  | equal | insertion | inversion | substitution | repeat)?

// -----

location: point | uncertain_point | range

point: OUTSIDE_CDS? (NUMBER | UNKNOWN) OFFSET?

OUTSIDE_CDS: "*" | "-"

OFFSET: ("+" | "-")? (NUMBER | UNKNOWN)

uncertain_point: "(" point "_" point ")"

range: (point | uncertain_point) "_" (point | uncertain_point)

exact_range: (NUMBER | UNKNOWN) "_" (NUMBER | UNKNOWN)

// -----

conversion: "con" inserted

deletion: "del" inserted?

deletion_insertion: "del" inserted? "ins" inserted

duplication: "dup" inserted?

equal: "="

insertion: "ins" inserted

inversion: "inv" inserted?

repeat: inserted

substitution: SEQUENCE? ">" inserted

// -----

inserted: ("[" (insert (";" insert)*) "]") | insert

insert: ((SEQUENCE | description_dna | location | length) ((INVERTED? ("[" repeat_number "]")?)
                                                     | (("[" repeat_number "]")? INVERTED?))?)
        | repeat_mixed+

INVERTED: "inv"

repeat_number: NUMBER | UNKNOWN | exact_range

repeat_mixed: (SEQUENCE  | location) "[" repeat_number "]" INVERTED?

length: NUMBER | UNKNOWN | "(" (NUMBER | UNKNOWN | exact_range) ")"

// -----

SEQUENCE: NT+

NT: "a" | "c" | "g" | "t" | "u" | "r" | "y" | "k"
  | "m" | "s" | "w" | "b" | "d" | "h" | "v" | "n"
  | "A" | "C" | "G" | "T" | "U" | "R" | "Y" | "K"
  | "M" | "S" | "W" | "B" | "D" | "H" | "V" | "N"
