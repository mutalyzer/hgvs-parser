// Common

LCASE_LETTER: "a".."z"
UCASE_LETTER: "A".."Z"

NAME: ((LCASE_LETTER) | (UCASE_LETTER) | (NUMBER))+

LETTER: UCASE_LETTER | LCASE_LETTER

NUMBER: ("0".."9")+

NT: "a" | "c" | "g" | "t" | "u" | "r" | "y" | "k"
  | "m" | "s" | "w" | "b" | "d" | "h" | "v" | "n"
  | "A" | "C" | "G" | "T" | "U" | "R" | "Y" | "K"
  | "M" | "S" | "W" | "B" | "D" | "H" | "V" | "N"

// Top rule
// --------

var: reference ":" coordinatesystem

// References
// ----------

reference: genbankref | lrgref

// Genbank references

genbankref: ACCESSION ("." VERSION)? specificlocus?

// Specific locus

specificlocus: "(" (accessionversion | geneproductid) ")"

accessionversion: ACCESSION "." VERSION

ACCESSION: (LETTER | NUMBER | "_")+

VERSION: NUMBER

geneproductid: GENENAME ( "_v" TRANSVAR | "_i" PROTISO)?

GENENAME: (LETTER | NUMBER | "-")+

TRANSVAR: NUMBER

PROTISO: NUMBER

// LRG references

lrgref.20: LRGREF (LRGSPECIFICLOCUS)?

LRGREF: "LRG_" NUMBER

LRGSPECIFICLOCUS: ("t" | "p") NUMBER

// Coordinate system

COORD: ("c" | "g" | "m" | "n" | "r")

coordinatesystem: COORD "."

