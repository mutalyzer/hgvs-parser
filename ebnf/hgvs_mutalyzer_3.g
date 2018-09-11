// Top rule
// --------

description: reference variants

// References
// ----------

reference: reference_id specific_locus? ":" coordinate_system?

reference_id: ACCESSION ("." VERSION)?

ACCESSION: LETTER (LETTER | NUMBER | "_")+ ((DIGIT DIGIT) | ("_" DIGIT))

VERSION: NUMBER

// Specific locus

specific_locus: genbank_locus | LRG_LOCUS

genbank_locus: "(" ((ACCESSION "." VERSION) | GENE_NAME SELECTOR?) ")"

GENE_NAME: (LETTER | NUMBER | "-")+

SELECTOR: ("_v" | "_i") NUMBER

LRG_LOCUS: ("t" | "p") NUMBER

// Coordinate system

COORDINATE: ("c" | "g" | "m" | "n" | "r")

coordinate_system: COORDINATE "."

// Variants
// --------

variants: (variant | "[" variant (";" variant)* "]")

variant: substitution | del | dup | ins | inv | con | delins | varssr | equal

substitution: (point | uncertain) DELETED ">" INSERTED

DELETED: NT

INSERTED: NT

del: location "del" (DELETED_SEQUENCE | DELETED_LENGTH)?

DELETED_SEQUENCE: NT+

DELETED_LENGTH: NUMBER

dup: location "dup" (DUPLICATED_SEQUENCE | DUPLICATED_LENGTH)?

DUPLICATED_SEQUENCE: NT+

DUPLICATED_LENGTH: NUMBER

ins: range "ins" insertions

delins: location "del" (NT+ | NUMBER)? "ins" insertions

insertions: ("[" inserted (";" inserted)* "]") | inserted

inserted: SEQUENCE | range INVERTED? | reference_location INVERTED?

INVERTED: "inv"

SEQUENCE: NT+

inv: range "inv" (NT+ | NUMBER)?

con: range "con" inserted_location

inserted_location: range | reference_location

abrssr: (point | uncertain)  SEQUENCE "(" NUMBER "_" NUMBER ")"

varssr: (point SEQUENCE "[" REPEAT_LENGTH "]")
      | (range "[" REPEAT_LENGTH "]")
      | abrssr

equal: (point | range) "="

REPEAT_LENGTH: NUMBER

// Locations
// ---------

location: point | range | uncertain

// Positions

point: OUTSIDE_CDS? POSITION OFFSET?

POSITION: NUMBER | "?"

OFFSET: ("+" | "-") (NUMBER | "?")

OUTSIDE_CDS: "-" | "*"

// Ranges

range: start "_" end

start: point | uncertain

end: point | uncertain

// Uncertain

uncertain: "(" uncertain_start "_" uncertain_end ")"

uncertain_start: point

uncertain_end: point

// Other

reference_location: reference_id specific_locus? (":" (COORDINATE ".")? range)?

chrom: NAME

// Commons
// -------

LCASE_LETTER: "a".."z"

UCASE_LETTER: "A".."Z"

NAME: ((LCASE_LETTER) | (UCASE_LETTER) | (NUMBER))+

LETTER: UCASE_LETTER | LCASE_LETTER

DIGIT: "0".."9"

NUMBER: DIGIT+

NT: "a" | "c" | "g" | "t" | "u" | "r" | "y" | "k"
  | "m" | "s" | "w" | "b" | "d" | "h" | "v" | "n"
  | "A" | "C" | "G" | "T" | "U" | "R" | "Y" | "K"
  | "M" | "S" | "W" | "B" | "D" | "H" | "V" | "N"
