description_protein: reference ":" (COORDINATE_SYSTEM ".")? p_variants

// -----

p_variants: p_variants_certain | p_variants_predicted

p_variants_certain: "[" p_variant (";" p_variant)* "]" | p_variant | "="

p_variants_predicted: "[(" p_variant (";" p_variant)* ")]" | "(" p_variant ")" | "(=)"

p_variant: (p_location (p_deletion | p_deletion_insertion | p_duplication
                        | p_equal | frame_shift | p_insertion | p_repeat
                        | p_substitution)?)
                        | extension

// -----

p_location: p_point | p_range

p_point: (AA? NUMBER) | UNKNOWN

p_range: p_point "_" p_point

// -----

p_deletion: "del" p_inserted?

p_deletion_insertion: "del" p_inserted? "ins" p_inserted

p_duplication: "dup" p_inserted?

p_equal: "=" p_inserted?

extension: "Met1" "ext" "-" NUMBER | ("*" | "Ter") p_point P_SEQUENCE "ext" ("*" | "Ter") p_point

frame_shift: "fs" | AA "fs" ("*" | "Ter") p_location

p_insertion: "ins" p_inserted

p_repeat: p_inserted

p_substitution: p_inserted?

// ----

p_inserted: ("[" (p_insert (";" p_insert)*) "]") | p_insert

p_insert: (P_SEQUENCE | description_protein | p_location | p_length) ("[" p_repeat_number "]")?
        | p_repeat_mixed+

p_repeat_number: NUMBER | UNKNOWN

p_repeat_mixed: (P_SEQUENCE  | p_location) "[" p_repeat_number "]"

p_length: NUMBER | UNKNOWN | "(" (NUMBER | UNKNOWN ) ")"

// ----

P_SEQUENCE: AA+

AA: "Ala" | "Arg" | "Asn" | "Asp" | "Cys" | "Gln" | "Glu"
  | "Gly" | "His" | "Ile" | "Leu" | "Lys" | "Met" | "Phe"
  | "Pro" | "Ser" | "Thr" | "Trp" | "Tyr" | "Val"
  | "Ter"
  | "Xaa"
  | "A"   | "R"   | "N"   | "D"   | "C"   | "Q"   | "E"
  | "G"   | "H"   | "I"   | "L"   | "K"   | "M"   | "F"
  | "P"   | "S"   | "T"   | "W"    | "Y"  | "V"
  | "*"
  | "X"
