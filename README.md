# HGVS Parser

Parser for HGVS variant descriptions.

It includes the original Mutalyzer `pyparsing` based implementation, for which
the EBNF grammar is written directly in Python, as well as the `lark` based
approach, which accepts the grammar written using the EBNF notation in a
separate file.

# Requirements

- Core requirements
  - Python 3.x
  - lark-parser
- Optional 
  - pyparsing (for the previous mutalyzer parser)
  - graphviz (for parse tree visualization)
- To run the tests
  - pytest


# Usage
```console
$ hgvsparser -h
usage: hgvsparser [-h] [-v] [-c] [-g G] [-r R] [-s S] [-p] description

hgvsparser: Parser for HGVS variant descriptions.

positional arguments:
  description  HGVS variant description to be parsed

optional arguments:
  -h, --help   show this help message and exit
  -v           show program's version number and exit
  -c           convert parse tree to model
  -g G         path to input grammar file
  -r R         start (top) rule for the grammar
  -s S         save parse tree as image
  -p           use the pyparsing parser

Copyright (c) 2018 Leiden University Medical Center <humgen@lumc.nl>
Copyright (c) 2018 Mihai Lefter <m.lefter@lumc.nl>
```


# Examples

## Successful parsing

```console
$ hgvsparser "NG_012232.1(NM_004006.1):c.93+1G>T" -c
{
  "reference": {
    "version": "1",
    "accession": "NG_012232",
    "type": "genbank"
  },
  "variants": [
    {
      "location": {
        "type": "point",
        "position": 92,
        "offset": {
          "value": 1
        }
      },
      "inserted": [
        {
          "sequence": "T",
          "source": "description"
        }
      ],
      "deleted": [
        {
          "sequence": "G",
          "source": "description"
        }
      ],
      "type": "substitution"
    }
  ],
  "specific_locus": {
    "version": "1",
    "accession": "NM_004006",
    "type": "genbank"
  },
  "coordinate_system": "c"
}
```

## Parsing errors


```console
$ hgvsparser "NM_00000:.-1+3C>A"
Error!
Unexpected input: .

NM_00000:.-1+3C>A
         ^

Expecting:
  - "(" for an uncertain position start
  - position (e.g., 100)
  - coordinate system: (e.g., "g", "c")
  - outside CDS ("*" or "-")
  - "=" to indicate no changes
  - __ANON_0
  - "[" for multiple variants, insertions, or repeats
```

```console
$ hgvsparser "NM_00000t1:g.100_200A>G" 
Error!
Unexpected input: A

NM_00000t1:g.100_200A>G
                    ^

Expecting:
  - "[" for multiple variants, insertions, or repeats
  - position offset ("-" or "+")
  - inv
  - duplication operation (e.g., 10dup)
  - conversion operation (e.g., 10_12con20_22)
  - deletion operation (e.g., 10del)
  - insertion operation (e.g., 11_12insTA, ins10_20)
  - "=" to indicate no changes
```

# Testing

```console
py.test tests
```
