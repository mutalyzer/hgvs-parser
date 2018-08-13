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

var: reference

// References
// ----------

reference: genbankref | lrgref

// Genbank references

genbankref: (ncbiref | udref) specificlocus?

ncbiref: ACC ("." VERSION)?

udref: UD

UD: "UD_" NUMBER+ "." NUMBER+

// Specific locus

specificlocus: "(" (ACCNOFULL | geneproductid) ")"

ACCNOFULL: ACC "." VERSION

ACC: (LETTER | NUMBER | "_")+

VERSION: NUMBER

geneproductid: GENENAME ( transvar | protiso)?

GENENAME: (LETTER | NUMBER | "-")+

transvar: "_v" NUMBER

protiso: "_i" NUMBER

// LRG references

lrgref.4: LRGREF (LRGTRANSCRIPTID | LRGPROTEINID)?

LRGREF: "LRG_" NUMBER

LRGTRANSCRIPTID: "t" NUMBER

LRGPROTEINID: "p" NUMBER
