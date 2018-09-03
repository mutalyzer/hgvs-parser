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

variant: substitution | deletion | duplication | insertion | inversion
       | conversion | deletion_insertion | varssr

substitution: position DELETED ">" INSERTED

DELETED: NT

INSERTED: NT

deletion: (position | range_location | uncertain_range) "del" (DELETED_SEQUENCE | DELETED_LENGTH)?

DELETED_SEQUENCE: NT+

DELETED_LENGTH: NUMBER

duplication: (position | range_location) "dup" (DUPLICATED_SEQUENCE | DUPLICATED_LENGTH)?

DUPLICATED_SEQUENCE: NT+

DUPLICATED_LENGTH: NUMBER

insertion: range_location "ins" insertions

deletion_insertion: (range_location | position) "del" (NT+ | NUMBER)? "ins" insertions

insertions: ("[" inserted (";" inserted)* "]") | inserted

inserted: (SEQUENCE | range_location INVERTED? | farloc)

INVERTED: "inv"

SEQUENCE: NT+

inversion: range_location "inv" (NT+ | NUMBER)?

conversion: range_location "con" farloc

transloc: "t" chromcoords "(" farloc ")"

abrssr: position NT+ "(" NUMBER "_" NUMBER ")"

varssr: (position NT+ "[" NUMBER "]") | (range_location "[" NUMBER "]") | abrssr


// Locations
// ---------

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

start_location: position

end_location: position

start_range: start_location "_" end_location

end_range: start_location "_" end_location

// Uncertain

uncertain_range: "(" range_location ")"
               | "(" start_range ")" "_" "(" end_range ")"

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
