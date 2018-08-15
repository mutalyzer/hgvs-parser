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

var: reference OPERATIONS?

// References
// ----------

reference: refid specificlocus? ":" coordinatesystem?

refid: ACCESSION ("." VERSION)?

ACCESSION: (LETTER | NUMBER | "_")+ DIGIT DIGIT

VERSION: NUMBER

// Specific locus

specificlocus: genbanklocus | LRGSPECIFICLOCUS

genbanklocus: "(" (refid | geneproductid) ")"

geneproductid: GENENAME SELECTOR?

GENENAME: (LETTER | NUMBER | "-")+

SELECTOR: ("_v" | "_i") NUMBER

LRGSPECIFICLOCUS: ("t" | "p") NUMBER

// Coordinate system

COORD: ("c" | "g" | "m" | "n" | "r")

coordinatesystem: COORD "."

// Operations

OPERATIONS: (LETTER | NUMBER | "-" | "_")+