// Top rule
// --------

description: reference variants

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
// --------

variants: (variant | "[" variant (";" variant)* "]")

variant: subst | del | dup | varssr | ins | indel | inv | conv

subst: ptloc DELETED ">" INSERTED

DELETED: NT

INSERTED: NT

del: (ptloc | rangeloc) "del" (DELETEDSEQ | DELETEDLENGTH)?

DELETEDSEQ: NT+

DELETEDLENGTH: NUMBER

dup: (ptloc | rangeloc) "dup" (SEQ | NUMBER)?

abrssr: ptloc NT+ "(" NUMBER "_" NUMBER ")"

varssr: (ptloc NT+ "[" NUMBER "]") | (rangeloc "[" NUMBER "]") | abrssr

ins: rangeloc "ins" simpleseqlist

indel: (rangeloc | ptloc) "del" (NT+ | NUMBER)? "ins" simpleseqlist

simpleseqlist: ("[" seqlist "]") | seq

seq: (NT+ | NUMBER | rangeloc "inv"? | farloc)

seqlist: seq (";" seq)*

inv: rangeloc "inv" (NT+ | NUMBER)?

conv: rangeloc "con" farloc

transloc: "t" chromcoords "(" farloc ")"


SEQ: NT+

// Locations
// ---------

loc: ptloc | rangeloc

// Positions

ptloc: OUTSIDETRANSLATION? POSITION OFFSET?
     | "IVS" INTRON OFFSET

POSITION: NUMBER | "?"

OFFSET: ("+" | "-") (NUMBER | "?")

OUTSIDETRANSLATION: "-" | "*"

INTRON: NUMBER

// Ranges

rangeloc: exloc
        | start_location "_" end_location
        | "(" start_range ")" "_" "(" end_range ")"

exloc: "EX" STARTEX ("-" ENDEX)?

STARTEX: NUMBER

ENDEX: NUMBER

start_location: ptloc | ((ACCESSION "." VERSION | GENENAME SELECTOR?) ":")? (COORDINATE ".")? ptloc

end_location: ptloc | ((ACCESSION "." VERSION | GENENAME SELECTOR?) ":")? (COORDINATE ".")? ptloc

start_range: start_location "_" end_location

end_range: start_location "_" end_location

// Other

farloc: (ACCESSION "." VERSION | GENENAME SELECTOR?) (":" (COORDINATE ".")? rangeloc)?

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
