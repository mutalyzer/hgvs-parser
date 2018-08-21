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

// Operations

OPERATIONS: (LETTER | NUMBER | "-" | "_")+