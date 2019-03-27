description: reference ":" (LETTER ".")? allele

reference: IDENTIFIER (reference)? | "(" IDENTIFIER (reference)? ")"

IDENTIFIER: LETTER (LETTER | DIGIT | "." | "_" | "-")*

allele: (("[" ((variant (";" variant)*) | "=") "]") | variant | "=")

variant: location (conversion | deletion | deletion_insertion | duplication
                  | equal | insertion | inversion | substitution | repeat)?

location: point | uncertain_point | range

point: ("*" | "-")? (NUMBER | UNKNOWN) (OFFSET)?

OFFSET: ("+" | "-")? (NUMBER | UNKNOWN)

uncertain_point: "(" point "_" point ")"

range: (point | uncertain_point) "_" (point | uncertain_point)

exact_range: (NUMBER | UNKNOWN) "_" (NUMBER | UNKNOWN)

conversion: "con" inserted

inserted: (("[" (insert (";" insert)*) "]") | insert)

insert: (SEQUENCE | description | location | length) (("inv"? ("[" repeat_number "]")?)
                                                     | (("[" repeat_number "]")? "inv"?))?

repeat_number: (NUMBER | UNKNOWN | exact_range)

length: NUMBER | UNKNOWN | "(" (NUMBER | UNKNOWN | exact_range) ")"

deletion: "del" (inserted)?

deletion_insertion: "del" (inserted)? "ins" inserted

duplication: "dup" (inserted)?

insertion: "ins" inserted

inversion: "inv" (inserted)?

substitution: (SEQUENCE)? ">" inserted

repeat: "[" repeat_number "]" | (SEQUENCE "[" repeat_number "]")+

equal: "="

DIGIT: "0".."9"

NUMBER: DIGIT+

LCASE_LETTER: "a".."z"

UCASE_LETTER: "A".."Z"

LETTER: UCASE_LETTER | LCASE_LETTER

UNKNOWN: "?"

SEQUENCE: NT+

NT: "a" | "c" | "g" | "t" | "u" | "r" | "y" | "k"
  | "m" | "s" | "w" | "b" | "d" | "h" | "v" | "n"
  | "A" | "C" | "G" | "T" | "U" | "R" | "Y" | "K"
  | "M" | "S" | "W" | "B" | "D" | "H" | "V" | "N"
