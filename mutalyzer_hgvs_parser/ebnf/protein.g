description: reference ":" (COORDINATE_SYSTEM ".")? variants

reference: ID reference? | "(" ID reference? ")"

ID: (LETTER | DIGIT) (LETTER | DIGIT | "." | "_" | "-")*

COORDINATE_SYSTEM: "p"

// -----

variants: ("[" (variant (";" variant)*) "]") | variant | "="

variant: variant_certain | variant_uncertain

variant_uncertain: "(" variant_certain ")"

variant_certain: (location (deletion | deletion_insertion | duplication
                           | equal  | frame_shift | insertion
                           | substitution)?)
                           | extension

location: point | range

point: (AA? NUMBER) | UNKNOWN

range: point "_" point

// -----

deletion: "del" inserted?

deletion_insertion: "delins" inserted?

duplication: "dup" inserted?

equal: "=" inserted?

extension: "Met1" "ext" "-" NUMBER | ("*" | "Ter") point PSEQUENCE "ext" ("*" | "Ter") point

frame_shift: "fs" | AA "fs" ("*" | "Ter") location

insertion: "ins" inserted

substitution: inserted?

// ----

inserted: ("[" (insert (";" insert)*) "]") | insert

insert: (PSEQUENCE | description | location | length) ("[" repeat_number "]")?
        | repeat_mixed+

repeat_number: NUMBER | UNKNOWN

repeat_mixed: (PSEQUENCE  | location) "[" repeat_number "]"

length: NUMBER | UNKNOWN | "(" (NUMBER | UNKNOWN ) ")"

// ----

LETTER: UCASE_LETTER | LCASE_LETTER

LCASE_LETTER: "a".."z"

UCASE_LETTER: "A".."Z"

DIGIT: "0".."9"

AA: "Ala" | "Arg" | "Asn" | "Asp" | "Cys" | "Gln" | "Glu"
  | "Gly" | "His" | "Ile" | "Leu" | "Lys" | "Met" | "Phe"
  | "Pro" | "Ser" | "Thr" | "Trp" | "Tyr" | "Val"
  | "Ter"
  | "A"   | "R"   | "N"   | "D"   | "C"   | "Q"   | "E"
  | "G"   | "H"   | "I"   | "L"   | "K"   | "M"   | "F"
  | "P"   | "S"   | "T"   | "W"    | "Y"  | "V"
  | "*"
  | "X"

PSEQUENCE: AA+

NUMBER: DIGIT+

UNKNOWN: "?"
