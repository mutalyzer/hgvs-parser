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

variant: substitution | del | dup | ins | inv | con | delins | varssr

substitution: position DELETED ">" INSERTED

DELETED: NT

INSERTED: NT

del: location "del" (DELETED_SEQUENCE | DELETED_LENGTH)?

DELETED_SEQUENCE: NT+

DELETED_LENGTH: NUMBER

dup: location "dup" (DUPLICATED_SEQUENCE | DUPLICATED_LENGTH)?

DUPLICATED_SEQUENCE: NT+

DUPLICATED_LENGTH: NUMBER

ins: range_location "ins" insertions

delins: location "del" (NT+ | NUMBER)? "ins" insertions

insertions: ("[" inserted (";" inserted)* "]") | inserted

inserted: (SEQUENCE | range_location INVERTED? | farloc)

INVERTED: "inv"

SEQUENCE: NT+

inv: range_location "inv" (NT+ | NUMBER)?

con: range_location "con" (range_location | farloc)

transloc: "t" chromcoords "(" farloc ")"

abrssr: position SEQUENCE "(" NUMBER "_" NUMBER ")"

varssr: (position SEQUENCE "[" REPEAT_LENGTH "]")
      | (range_location "[" REPEAT_LENGTH "]")
      | abrssr

REPEAT_LENGTH: NUMBER

// Locations
// ---------

location: position | range_location | uncertain

// Positions

position: OUTSIDETRANSLATION? POSITION OFFSET?
     | "IVS" INTRON OFFSET

POSITION: NUMBER | "?"

OFFSET: ("+" | "-") (NUMBER | "?")

OUTSIDETRANSLATION: "-" | "*"

INTRON: NUMBER

// Ranges

range_location: exloc
        | start_location "_" end_location

exloc: "EX" STARTEX ("-" ENDEX)?

STARTEX: NUMBER

ENDEX: NUMBER

start_location: position | uncertain

end_location: position | uncertain

// Uncertain

uncertain: "(" uncertain_start "_" uncertain_end ")"

uncertain_start: position

uncertain_end: position

// Other

farloc: (ACCESSION "." VERSION) (":" (COORDINATE ".")? range_location)?

chromband: ("p" | "q") NUMBER "." NUMBER

chromcoords: "(" chrom ";" chrom ")" "(" chromband ";" chromband ")"

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
