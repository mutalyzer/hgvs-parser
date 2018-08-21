// Common

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

// Top rule
// --------

var: reference variant

// References
// ----------

reference: refid specificlocus? ":" coordinatesystem?

refid: ACCESSION ("." VERSION)?

ACCESSION: LETTER (LETTER | NUMBER | "_")+ ((DIGIT DIGIT) | ("_" DIGIT))

VERSION: NUMBER

// Specific locus

specificlocus: genbanklocus | LRGLOCUS

genbanklocus: "(" ((ACCESSION "." VERSION) | GENENAME SELECTOR?) ")"

GENENAME: (LETTER | NUMBER | "-")+

SELECTOR: ("_v" | "_i") NUMBER

LRGLOCUS: ("t" | "p") NUMBER

// Coordinate system

COORDINATE: ("c" | "g" | "m" | "n" | "r")

coordinatesystem: COORDINATE "."

// Variants

variant: subst | del | dup | varssr | ins | indel | inv | conv

subst: ptloc NT ">" NT

del: loc "del" (NT+ | NUMBER)?

dup: loc "dup" (NT+ | NUMBER)?

abrssr: ptloc NT+ "(" NUMBER "_" NUMBER ")"

varssr: (ptloc NT+ "[" NUMBER "]") | (rangeloc "[" NUMBER "]") | abrssr

seq: (NT+ | NUMBER | rangeloc "inv"? | farloc)

seqlist: seq (";" seq)*

simpleseqlist: ("[" seqlist "]") | seq

ins: rangeloc "ins" simpleseqlist

indel: (rangeloc | ptloc) "del" (NT+ | NUMBER)? "ins" simpleseqlist

inv: rangeloc "inv" (NT+ | NUMBER)?

conv: rangeloc "con" farloc

transloc: "t" chromcoords "(" farloc ")"

// Locations

OFFSET: ("+" | "-") ("u" | "d")? (NUMBER | "?")

ptloc: (("-" | "*")? NUMBER OFFSET?) | "?"

extent: ptloc "_" ("o"? (refid | GENENAME) ":")? coordinatesystem? ptloc

rangeloc: extent | "(" extent | ")"

loc: ptloc | rangeloc

farloc: (refid | GENENAME) (":" coordinatesystem? extent)?

chromband: ("p" | "q") NUMBER "." NUMBER

chromcoords: "(" chrom ";" chrom ")" "(" chromband ";" chromband ")"

chrom: NAME
