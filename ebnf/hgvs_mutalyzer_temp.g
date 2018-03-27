LCASE_LETTER: "a".."z"
UCASE_LETTER: "A".."Z"

NAME: ((LCASE_LETTER) | (UCASE_LETTER) | (NUMBER))+

LETTER: UCASE_LETTER | LCASE_LETTER

NUMBER: ("0".."9")+

NT: "a" | "c" | "g" | "t" | "u" | "r" | "y" | "k"
  | "m" | "s" | "w" | "b" | "d" | "h" | "v" | "n"
  | "A" | "C" | "G" | "T" | "U" | "R" | "Y" | "K"
  | "M" | "S" | "W" | "B" | "D" | "H" | "V" | "N"


// Reference sequences

transvar: "_v" NUMBER

protiso: "_i" NUMBER

GENENAME: (LETTER | NUMBER | "-")+ // transformed into a token

geneproductid: GENENAME ( transvar | protiso)?

// accnostem was removed; no except or suppress utilized, in contrast to
// pyparse where "NotAny('LRG_')" was present

ACCNOFULL: ACC "." VERSION

genesymbol: "(" (geneproductid | ACCNOFULL) ")"

gi: ("GI" | "GI:" | "gi" | "gi:")? NUMBER

VERSION: NUMBER // transformed into a token (moved the '.' into the accno rule)

ACC: (LETTER | NUMBER | "_")+

accno: ACC "." VERSION?

UD: "UD_" [LETTER+] ("_" | NUMBER)+ // hopefully is equivalent to pyparsing

lrgtranscriptid: "t" NUMBER

lrgproteinid: "p" NUMBER

lrg: "LRG_" NUMBER (lrgtranscriptid | lrgproteinid)?

genbankref: (gi | accno | UD) genesymbol?

refseqacc: genbankref | lrg

chrom: NAME

COORD: ("c" | "g" | "m" | "n" | "r")

reftype: COORD "."

dref: (refseqacc | genesymbol)? ":" reftype?

refone: refseqacc ":" reftype?

// Locations

offset: ("+" | "-") ("u" | "d")? (NUMBER | "?")

realptloc: (("-" | "*")? NUMBER offset?) | "?" // was some grouping in pyparsing

ivsloc: "IVS" NUMBER ("+" | "-") NUMBER // was some grouping in pyparsing

ptloc: ivsloc | realptloc

realextent: ptloc "_" ("o"? (refseqacc | genesymbol) ":")? reftype? ptloc //
// was some grouping in pyparsing

exloc: "EX" NUMBER ("-" NUMBER)? // was some grouping in pyparsing

extent: realextent | exloc

rangeloc: extent | "(" extent | ")"

loc: ptloc | rangeloc // was some grouping in pyparsing

farloc: (refseqacc | genesymbol) (":" reftype? extent)?

chromband: ("p" | "q") NUMBER "." NUMBER

chromcoords: "(" chrom ";" chrom ")" "(" chromband ";" chromband ")"

// Single variations

subst: ptloc NT ">" NT  // setParseAction(replaceWith('subst')) for '>' in pyparsing

del: loc "del" (NT+ | NUMBER)?

dup: loc "dup" (NT+ | NUMBER)? // nest?

abrssr: ptloc NT+ "(" NUMBER "_" NUMBER ")"

varssr: (ptloc NT+ "[" NUMBER "]") | (rangeloc "[" NUMBER "]") | abrssr

seq: (NT+ | NUMBER | "inv"? | farloc) // nest?

seqlist: seq (";" seq)* // check delimitedList(Seq, delim=';')

simpleseqlist: ("[" seqlist "]") | seq

ins: rangeloc "ins" simpleseqlist

indel: (rangeloc | ptloc) "del" (NT+ | NUMBER)? "ins" simpleseqlist

inv: rangeloc "inv" (NT+ | NUMBER)? // nest?

conv: rangeloc "con" farloc // nest?

transloc: "t" chromcoords "(" farloc ")"

crawvar: subst | del | dup | varssr | ins | indel | inv | conv

rawvar: (crawvar | ("(" crawvar ")")) "?"? // originalTextFor(..) used in pyparsing

singlevar: refone (rawvar | transloc)

extendedrawvar: rawvar | "=" | "?"

unkeffectvar: dref ("(=)" | "?")

splicingvar: dref ("spl?" | "(spl?)")

nornavar: dref "0" "?"?

// Multiple variations

callelevarset: extendedrawvar (";" extendedrawvar)*

uallelevarset: (callelevarset | ("(" callelevarset ")")) "?"?

simpleallelevarset: ("[" uallelevarset "]") | extendedrawvar

mosaicset: "[" simpleallelevarset ("/" simpleallelevarset)* "]" | simpleallelevarset

chimeronset: ("[" mosaicset ("//" mosaicset)* "]") | mosaicset

singleallelevarset: ("[" chimeronset ((";" | "^") chimeronset)* ("(;)" chimeronset)* "]") | chimeronset

singleallelevars: dref singleallelevarset

multiallelevars: dref singleallelevarset (";" dref? singleallelevarset)+

multivar: singleallelevars | multiallelevars

multitranscriptvar: dref "[" extendedrawvar (";" extendedrawvar)* ("," extendedrawvar (";" extendedrawvar)*)+ "]"

// Top-level rule

var: singlevar | multivar | multitranscriptvar | unkeffectvar | nornavar | splicingvar //| proteinvar